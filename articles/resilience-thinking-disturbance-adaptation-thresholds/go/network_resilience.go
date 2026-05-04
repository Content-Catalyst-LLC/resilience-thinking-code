package main

import "fmt"

type Edge struct {
	From string
	To   string
}

func main() {
	edges := []Edge{
		{"Supplier A", "Factory 1"},
		{"Supplier B", "Factory 1"},
		{"Factory 1", "Distribution Hub"},
		{"Factory 2", "Distribution Hub"},
		{"Distribution Hub", "Region 1"},
		{"Distribution Hub", "Region 2"},
		{"Backup Supplier", "Factory 2"},
	}

	degree := map[string]int{}

	for _, edge := range edges {
		degree[edge.From]++
		degree[edge.To]++
	}

	fmt.Println("Network resilience degree diagnostics:")
	for node, value := range degree {
		fmt.Printf("%s: %d\n", node, value)
	}
}
