package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")

	//var colors map[string]string

	// colors := make(map[string]string)
	// colors["red"] = "#ff0000"
	// colors["green"] = "#00ff00"
	// colors["blue"] = "#0000ff"

	// fmt.Println(colors)

	//create a map
	colors := map[string]string{
		"red":   "#ff0000",
		"green": "#00ff00",
		"blue":  "#0000ff", //so weird, but this comma is required at the end of the map
	}

	colors["yellow"] = "#ffff00"
	delete(colors, "red")

	fmt.Println(colors) //this will print the map as a map
	printMap(colors)    //this will print the map items one by one

}

// print the map
func printMap(c map[string]string) {
	for color, hex := range c {
		fmt.Println("Hex code for", color, "is", hex)
	}
	//if we make a change to the map c inside here, it will
	//change the original map because we are passing the reference to the map
	//if we want to make a copy of the map, we can do:
	//newMap := make(map[string]string)
	//for color, hex := range c {
	//	newMap[color] = hex
	//}
	//return newMap
	//but this is not efficient, so we can just pass the reference to the map

	//that's different than passing a struct,
	//if we pass a struct to a function, the function will receive a copy of the struct, not the original struct
	//if we want to make a change to the struct inside the function, we need to pass a pointer to the struct
}
