import cards

class Player:
    
    def __init__(self, name) -> None:
        self.name = name


class Game:

    def __init__(self, players: list[str]) -> None:

        self.players = [ Player(name) for name in players ]

        self.state = GameState(len(players))


class GameState:

    def __init__(self, players) -> None:
        self.stock = cards.deck()
        self.dump = []
        self.hands = [ [] for i in range(players) ]
        self.player_on_turn = 0
        self.next_must_take = 0
        self.next_must_skip = False
        self.next_may_take = True
        self.next_may_skip = False
        self.next_suit = None
        self.next_rank = None

    def __str__(self) -> str:
        return 'Game(' \
                + 'faceup={}'.format(self.dump[-1]) \
                + ', stock={}'.format(len(self.stock)) \
                + ', dump={}'.format(len(self.dump)) \
                + f', next_suit={self.next_suit}, next_rank={self.next_rank}' \
                + f', next_must_take={self.next_must_take}, next_must_skip={self.next_must_skip}' \
                + f', next_may_take={self.next_may_take}, next_may_skip={self.next_may_skip}' \
                + ')'


from random import shuffle

class GameController:
    
    def __init__(self, game) -> None:
        self.game = game
        self.state = game.state

    def setup(self):
        self.state.stock = cards.deck()
        shuffle(self.state.stock)
        self.deal_cards(5)
        self.state.dump.append(self.state.stock.pop())

    def deal_cards(self, count):
        for n in range(count):
            for hand in self.state.hands:
                hand.append(self.state.stock.pop())

    def get_player_on_turn(self) -> int:
        return self.state.player_on_turn

    def handle_move(self, move):
        if move[0] != self.get_player_on_turn():
            raise IllegalMoveException('It is not your turn.')
        
        match move[1]:
            case 'play':
                self.handle_play_move(move)
            case 'take':
                self.handle_take_move(move)
            case 'skip':
                self.handle_skip_move(move)

    def handle_skip_move(self, move):
        if self.state.next_must_skip or self.state.next_may_skip:
            self.state.next_must_skip = False
            self.end_turn()
        elif self.state.next_must_take > 0:
            raise IllegalMoveException('You must take cards or play a SEVEN.')
        else:
            raise IllegalMoveException('You must take a card if you cannot play.')
        
    def handle_take_move(self, move):

        player, _, count = move

        if self.state.next_must_skip:
            raise IllegalMoveException('You must skip or play an EIGHT.')
        
        elif not self.state.next_may_take:
            raise IllegalMoveException('You must play a card or skip.')
        
        elif self.state.next_must_take > 0:
            if count == self.state.next_must_take:
                for n in range(self.state.next_must_take):
                    self.take_card(player, self.draw_card())
                self.state.next_must_take = 0
                self.state.next_may_take = False
                self.state.next_may_skip = True
                # no end of turn
            else:
                raise IllegalMoveException(f'You must take {self.state.next_must_take} cards.')
            
        else:
            if count == 1:
                self.take_card(player, self.draw_card())
                self.state.next_may_take = False
                self.state.next_may_skip = True
                # no end of turn
            else:
                raise IllegalMoveException('You must only take one card if you cannot play.')

    def handle_play_move(self, move):
        
        player, _, card, next_suit = move
        rank, suit = card

        if self.state.next_must_skip:
            if rank == 'EIGHT':
                self.play_card(player, card)
                self.state.dump.append(card)
                self.end_turn()
            else:
                raise IllegalMoveException('You must play an EIGHT or skip.')
        elif self.state.next_must_take > 0:
            if rank == 'SEVEN':
                self.play_card(player, card)
                self.state.dump.append(card)
                self.state.next_must_take = self.state.next_must_take + 2
                self.end_turn()
            else:
                raise IllegalMoveException('You must play a SEVEN or take cards.')
        else:
            if not self.follows(card):
                raise IllegalMoveException('Card must follow suit or rank.')
            
            self.play_card(player, card)
            self.state.dump.append(card)
            self.state.next_rank = None if rank in ['JAKE', 'ACE'] else rank
            self.state.next_suit = next_suit

            match rank:
                case 'SEVEN':
                    self.state.next_must_take = 2
                    self.end_turn()
                case 'EIGHT':
                    self.state.next_must_skip = True
                    self.end_turn()
                case 'ACE':
                    pass # no end turn
                case _:
                    self.end_turn()

    def play_card(self, player, card):
        
        if not card in self.state.hands[player]:
            raise ValueError('No such card in hand.')
        
        self.state.hands[player].remove(card)

        return card

    def draw_card(self):
        if not len(self.state.stock):
            top = self.state.dump.pop()
            while self.state.dump:
                self.state.stock.append(self.state.dump.pop())
            self.state.dump.append(top)
            shuffle(self.state.stock)
        return self.state.stock.pop()
    
    def take_card(self, player, card):
        self.state.hands[player].append(card)

    def follows(self, card):
        
        rank, _ = card

        if rank == 'JAKE':
            return True

        if not self.state.next_rank:
            return self.follows_suit(card)

        return self.follows_suit(card) or self.follows_rank(card)
    
    def follows_suit(self, card):
        return self.state.next_suit == card[1] or not self.state.next_suit
    
    def follows_rank(self, card):
        return self.state.next_rank == card[0] or not self.state.next_rank
    
    def end_turn(self):
        self.state.next_may_skip = False
        self.state.next_may_take = True
        self.state.player_on_turn = (self.state.player_on_turn + 1) \
            % len(self.game.players)

    def is_game_over(self):
        return any(not hand for hand in self.state.hands)
    

class IllegalMoveException(Exception):
    pass