from game import Game, GameController, IllegalMoveException
from util import prompt_move, prompt_names


def main():
    
    print('Let\'s play Mau-Mau!')

    players = prompt_names()
    game = Game(players)
    ctrl = GameController(game)
    ctrl.setup()

    while not ctrl.is_game_over():
        
        print(f'\n{game.state}')

        try:
            player = ctrl.get_player_on_turn()
            move = prompt_move(
                    game.players[player].name,
                    player,
                    ctrl.state.hands[player],
                    max(1, ctrl.state.next_must_take)
                    )
            print(move)
            ctrl.handle_move(move)
        
        except IllegalMoveException as e:
            print(e)
    
    print('\nGame over!')


if __name__ == '__main__':
    main()