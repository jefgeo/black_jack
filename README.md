# black_jack
A simple BlackJack game.  The game shows the use of classes in Python:  
### Card 
a class that provides the suit and value of a card as a string and the numeric value of the card.   
### Deck
an array of cards.  On itit, it creates the deck and shuffles it.  Cards are also dealt from the deck.  
### Hand 
an array of cards.  Show lists all of the cards.  There is also a property for the value of the hand and a flag is the hand has busted. 
### Bank 
tracks the amount the player has and has a string to show it. 
### Player 
deals initial cards, takes the player's bet, allows the user to select the next play (Hit, No Hit, or Double), and prints the status.  
### Dealer 
inherits their hand from player.  It overrides next_play based on standard dealer rules, 
### Game
main look for the game.  It instantiates teh deck, creates a dealer, and keeps an array of players.  
