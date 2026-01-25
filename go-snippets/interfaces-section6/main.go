package main

import "fmt"

type chatBot interface {
	getGreeting() string
}

type engChatBot struct{}
type spanishChatBot struct{}

func (eb engChatBot) getGreeting() string {
	return "Hello, World!"
}

func (sb spanishChatBot) getGreeting() string {
	return "Hola, Mundo!"
}

func printGreeting(b chatBot) {
	fmt.Println(b.getGreeting())
}

func main() {
	eb := engChatBot{}
	sb := spanishChatBot{}
	printGreeting(eb)
	printGreeting(sb)
}

// package main

// import "fmt"

// type engChatBot struct{}
// type spanishChatBot struct{}

// func printGreeting(eb engChatBot) {
// 	fmt.Println("Hello, World!")
// }

// func printGreeting(sb spanishChatBot) {
// 	fmt.Println("Hola, Mundo!")
// }

// func main() {
// 	eb := engChatBot{}
// 	sb := spanishChatBot{}
// 	printGreeting(eb)
// 	printGreeting(sb)
// }
