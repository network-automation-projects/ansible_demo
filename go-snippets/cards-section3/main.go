package main

func main() {
	//cards := newDeck()

	//cardString := cards.toString()

	// print(cardString)

	//cards.saveToFile("my_cards.txt")

	loadedCards := newDeckFromFile("my_rds.txt")

	loadedCards.shuffle()

	loadedCards.printEach()

	// hand, remainingCards := deal(cards, 5)

	// hand.printEach()
	// remainingCards.printEach()
}
