package main

import (
	"flag"
	"fmt"
	"os"

	"inventory-drift-detector/internal/compare"
	"inventory-drift-detector/internal/inventory"
	"inventory-drift-detector/internal/report"
	"inventory-drift-detector/internal/ticket"
)

func main() {
	// Define flags
	expectedPath := flag.String("expected", "", "Path to expected inventory file (JSON or YAML)")
	actualPath := flag.String("actual", "", "Path to actual inventory file (JSON or YAML)")
	keyField := flag.String("key", "hostname", "Unique key field for comparison (default: hostname)")
	outputFormat := flag.String("output", "human", "Output format: human, json, or both (default: human)")
	jsonOutputPath := flag.String("json-output", "", "Path to save JSON diff file (optional)")
	createTicket := flag.Bool("ticket", false, "Create a mock ticket for drift (flag)")
	verbose := flag.Bool("verbose", false, "Enable verbose logging")

	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Usage: %s [options]\n\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "Compare two inventory files and report drift.\n\n")
		fmt.Fprintf(os.Stderr, "Options:\n")
		flag.PrintDefaults()
	}

	flag.Parse()

	// Validate required flags
	if *expectedPath == "" {
		fmt.Fprintf(os.Stderr, "Error: --expected flag is required\n\n")
		flag.Usage()
		os.Exit(1)
	}

	if *actualPath == "" {
		fmt.Fprintf(os.Stderr, "Error: --actual flag is required\n\n")
		flag.Usage()
		os.Exit(1)
	}

	// Validate file paths exist
	if _, err := os.Stat(*expectedPath); os.IsNotExist(err) {
		fmt.Fprintf(os.Stderr, "Error: expected inventory file not found: %s\n", *expectedPath)
		os.Exit(1)
	}

	if _, err := os.Stat(*actualPath); os.IsNotExist(err) {
		fmt.Fprintf(os.Stderr, "Error: actual inventory file not found: %s\n", *actualPath)
		os.Exit(1)
	}

	// Load inventories
	if *verbose {
		fmt.Printf("Loading expected inventory from: %s\n", *expectedPath)
	}
	expectedInv, err := inventory.LoadInventory(*expectedPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error loading expected inventory: %v\n", err)
		os.Exit(1)
	}

	if *verbose {
		fmt.Printf("Loading actual inventory from: %s\n", *actualPath)
	}
	actualInv, err := inventory.LoadInventory(*actualPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error loading actual inventory: %v\n", err)
		os.Exit(1)
	}

	if *verbose {
		fmt.Printf("Expected inventory: %d devices\n", len(expectedInv.Devices))
		fmt.Printf("Actual inventory: %d devices\n", len(actualInv.Devices))
		fmt.Printf("Using key field: %s\n", *keyField)
	}

	// Compare inventories
	if *verbose {
		fmt.Println("Comparing inventories...")
	}
	result, err := compare.Compare(expectedInv, actualInv, *keyField)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error comparing inventories: %v\n", err)
		os.Exit(1)
	}

	// Output results
	switch *outputFormat {
	case "human":
		fmt.Print(report.FormatHuman(result))
	case "json":
		jsonData, err := report.FormatJSON(result)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error formatting JSON: %v\n", err)
			os.Exit(1)
		}
		fmt.Println(string(jsonData))
	case "both":
		fmt.Print(report.FormatHuman(result))
		fmt.Println("\n--- JSON Output ---\n")
		jsonData, err := report.FormatJSON(result)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error formatting JSON: %v\n", err)
			os.Exit(1)
		}
		fmt.Println(string(jsonData))
	default:
		fmt.Fprintf(os.Stderr, "Error: invalid output format '%s'. Use 'human', 'json', or 'both'\n", *outputFormat)
		os.Exit(1)
	}

	// Save JSON output to file if specified
	if *jsonOutputPath != "" {
		jsonData, err := report.FormatJSON(result)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error formatting JSON for file: %v\n", err)
			os.Exit(1)
		}
		err = os.WriteFile(*jsonOutputPath, jsonData, 0644)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error writing JSON output to file: %v\n", err)
			os.Exit(1)
		}
		if *verbose {
			fmt.Printf("JSON output written to: %s\n", *jsonOutputPath)
		}
	}

	// Create mock ticket if requested
	if *createTicket {
		if result.HasDrift() {
			ticket, err := ticket.CreateTicket(result)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error creating ticket: %v\n", err)
				os.Exit(1)
			}
			fmt.Printf("\n--- Mock Ticket Created ---\n")
			fmt.Printf("Ticket ID:     %s\n", ticket.ID)
			fmt.Printf("Title:         %s\n", ticket.Title)
			fmt.Printf("Status:        %s\n", ticket.Status)
			fmt.Printf("Created At:    %s\n", ticket.CreatedAt.Format("2006-01-02 15:04:05"))
			fmt.Printf("\nDescription:\n%s\n", ticket.Description)
		} else {
			fmt.Println("\nNo drift detected, skipping ticket creation.")
		}
	}

	// Exit with code 0 if no drift, 1 if drift detected
	if result.HasDrift() {
		os.Exit(1)
	}
	os.Exit(0)
}
