package main

import (
	"fmt"
	"math"
)

func main() {

	myNumbers := []int{}

	//loop through 0 to 9
	for i := 0; i < 10; i++ {
		myNumbers = append(myNumbers, i)
		if math.Mod(float64(i), 2) == 0 {
			fmt.Println("Even")
		} else {
			fmt.Println("Odd")
		}
	}

	fmt.Println(myNumbers)

}
