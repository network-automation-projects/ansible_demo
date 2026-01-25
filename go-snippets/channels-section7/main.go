package main

import (
	"fmt"
	"net/http"
	"time"
)

//let's use channels to make this more efficient

func main() {
	links := []string{
		"http://google.com",
		"http://facebook.com",
		"http://stackoverflow.com",
		"http://golang.org",
		"http://amazon.com",
	}
	//byte slice or string slice are like arrays, but more flexible
	//

	c := make(chan string)

	for _, link := range links {
		go checkLink(link, c) //this will start the checklink
		//process each time on a new goroutine
		//however, it doesn't wait for the checkLink to finish
		//so the main func will exit without waiting for responses.
	}

	//fmt.Println(<-c)  //this becomes a blocking line of code.
	//main will wait for the routine to return a value before it moves
	//to other lines of code below this one.

	// for i := 0; i < len(links); i++ {  //this will only run len(links) times
	// 	fmt.Println(<-c)
	// }

	// for { //this will run infinitely to keep checking links
	// 	time.Sleep(5 * time.Second) //wait 5 seconds between checks
	// 	//this is actually a terrible place to put this code.
	// 	//it is inside the main routine, so it will block
	// 	//the main routine from receiving values from the channel
	// 	go checkLink(<-c, c)        //this will wait for a value from the channel
	// }

	// for link := range c { //this is just clearer syntax
	// 	go checkLink(link, c) //this will wait for a value from the channel
	// }

	// for link := range c { //this is just clearer syntax
	// 	go func() {
	// 		time.Sleep(5 * time.Second) //wait 5 seconds between checks
	// 		checkLink(link, c)
	// 	}()
	// 	//this will wait for a value from the channel
	// 	//this version is using the function literal to add the sleep
	// 	//since it doesn't really belong inside checkLink
	// }
	//this one doesn't pass link properly,
	//the child routine should never rely on a variable from the parent routine
	//that hasn't been passed in as a parameter

	for link := range c { //this is just clearer syntax
		go func(llink string) {
			time.Sleep(5 * time.Second) //wait 5 seconds between checks
			checkLink(llink, c)
		}(link)
		//this will wait for a value from the channel
		//this version is using the function literal to add the sleep
		//since it doesn't really belong inside checkLink
	}

}

func checkLink(link string, c chan string) {
	//time.Sleep(5 * time.Second) //wait 5 seconds between checks
	//moved into function literal above

	resp, err := http.Get(link)
	if err != nil {
		fmt.Println(link, "might be down!", err)
		c <- link //send link back to channel c
		return
	}
	fmt.Println(link, "is up!", resp.StatusCode)
	c <- link
}

//this way forces us to wait for each to be checked before
//moving on to the next one

// func main() {
// 	links := []string{
// 		"http://google.com",
// 		"http://facebook.com",
// 		"http://stackoverflow.com",
// 		"http://golang.org",
// 		"http://amazon.com",
// 	}
// 	for _, link := range links {
// 		go checkLink(link)
// 	}
// }

// func checkLink(link string) {
// 	resp, err := http.Get(link)
// 	if err != nil {
// 		fmt.Println(link, "might be down!", err)
// 		return
// 	}
// 	fmt.Println(link, "is up!", resp.StatusCode)
// }
