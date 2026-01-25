# Setup and Usage Instructions - SSH - Connection 

Complete step-by-step guide to get started with the Go Network Monitor and Prometheus setup.

---

## Prerequisites
To use it, you'll need to:

Initialize a Go module (if not already): 
go mod init ssh-connection

Install dependencies: 
go get golang.org/x/crypto/ssh
The code is ready to connect to your Nokia routers from the containerlab projects.

or let go do discovery and install automatically by running:
go mod tidy

start the Nokia (or other device) services:
option1:

Navigate to the project:
   cd mcp_networkc/mcp_nethealth_chatbot
Deploy the containerlab topology:
   clab deploy -t topology.yml
Verify routers are running:
   docker ps | grep router
You should see:
clab-mcp-nethealth-chatbot-router1
clab-mcp-nethealth-chatbot-router2



## The code now supports:
Default usage: go run main.go (connects to localhost:2221, runs "show system information")
Custom host: go run main.go localhost:2222
Custom host and command: go run main.go clab-mcp-nethealth-chatbot-router1:22 "show version"
