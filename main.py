import random


class Card:

    def __init__(self, value, suit):
        if 4 >= suit >= 1:
            self.suit = suit
        else:
            self.suit = 1
        if 13 >= value >= 1:
            self.value = value
        else:
            self.value = 1

    def __str__(self):
        return self.card_name

    @property
    def card_value(self):
        return self.value_map[self.value][1]

    @property
    def card_name(self):
        return '{} of {}'.format(self.value_map[self.value][0], self.suit_map[self.suit])

    value_map = {1: ['Ace', 1], 2: ['Two', 2], 3: ['Three', 3], 4: ['Four', 4], 6: ['Six', 6],
                 5: ['Five', 5], 7: ['Seven', 7], 8: ['Eight', 8], 9: ['Nine ', 9], 10: ['Ten', 10],
                 11: ['Jack', 10], 12: ['Queen', 10], 13: ['King', 10]}

    suit_map = {1: 'Hearts', 3: 'Diamonds', 2: 'Spades', 4: 'Clubs'}


class Deck:

    def __init__(self):
        self.deck = []
        for value in range(1, 14):
            for suit in range(1, 5):
                self.deck.append(Card(value, suit))
        random.shuffle(self.deck)

    @property
    def cards_left(self):
        return len(self.deck)

    def deal_card(self):
        return self.deck.pop()


class Hand:

    def __init__(self):

        self.hand = []  # Array of cards
        self.hand_value = 0
        self.soft = False

    def get_card(self, card):
        self.hand.append(card)
        if card.card_value == 1:
            self.soft = True
        self.hand_value = self.hand_value + card.card_value

    def show(self, hide_first):
        string = ""
        if not hide_first:
            for card in self.hand:
                string += str(card) + ", "
            string = string[0:len(string) - 2]
            string += " ("
            string += str(self.hand_value)
            string += (" or " + str(self.hand_value + 10)) if (self.soft and self.hand_value <= 11) else ""
            string += ")"
        else:
            for card in self.hand[1:]:
                string += str(card) + ", "
            string = string[0:len(string) - 2] + "\n"
        return string

    @property
    def busted(self):
        return self.hand_value > 21

    @property
    def score(self):
        return self.hand_value + 10 if (self.hand_value <= 11 and self.soft) else self.hand_value

    @property
    def cards_in_hand(self):
        return len(self.hand)


class Bank:

    def __init__(self, value):
        self.value = value

    def show(self):
        return "Current Balance is: " + str(self.value)


class Player:

    def __init__(self, name):
        self.hand = Hand()
        self.bank = Bank(100)
        self.currentBet = 0
        self.name = name

    def deal(self, deck):
        self.hand.__init__()
        self.hand.get_card(deck.deal_card())
        self.hand.get_card(deck.deal_card())

    def next_play(self):
        if not self.hand.busted:

            try:
                choice = str.upper(input("Player hit? (Y/N/D)"))[0:1]
            except ValueError:
                choice = 'N'
            if choice == "Y":
                return True
            elif choice == "D":
                self.bank.value -= self.currentBet
                self.currentBet = self.currentBet * 2
                return True
            else:
                return False

    def best_score(self):
        return self.hand.score

    def status(self, showHand=True, showBank=False, dealerFirstRound=False):
        string = "Player " + self.name + ":  "
        if showBank:
            string += self.bank.show() + "\n "
        if showHand:
            string += self.hand.show(hide_first=dealerFirstRound)
        return string

    def set_bet(self):
        if self.bank.value > 0:
            try:
                bet = int(input(self.name + ", you have $" + str(self.bank.value) + ".  How much do you want to bet? "))
            except ValueError:
                print("Must enter a number.  Defaulting to $1")
                bet = 1
            if bet > 0:
                if bet > self.bank.value:
                    bet = self.bank.value
                self.bank.value -= bet
                self.currentBet = bet
                return bet
        else:
            self.currentBet = 0
            return 0


class Dealer(Player):

    def __init__(self):
        super().__init__(name="Dealer")

    def next_play(self):
        if not self.hand.busted and self.hand.hand_value < 17:
            return True
        else:
            return False

    def status(self, showHand=True, showBank=False, dealerFirstRound=False):
        string = "DEALER "
        string += self.hand.show(hide_first=dealerFirstRound) + '\n'
        return string


def Game():
    deck = Deck()
    dealer = Dealer()
    players = []

    try:
        number_players = int(input("Number of Players?  "))
    except ValueError:
        print("must enter a number.  Defaulting to 1 player")
        number_players = 1

    for i in range(0, number_players):
        players.append(Player(input("Player Name: ")))

    # MAIN GAME
    while True:
        # PLAYERS LOOP
        players_in = 0
        dealer.deal(deck)

        for player in players:
            player.set_bet()
            if player.currentBet > 0:
                players_in += 1

        if players_in == 0:
            break

        for player in players:
            if player.currentBet > 0:
                player.deal(deck)
                print("Player:\n", player.status(showBank=True))
                print("Dealer:\n", dealer.status(dealerFirstRound=True))

                while player.next_play():
                    player.hand.get_card(deck.deal_card())
                    print("Player:\n", player.status())

            # Dealer Loop
        while dealer.next_play():
            dealer.hand.get_card(deck.deal_card())
            print("\nCurrent Dealer:\n", dealer.status())

        for player in players:
            if player.currentBet > 0:

                print("\nPlayer Final:  ", player.status())
                print("Dealer Final:  ", dealer.status())

                if player.hand.score == dealer.hand.score:
                    print("PUSH")
                    player.bank.value += player.currentBet
                elif (player.hand.score > dealer.hand.score or dealer.hand.busted) and not player.hand.busted:
                    print("PLAYER WINS")
                    player.bank.value += 2 * player.currentBet
                else:
                    print("DEALER WINS")
                print(player.status(showHand=False, showBank=True))


if __name__ == '__main__':
    Game()
