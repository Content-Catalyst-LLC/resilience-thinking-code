package main

import "fmt"

type Strategy struct {
	Name       string
	Value      float64
	CommonMode float64
	Coordination float64
	Justice    float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 7.25 && s.CommonMode <= 3.7 {
		return "strong diverse-redundancy profile"
	}
	if s.CommonMode >= 4.0 {
		return "common-mode failure review needed"
	}
	if s.Coordination < 7.5 {
		return "coordination and interoperability constraint"
	}
	if s.Justice < 7.6 {
		return "justice contribution needs stronger design"
	}
	return "promising but requires stress testing"
}

func main() {
	strategies := []Strategy{
		{"Distributed Backup Infrastructure Network", 7.47, 3.8, 7.6, 7.2},
		{"Multi-Supplier and Multi-Technology System Design", 7.64, 3.5, 7.3, 7.4},
		{"Public Health Community Surge Network", 7.72, 3.6, 7.9, 8.4},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
