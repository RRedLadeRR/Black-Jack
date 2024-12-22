import cards, games

class BlackJack_Card(cards.Positionable_Card):
    ace_value = 1

    @property
    def total(self):
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
    def __init__(self, name, capital=100):
        super().__init__(name)
        self.capital = capital
        self.bet = 0

    def make_bet(self):
        print(f"{self.name}, у вас є {self.capital} грошей.")
        while True:
            try:
                self.bet = int(input(f"{self.name}, введіть ставку: "))
                if 0 < self.bet <= self.capital:
                    self.capital -= self.bet
                    print(f"{self.name} зробив ставку {self.bet}. Залишок: {self.capital}.")
                    break
                else:
                    print("Недійсна ставка. Введіть суму в межах вашого капіталу.")
            except ValueError:
                print("Введіть ціле число.")

    def win(self):
        winnings = self.bet * 2
        self.capital += winnings
        print(f"{self.name} виграв {winnings}! Тепер у нього {self.capital} грошей.")

    def lose(self):
        print(f"{self.name} програв {self.bet}. Залишок: {self.capital}.")

    def push(self):
        self.capital += self.bet
        print(f"{self.name} зіграв у нічию. Ставка {self.bet} повернена. Залишок: {self.capital}.")

class BlackJack_Dealer(BlackJack_Hand):
    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "перебрав.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()

class BlackJack_Game:
    def __init__(self, names):
        self.players = []
        for name in names:
            player = BlackJack_Player(name)
            self.players.append(player)

        self.dealer = BlackJack_Dealer("Дилер")
        self.deck = BlackJack_Deck()
        self.deck.populate()
        self.deck.shuffle()

    def play(self):
        if not self.players:
            print("У грі не залишилося гравців. Гра закінчується.")
            return

        for player in self.players:
            player.make_bet()

        self.check_deck(min_cards=10)
        self.deck.deal(self.players + [self.dealer], per_hand=2)

        self.dealer.flip_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)

        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()
        print(self.dealer)

        if self.still_playing():
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                for player in self.still_playing():
                    player.win()
            else:
                for player in self.still_playing():
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        self.players = [player for player in self.players if player.capital > 0]

        if not self.players:
            print("Усі гравці втратили свої гроші. Гра завершена.")
        else:
            for player in self.players:
                print(f"{player.name} залишок капіталу: {player.capital}.")

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def check_deck(self, min_cards):
        if len(self.deck.cards) < min_cards:
            print(f"Увага! У колоді залишилося лише {len(self.deck.cards)} карт.")
            self.deck.add_new_deck()

    def still_playing(self):
        return [player for player in self.players if not player.is_busted()]

def main():
    print("\t\tЛаскаво просимо до гри 'Блек-джек'!\n")

    names = []
    number = games.ask_number("Скільки гравців? (1 - 7):", low=1, high=7)

    for i in range(number):
        name = input("Введіть ім'я гравця №" + str(i + 1) + ": ")
        names.append(name)
    print()

    game = BlackJack_Game(names)

    again = None
    while again != "n":
        game.play()
        if not game.players:
            break
        again = games.ask_yes_no("\nХочете зіграти ще один раунд?")

    print("Дякуємо за гру!")

if __name__ == "__main__":
    main()
