package main

import (
	"fmt"
	"math"
)

type Node struct {
	Name       string
	Capacity   float64
	Dependency []int
}

func networkViability(nodes []Node, failed map[int]bool) float64 {
	total := 0.0
	available := 0.0

	for i, node := range nodes {
		total += node.Capacity
		if failed[i] {
			continue
		}

		dependencyPenalty := 0.0
		for _, dep := range node.Dependency {
			if failed[dep] {
				dependencyPenalty += 0.20
			}
		}

		available += node.Capacity * math.Max(0.0, 1.0-dependencyPenalty)
	}

	if total == 0 {
		return 0
	}
	return available / total
}

func main() {
	nodes := []Node{
		{"water", 0.25, []int{1, 2}},
		{"power", 0.30, []int{2}},
		{"transport", 0.20, []int{}},
		{"health", 0.25, []int{0, 1}},
	}

	failed := map[int]bool{1: true}
	viability := networkViability(nodes, failed)

	fmt.Printf("network_viability=%.4f\n", viability)
	if viability < 0.70 {
		fmt.Println("diagnostic=dependency concentration requires resilience review")
	} else {
		fmt.Println("diagnostic=network retains acceptable synthetic viability")
	}
}
