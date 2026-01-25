package main

import (
	"io"
	"log"
	"net/http"
	"os"
)

type logWriter struct{}

func (logWriter) Write(byte_slice []byte) (int, error) {
	//because we associated logWriter with the Write funciton,
	//it is now an io.Writer

	log.Println(string(byte_slice))
	log.Println("Just wrote this many bytes:", len(byte_slice))
	return len(byte_slice), nil
}

func main() {

	resp, err := http.Get("https://www.google.com")
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	}

	byte_slice := make([]byte, 99999) //making a byte slice
	//because the response body is an io.Reader, with
	// the Read method that requires a byte slice as an argument
	// and we can read it into a byte slice
	//we use 99999 as the size of the byte slice
	//because the response body is usually less than 99999 bytes

	resp.Body.Read(byte_slice)
	log.Println(string(byte_slice))

	// OR
	//io.Copy(os.Stdout, resp.Body)

	lw := logWriter{}
	io.Copy(lw, resp.Body) //we can legally pass in
	//lw as an io.Writer to io.Copy because it
	//implements the io.Writer interface (Write method above)

	// defer resp.Body.Close()
	// body, err := io.ReadAll(resp.Body)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// fmt.Println(string(body))

	//write our own custom type the implements the io.Writer
	//  interface

	//and pass that to io.Copy
	//by associating the custom type with the io.Writer interface

}
