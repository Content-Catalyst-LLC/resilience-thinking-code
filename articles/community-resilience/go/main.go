package main

import "fmt"

type Strategy struct {
	Name                 string
	Value                float64
	ImplementationBurden float64
	EquityProtection     float64
	InfrastructureAccess float64
	InformationQuality   float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 8.10 && s.ImplementationBurden <= 3.0 {
		return "strong community resilience profile"
	}
	if s.ImplementationBurden >= 3.3 {
		return "implementation burden review needed"
	}
	if s.EquityProtection < 8.0 {
		return "equity protection needs strengthening"
	}
	if s.InfrastructureAccess < 7.4 {
		return "infrastructure access needs strengthening"
	}
	if s.InformationQuality < 7.6 {
		return "information and communication review needed"
	}
	return "promising but requires community scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Neighborhood Mutual Aid and Preparedness Network", 8.09, 2.7, 8.1, 7.1, 7.9},
		{"Inclusive Community Governance and Adaptation Forum", 8.18, 3.1, 8.8, 7.4, 7.8},
		{"Community Health and Care Continuity Network", 8.17, 3.0, 8.7, 7.8, 8.0},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
