package main

import "fmt"

type Strategy struct {
	Name                 string
	Value                float64
	HumanSafeguards      float64
	Maintainability      float64
	Governance           float64
	VendorContingency    float64
	TechnicalDebtRisk    float64
	ImplementationBurden float64
}

func diagnostic(s Strategy) string {
	if s.ImplementationBurden >= 3.7 {
		return "implementation-burden review needed"
	}
	if s.TechnicalDebtRisk >= 3.3 {
		return "technical-debt review needed"
	}
	if s.HumanSafeguards < 8.1 {
		return "human-safeguards review needed"
	}
	if s.Maintainability < 8.1 {
		return "maintainability review needed"
	}
	if s.Governance < 8.3 {
		return "governance review needed"
	}
	if s.VendorContingency < 7.9 {
		return "vendor-contingency review needed"
	}
	return "promising but requires stress testing"
}

func main() {
	strategies := []Strategy{
		{"Cyber Recovery and Tested Backup Program", 7.90, 8.0, 8.1, 8.6, 7.9, 3.2, 3.5},
		{"Data Integrity and Lineage Governance", 7.88, 8.2, 8.2, 8.8, 7.8, 3.0, 3.4},
		{"Technical Debt and Maintainability Program", 7.82, 8.3, 9.2, 8.5, 7.8, 2.6, 3.7},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
