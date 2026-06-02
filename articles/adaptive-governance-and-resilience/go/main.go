package main

import "fmt"

type Strategy struct {
	Name                 string
	Value                float64
	ImplementationBurden float64
	EquityProtection     float64
	Legitimacy           float64
	Accountability       float64
	Flexibility          float64
	Coordination         float64
}

func diagnostic(s Strategy) string {
	if s.ImplementationBurden >= 3.5 {
		return "implementation-burden review needed"
	}
	if s.EquityProtection < 8.0 {
		return "equity safeguards need strengthening"
	}
	if s.Accountability < 8.0 && s.Flexibility >= 8.5 {
		return "flexibility-accountability review needed"
	}
	if s.Legitimacy < 8.0 {
		return "legitimacy and trust review needed"
	}
	if s.Coordination < 8.0 {
		return "coordination review needed"
	}
	return "promising but requires scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Adaptive Pathways and Decision Triggers", 8.18, 3.2, 7.8, 7.9, 8.0, 8.9, 7.9},
		{"Community Knowledge Co-Production Platform", 8.40, 3.1, 8.7, 8.8, 8.3, 7.6, 8.0},
		{"Equity Accountability and Rights Safeguard", 8.43, 3.0, 9.2, 8.7, 9.1, 7.7, 7.9},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
