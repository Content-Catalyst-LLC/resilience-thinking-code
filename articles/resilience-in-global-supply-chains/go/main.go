package main

import "fmt"

type Strategy struct {
	Name                     string
	Value                    float64
	ImplementationBurden     float64
	EquitySafeguards         float64
	InfrastructureContinuity  float64
	Visibility               float64
	Redundancy               float64
}

func diagnostic(s Strategy) string {
	if s.ImplementationBurden >= 3.7 {
		return "implementation-burden review needed"
	}
	if s.EquitySafeguards < 7.8 {
		return "equity and labor safeguards need strengthening"
	}
	if s.InfrastructureContinuity < 7.8 {
		return "infrastructure-continuity review needed"
	}
	if s.Visibility < 7.4 {
		return "visibility and dependency-mapping review needed"
	}
	if s.Redundancy < 7.4 {
		return "redundancy review needed"
	}
	return "promising but requires stress testing"
}

func main() {
	strategies := []Strategy{
		{"Supplier Diversification and Qualification Program", 6.93, 3.2, 7.9, 7.6, 7.6, 8.8},
		{"Multi-Route Logistics and Chokepoint Redesign", 7.03, 3.4, 7.8, 8.5, 8.0, 8.1},
		{"Fair Supplier Finance and Labor Continuity Program", 6.98, 3.0, 9.0, 7.6, 7.5, 7.7},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
