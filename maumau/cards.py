
SUITS = { 'CLUBS', 'HEARTS', 'SPADES', 'DIAMONDS' }
RANKS = { 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'JAKE', 'QUEEN', 'KING', 'ACE' }

def deck():
    return [ (rank, suit) for rank in RANKS for suit in SUITS ]