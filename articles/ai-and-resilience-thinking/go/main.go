package main

import "fmt"

type Strategy struct {
	Name                 string
	Value                float64
	GovernanceQuality    float64
	EquitySafeguards     float64
	HumanOversight       float64
	LocalKnowledge       float64
	AIRisk               float64
	ImplementationBurden float64
}

func diagnostic(s Strategy) string {
	if s.ImplementationBurden >= 3.8 {
		return "implementation-burden review needed"
	}
	if s.AIRisk >= 3.2 {
		return "AI-risk review needed"
	}
	if s.EquitySafeguards < 8.0 {
		return "equity-safeguards review needed"
	}
	if s.HumanOversight < 8.1 {
		return "human-oversight review needed"
	}
	if s.LocalKnowledge < 8.0 {
		return "local-knowledge review needed"
	}
	if s.GovernanceQuality < 8.1 {
		return "governance review needed"
	}
	return "promising but requires participatory validation"
}

func main() {
	strategies := []Strategy{
		{"AI Decision Support with Human Oversight", 7.88, 8.7, 8.4, 9.2, 8.2, 2.7, 3.4},
		{"Participatory AI and Local Knowledge Integration", 7.92, 8.6, 9.2, 9.1, 9.4, 2.6, 3.7},
		{"AI Governance Audit and Drift Monitoring", 8.02, 9.3, 8.8, 8.8, 8.4, 2.5, 3.8},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
