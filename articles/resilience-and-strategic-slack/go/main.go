package main

import "fmt"

type Portfolio struct {
	Name                   string
	Value                  float64
	WorkforceSlack         float64
	KnowledgeSlack         float64
	GovernanceSlack        float64
	EthicalBurden          float64
	ImplementationBurden   float64
}

func diagnostic(p Portfolio) string {
	if p.ImplementationBurden >= 3.6 {
		return "implementation-burden review needed"
	}
	if p.EthicalBurden >= 3.2 {
		return "ethical-burden review needed"
	}
	if p.WorkforceSlack < 7.6 {
		return "workforce-slack review needed"
	}
	if p.KnowledgeSlack < 7.6 {
		return "knowledge-slack review needed"
	}
	if p.GovernanceSlack < 7.8 {
		return "governance-slack review needed"
	}
	return "promising but requires scenario testing"
}

func main() {
	portfolios := []Portfolio{
		{"Workforce Depth and Recovery Time", 7.64, 9.2, 8.0, 8.2, 2.6, 3.4},
		{"Knowledge Architecture and Institutional Memory", 7.58, 8.0, 9.3, 8.5, 2.9, 3.3},
		{"Adaptive Governance and Emergency Decision Space", 7.72, 8.1, 8.4, 9.1, 2.8, 3.2},
	}

	fmt.Println("portfolio,value,diagnostic")
	for _, p := range portfolios {
		fmt.Printf("%s,%.5f,%s\n", p.Name, p.Value, diagnostic(p))
	}
}
