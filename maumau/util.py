def prompt_int(prompt, min, max):
    n = None
    while n == None or n < min or n > max:
        try:
            n = int(input(f'{prompt} [{min}, {max}]: '))
        except ValueError:
            pass
    return n


def prompt_move(player_name, player, hand, max_take):

    print('Player {}: {}'.format(player_name, hand))
    n = prompt_int('Make your move', -len(hand), max_take)
    
    if n < 0: # play card
        card = hand[-1-n]
        if card[0] == 'JAKE':
            next_suit = prompt_suit()
            return (player, 'play', card, next_suit)
        else:
            return (player, 'play', card, card[1])
    elif n > 0: # take cards
        return (player, 'take', n)
    else: # skip
        return (player, 'skip')


def prompt_suit():
    match prompt_int('Choose next suit (CLUBS, HEARTS, SPADES, DIAMONDS)', 1, 4):
        case 1: return 'CLUBS'
        case 2: return 'HEARTS'
        case 3: return 'SPADES'
        case 4: return 'DIAMONDS'

def prompt_names():
    
    print('Enter player names (empty line terminates input):')
    name = True
    names = []

    while name:
        name = input().strip()
        names.append(name)

    return names