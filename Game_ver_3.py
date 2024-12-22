import random

class Card:
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = [u"\u2660", u"\u2663", u"\u2665", u"\u2666"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + self.suit

class Positionable_Card(Card):
    def __init__(self, rank, suit, face_up=True):
        super().__init__(rank, suit)
        self.is_face_up = face_up

    def __str__(self):
        return super().__str__() if self.is_face_up else "▮▮"

    def flip(self):
        self.is_face_up = not self.is_face_up

class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        return "\t".join(map(str, self.cards)) if self.cards else "<empty>"

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
                self.add(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, hands, per_hand=1):
        for _ in range(per_hand):
            for hand in hands:
                if not self.cards:
                    self.populate()
                    self.shuffle()
                    print("\nNew deck is populated and shuffled!")
                top_card = self.cards[0]
                self.give(top_card, hand)

class BlackJack_Card(Positionable_Card):
    ace_value = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BlackJack_Card.ranks.index(self.rank) + 1
            if v > 10:
                v = 10
            return v
        return None

class BlackJack_Hand(Hand):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.bet = 0
        self.balance = 100

    @property
    def total(self):
        if not self.cards:
            return 0
        total = 0
        contains_ace = False
        for card in self.cards:
            if not card.value:
                return None
            total += card.value
            if card.value == BlackJack_Card.ace_value:
                contains_ace = True
        if contains_ace and total <= 11:
            total += 10
        return total

    def is_busted(self):
        return self.total > 21

    def __str__(self):
        rep = f"{self.name}:\t{super().__str__()}"
        if self.total:
            rep += f" ({self.total})"
        return rep

class BlackJack_Player(BlackJack_Hand):
    def is_hitting(self):
        response = input(f"\n{self.name}, do you want another card (y/n)? ").lower()
        return response == "y"

    def place_bet(self):
        while True:
            try:
                self.bet = int(input(f"{self.name}, you have ${self.balance}. Enter your bet: "))
                if 0 < self.bet <= self.balance:
                    self.balance -= self.bet
                    break
                else:
                    print("Invalid bet amount.")
            except ValueError:
                print("Please enter a valid number.")

    def bust(self):
        print(f"{self.name} busts!")

    def win(self):
        winnings = self.bet * 2
        self.balance += winnings
        print(f"{self.name} wins ${winnings}!")

    def lose(self):
        print(f"{self.name} loses.")

    def push(self):
        self.balance += self.bet
        print(f"{self.name} pushes. Bet returned.")

class BlackJack_Dealer(BlackJack_Hand):
    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print("Dealer busts!")

    def flip_first_card(self):
        if self.cards:
            self.cards[0].flip()

class BlackJack_Game:
    def __init__(self, names):
        self.players = [BlackJack_Player(name) for name in names]
        self.dealer = BlackJack_Dealer("Dealer")
        self.deck = Deck()
        self.deck.populate()
        self.deck.shuffle()

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        for player in self.players:
            if player.balance <= 0:
                print(f"{player.name} is out of money and leaves the table.")
        self.players = [player for player in self.players if player.balance > 0]

        if not self.players:
            print("All players are out of money. Game over.")
            return

        for player in self.players:
            player.place_bet()

        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)

        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()
        print(self.dealer)
        if any(not player.is_busted() for player in self.players):
            self.__additional_cards(self.dealer)

        if self.dealer.is_busted():
            for player in self.players:
                if not player.is_busted():
                    player.win()
        else:
            for player in self.players:
                if not player.is_busted():
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        for player in self.players:
            player.clear()
        self.dealer.clear()

def main():
    print("\t\tWelcome to Black Jack\n")
    names = []
    number = int(input("How many players? (1-7): "))
    for i in range(number):
        name = input(f"Enter player name #{i + 1}: ")
        names.append(name)
    print()

    game = BlackJack_Game(names)

    while True:
        game.play()
        again = input("\nDo you want to play again (y/n)? ").lower()
        if again != "y":
            break

main()
