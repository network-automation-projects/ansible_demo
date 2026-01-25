package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type IPResponse struct {
	IP string `json:"ip"`
}

func main() {
	resp, err := http.Get("https://api.ipify.org?format=json") // Fetch public IP as JSON
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer resp.Body.Close() // Don't forget to close the body

	body, err := io.ReadAll(resp.Body) // Read the response body
	if err != nil {
		fmt.Println("Error reading body:", err)
		return
	}

	fmt.Println(string(body)) // Print the JSON response

	//parse the json response to get the ip address
	var ip IPResponse
	err = json.Unmarshal(body, &ip) //so this pulls the ip itself from the json response.

	if err != nil {
		fmt.Println("Error unmarshalling JSON:", err)
		return
	}
	fmt.Println(ip.IP)
}
