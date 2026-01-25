package main

import (
	"io"
	"log"
	"os"
)

type logWriter struct{}

//this is less efficient than using io.Copy, but it's a good example of how to implement the io.Writer interface
//Problems:
// Loads the entire file into RAM
// For a 100MB file, it uses 100MB of memory
// If the file is 1GB, your program might crash or run very slowly

func (logWriter) Write(byte_slice []byte) (int, error) {
	//because we associated logWriter with the Write funciton,
	//it is now an io.Writer

	log.Println(string(byte_slice))
	log.Println("Just wrote this many bytes:", len(byte_slice))
	return len(byte_slice), nil
}

func main() {
	//filename := os.Args[0] //nope, it's the element at 1 that is the filename
	filename := os.Args[1]

	// data, err := os.ReadFile(filename)
	// if err != nil {
	// 	log.Fatal(err)
	// 	os.Exit(1)
	// }

	// lw := logWriter{}
	// io.Copy(lw, data)

	file_data, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	}

	io.Copy(os.Stdout, file_data)

}
