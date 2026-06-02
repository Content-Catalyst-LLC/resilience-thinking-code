package main

import "fmt"

type Strategy struct {
	Name                   string
	Value                  float64
	ImplementationBurden   float64
	EquityProtection       float64
	InstitutionalCapacity  float64
	Transformability       float64
	Resistance             float64
}

func diagnostic(s Strategy) string {
	if s.ImplementationBurden >= 3.6 {
		return "implementation-burden review needed"
	}
	if s.EquityProtection < 8.0 {
		return "equity safeguards need strengthening"
	}
	if s.InstitutionalCapacity < 8.0 {
		return "institutional-capacity review needed"
	}
	if s.Transformability < 7.8 {
		return "transformation pathway review needed"
	}
	if s.Resistance < 7.8 {
		return "resistance-capacity review needed"
	}
	return "promising but requires scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Industrial Diversification and Local Production Program", 8.18, 3.5, 8.1, 8.2, 8.4, 8.0},
		{"Countercyclical Stabilization and Public Investment Framework", 8.38, 3.4, 8.3, 8.8, 8.0, 8.5},
		{"Community Finance and Small Business Continuity Fund", 8.25, 2.9, 8.7, 8.2, 7.9, 8.1},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
