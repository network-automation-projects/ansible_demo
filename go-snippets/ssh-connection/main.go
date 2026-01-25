package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"golang.org/x/crypto/ssh"
)

func main() {
	// Step 1: Fetch public IP (from original)
	resp, err := http.Get("https://api.ipify.org?format=text")
	if err != nil {
		fmt.Println("Error fetching IP:", err)
		return
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading body:", err)
		return
	}
	publicIP := string(body)
	fmt.Printf("Public IP: %s\n", publicIP)

	// Step 2: SSH connection to Nokia SR Linux router
	// Option 1: Containerlab hostname (e.g., clab-mcp-nethealth-chatbot-router1:22)
	// Option 2: Localhost with port forwarding (e.g., localhost:2221)
	host := "localhost:2221"
	if len(os.Args) > 1 {
		host = os.Args[1] // Allow host to be passed as argument
		//so this pulls the ip address better than unmarshalling the json response
	}

	user := "admin"
	pass := "NokiaSrl1!"

	config := &ssh.ClientConfig{
		User: user,
		Auth: []ssh.AuthMethod{
			ssh.Password(pass),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(), // For testing; use known_hosts in prod
		Timeout:         10 * time.Second,
	}

	fmt.Printf("Connecting to Nokia SR Linux router at %s...\n", host)
	client, err := ssh.Dial("tcp", host, config)
	if err != nil {
		fmt.Printf("SSH dial error: %v\n", err)
		fmt.Println("Make sure the router is accessible and credentials are correct")
		return
	}
	defer client.Close()

	session, err := client.NewSession()
	if err != nil {
		fmt.Println("Session error:", err)
		return
	}
	defer session.Close()

	// Nokia SR Linux command (not 'show version')
	command := "show system information"
	if len(os.Args) > 2 {
		command = os.Args[2] // Allow custom command as second argument
	}

	fmt.Printf("Executing command: %s\n", command)
	output, err := session.CombinedOutput(command)
	if err != nil {
		fmt.Printf("Command error: %v\n", err)
		fmt.Println("Output (if any):")
		fmt.Println(string(output))
		return
	}

	fmt.Println("\n=== Nokia SR Linux Router Output ===")
	fmt.Println(string(output))
}
