package main

import "fmt"

type Strategy struct {
	Name                 string
	Value                float64
	ImplementationBurden float64
	EquityProtection     float64
	Legitimacy           float64
	Capacity             float64
	Coordination         float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 8.10 && s.ImplementationBurden <= 3.0 {
		return "strong institutional resilience profile"
	}
	if s.ImplementationBurden >= 3.3 {
		return "implementation burden review needed"
	}
	if s.EquityProtection < 7.8 {
		return "equity protection needs strengthening"
	}
	if s.Legitimacy < 7.6 {
		return "legitimacy and trust review needed"
	}
	if s.Capacity < 7.5 {
		return "administrative capacity needs strengthening"
	}
	if s.Coordination < 7.6 {
		return "coordination review needed"
	}
	return "promising but requires institutional scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Public Trust and Transparency Initiative", 7.71, 2.8, 8.2, 8.9, 7.1, 7.2},
		{"Equity and Access Accountability Review", 8.18, 3.0, 9.1, 8.3, 7.5, 7.6},
		{"Institutional Learning and After-Action Implementation System", 8.27, 3.3, 8.1, 7.8, 8.0, 8.4},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
