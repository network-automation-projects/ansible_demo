package main

import "fmt"

type contactInfo struct {
	email string
	phone string
}

type person struct {
	firstName   string
	lastName    string
	contactInfo contactInfo // or contactInfo
}

func main() {
	joe := person{firstName: "Joe", lastName: "Doe"}
	fmt.Println(joe)

	var jane person
	fmt.Printf("%+v\n", jane)
	fmt.Println(jane)

	jane.updateName("Janet")

	//in order to update the original person, we need to pass a pointer to the person

	janePointer := &jane
	janePointer.updateName2("Janet Jackson")
	fmt.Printf("%+v\n", jane)

	//SHORTCUT
	jane.updateName2("Janet Jackson")
	fmt.Printf("%+v\n", jane)

	//gotcha: if you pass a pointer to a function, the function will receive a copy of the pointer, not the original pointer

}

func (p person) updateName(newFirstName string) {
	//update the person's first name to "Jane"
	p.firstName = newFirstName // this will update the function's local copy of the person, not the original person
	fmt.Printf("%+v\n", p)
}

func (pointerToPerson *person) updateName2(newFirstName string) {
	//update the person's first name to "Jane"
	pointerToPerson.firstName = newFirstName // this will update the actual person, not the original person
	//OR
	(*pointerToPerson).firstName = newFirstName // this will update the actual person, not the original person

	fmt.Printf("%+v\n", pointerToPerson)
}
