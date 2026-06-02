package main

import "fmt"

type Strategy struct {
	Name                  string
	Value                 float64
	ResourceDepletionRisk float64
	Access                float64
	Quality               float64
	EquityProtection      float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 7.75 && s.ResourceDepletionRisk <= 2.9 {
		return "strong food-water resilience profile"
	}
	if s.ResourceDepletionRisk >= 3.5 {
		return "resource depletion review needed"
	}
	if s.Access < 7.8 {
		return "access protection needs strengthening"
	}
	if s.Quality < 7.8 {
		return "quality and safety review needed"
	}
	if s.EquityProtection < 7.8 {
		return "equity protection needs strengthening"
	}
	return "promising but requires food-water scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Climate-Smart Irrigation Upgrade", 7.75, 3.7, 7.5, 7.8, 7.4},
		{"Community Water Governance and Access Reform", 8.16, 2.8, 8.8, 8.1, 8.9},
		{"Safe Water Treatment and Sanitation Resilience Plan", 8.14, 3.0, 8.5, 8.9, 8.6},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
