package main

import "fmt"

type Pathway struct {
	Name                 string
	Value                float64
	ResourcePressure     float64
	SocialInclusion      float64
	EcologicalIntegrity  float64
	GovernanceCapacity   float64
	ImplementationBurden float64
}

func diagnostic(p Pathway) string {
	if p.ResourcePressure >= 4.2 {
		return "resource-pressure review needed"
	}
	if p.SocialInclusion < 8.0 {
		return "social-inclusion safeguards need strengthening"
	}
	if p.EcologicalIntegrity < 8.0 {
		return "ecological-integrity safeguards need strengthening"
	}
	if p.GovernanceCapacity < 8.0 {
		return "governance-capacity review needed"
	}
	if p.ImplementationBurden >= 3.6 {
		return "implementation-burden review needed"
	}
	if p.Value >= 8.0 {
		return "strong sustainable resilience pathway candidate"
	}
	return "promising but requires scenario validation"
}

func main() {
	pathways := []Pathway{
		{"Distributed Renewable Infrastructure", 7.90, 4.0, 7.8, 8.2, 7.8, 3.5},
		{"Climate-Resilient Food and Water Strategy", 8.21, 3.9, 8.1, 8.4, 8.1, 3.4},
		{"Ecosystem Restoration and Livelihood Diversification", 8.25, 3.5, 8.2, 9.0, 8.0, 3.2},
	}

	fmt.Println("pathway,value,diagnostic")
	for _, p := range pathways {
		fmt.Printf("%s,%.5f,%s\n", p.Name, p.Value, diagnostic(p))
	}
}
