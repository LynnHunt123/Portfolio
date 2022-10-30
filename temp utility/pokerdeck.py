from enum import IntEnum
import random

class Suit(IntEnum):
    spade = 1
    heart = 2
    diamond = 3
    club = 4

class Rank(IntEnum):
    Ace, Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Jack, Queen, King = range(1,14)


class PokerCard:
    suit_dict = {Suit(1): "\u2660",
                    Suit(2): "\u2665", 
                    Suit(3): "\u2666", 
                    Suit(4): "\u2663"}
    rank_dict = {Rank(i): str(i) for i in range(2,11)}
    rank_dict[Rank(11)] = "J"
    rank_dict[Rank(12)] = "Q"
    rank_dict[Rank(13)] = "K"
    rank_dict[Rank(1)] = "A"
    def __init__(self, s: int, r: int):
        self.suit = Suit(s)
        self.rank = Rank(r)

    def __str__(self):
        return f"[{self.suit_dict[self.suit]}{self.rank_dict[self.rank]}]"


class PokerDeck:

    def __init__(self):
        self.deck = [PokerCard(suit, rank) for rank in range(1, 14) for suit in range(1, 5) ]
    
    def shuffle(self):
        random.shuffle(self.deck)

    def __str__(self):
        s = "\n".join(
            [f"{Rank(i+1)}: {self.deck[4*i]}-{self.deck[4*i+1]}-{self.deck[4*i+2]}-{self.deck[4*i+3]}" for i in range(13)]
        )
        return s

def pop_order(poker_deck: PokerDeck, init_pos: int = 13):
    divided = {
        i+1: poker_deck.deck[4*i:4*(i+1)] for i in range(13)
    }
    init_deck = poker_deck
    pos = init_pos
    res = []
    while True:
        if divided[pos]:
            popped = divided[pos].pop(0)
            pos = popped.rank
            res.append(popped)
        else:
            break
    return {
        "init_deck": init_deck, 
        "res": res,
        "divided": divided
    }

def print_pop_order(result_dict: dict):
    init_deck = result_dict["init_deck"]
    res = result_dict["res"]
    divided = result_dict["divided"]
    print("Initial:")
    print('-'.join([str(card) for card in init_deck.deck]))
    print()
    print("New Order:")
    print('-'.join([str(card) for card in res]))
    print()
    print("Sub-decks:")
    for key, val in divided.items():
        print(f"{key}: {[str(v) for v in val]}")


if __name__ == "__main__":
    deck = PokerDeck()
    deck.shuffle()
    # print(deck)
    d = pop_order(deck)
    # for key, val in d.items():
    #     print(f"{key}: {[str(v) for v in val]}")
    print_pop_order(d)

