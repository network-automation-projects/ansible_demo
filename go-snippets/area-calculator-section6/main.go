package main

import (
	"fmt"
)

type shape interface {
	getArea() float64
}

// create custom struct types triangle and square
type triangle struct { // ✅ Correct
	height float64
	base   float64
}

type square struct {
	sideLength float64
}

func main() {
	triangle1 := triangle{2, 4}
	square1 := square{3}
	printShape(triangle1)
	printShape(square1)

}

func (t triangle) getArea() float64 {
	area := 0.5 * t.height * t.base
	return float64(area)
}

func (s square) getArea() float64 {
	area := s.sideLength * s.sideLength
	return float64(area)
}

func printShape(s shape) {
	fmt.Println(s.getArea())
}
