import cards, games

class BlackJack_Card(cards.Positionable_Card):
    ace_value = 1

    @property
    def total(self):
        for card in self.cards:
            if not card.value:
                return None
        t = 0
        contains_ace = False
        for card in self.cards:
            t += card.value
            if card.value == BlackJack_Card.ace_value:
                contains_ace = True
        if contains_ace and t <= 11:
            t += 10
        return t
    
    def is_busted(self):
        return self.total > 21

    def value(self):
        if self.is_face_up:
            v = BlackJack_Card.ranks.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v
    
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp
    
    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        self.deck.deal(self.players + [self.dealer], per_hand = 2)
        self.dealer.flip_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)
        for player in self.players:
            self.__additional_cards(player)
        self.dealer.flip_first_card()
        if not self.still_playing:
            print(self.dealer)
        else:
            print(self.dealer)
            self.__additional_cards(self.dealer)
            if self.dealer.is_busted():
                for player in self.still_playing:
                    player.win()
            else:
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()
        for player in self.players:
    
class BlackJack_Deck(cards.Deck):
    def populate(self):
        for suit in BlackJack_Card.suits:
            for rank in BlackJack_Card.ranks:
                self.cards.append(BlackJack_Card(rank, suit))

class BlackJack_Hand(cards.Hand):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super().__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep
    
class BlackJack_Player(BlackJack_Hand):
    def is_hitting(self):
        response = games.ask_yes_no("\n" + self.name + ", will take more cards")
        return response == "y"
    
    def bust(self):
        print(self.name, "took to much.")
        self.lose()

    def lose(self):
        print(self.name, "has lost.")
    
    def win(self):
        print(self.name, "has won.")

    def push(self):
        print(self.name, "played draw with the dealer.")

class BlackJack_Dealer(BlackJack_Hand):
    def is_hitting(self):
        return self.total < 17
    
    def bust(self):
        print(self.name, "took to much.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()

class BlackJack_Game:
    def __init__(self, names):
        self.players = []
        for name in names:
            player = BlackJack_Player(name)
            self.players.append(player)

        self.dealer = BlackJack_Dealer("Dealer")

        self.deck = BlackJack_Deck()
        self.deck.populate()
        self.deck.shuffle()



def ask_yes_no(question):
    response = None
    while response not in ("y", "n"):
        response = input(question + " (y/n)?").lower()
    return response

def ask_number(question, low, high):
    response = None
    while response not in range(low, high + 1):
        response = int(input(question))
    return response

if __name__ == "__main__":
    print("You started games module, ""but not imported it (import games).")
    print("Testing module.")
    answer = ask_yes_no("Continue testing")
    print("Function ask_yes_no returned", answer)
    answer = ask_number("Enter integer from 1 to 10:", 1, 10)
    print("Function ask_number returned", answer)

class Card:

    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    suits = [u"\u2660", u"\u2663", u"\u2665", u"\u2666"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        rep = self.rank + self.suit
        return rep
    
class Unprintable_Card(Card):

    def __str__(self):
        return "<Cant be printed>"
    
class Positionable_Card(Card):

    def __init__(self, rank, suit, face_up = True):
        super().__init__(rank, suit)
        self.is_face_up = face_up
    def __str__(self):
        if self.is_face_up:
            rep = super().__str__()
        else:
            rep = "▮▮"
        return rep
    def flip(self):
        self.is_face_up = not self.is_face_up

class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + "\t"
        else:
            rep = "<empty>"
        return rep
    
    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)

class Deck(Hand):

    def populate(self):
        for suit in Card.suits:
            for rank in Card.ranks:
                self.add(Card(rank,suit))

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def add_new_deck(self):
        self.populate()
        self.shuffle()

    def deal(self, hands, per_hand = 1):
        for rounds in range(per_hand):
            for hand in hands:
                if not self.cards:
                    seld.add_new_deck()
                top_card = self.cards[0]
                self.give(top_card, hand)

def main():
    print("\t\tWelcome to Black Jack\n")

    names = []
    number = games.ask_number("How many players? (1 - 7):", low = 1, high = 7)

    for i in range(number):
        name = input("Enter player name № " + str(i + 1) + ":")
        names.append(name)
    print()

    game = BlackJack_Game(names)

    again = None
    while again != "n":
        game.play()
        again = games.ask_yes_no("\nWant to play one more time?")

main()

if __name__ == "__main__":
    print("You started games module, ""but not imported it (import games).")
    print("Testing module.\n")

    card1 = Card("A", Card.suits[0])
    card2 = Unprintable_Card("A", Card.suits[1])
    card3 = Positionable_Card("A", Card.suits[2])
    print("Card object:", card1)
    print("Unprintable_Card object:", card2)
    print("Positionable_Card object:", card3)
    card3.flip()
    print("Turn over Positionable_Card object:", card3)

    deck1 = Deck()
    print("\nCreating new deck", deck1)
    deck1.populate()
    print("New cards in deck appeared:", deck1, sep="\n")
    deck1.shuffle()
    print("Deck shuffled:", deck1, sep="\n")
    hand1 = Hand()
    hand2 = Hand()
    deck1.deal(hands=(hand1, hand2), per_hand = 5)
    print("\n5 cards dealt.")
    print("Hand1:", hand1)
    print("Hand2:", hand2)
    print("Left in deck:", deck1, sep="\n")
    deck1.clear()
    print("Deck cleared:", deck1)
