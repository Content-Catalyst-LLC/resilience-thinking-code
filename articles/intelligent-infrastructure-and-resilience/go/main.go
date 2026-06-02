package main

import "fmt"

type Strategy struct {
	Name                 string
	Value                float64
	GovernanceQuality    float64
	EquityPerformance    float64
	CyberPhysicalSecurity float64
	PredictiveMaintenance float64
	FragilityRisk         float64
	ImplementationBurden  float64
}

func diagnostic(s Strategy) string {
	if s.ImplementationBurden >= 3.9 {
		return "implementation-burden review needed"
	}
	if s.FragilityRisk >= 3.1 {
		return "hidden-fragility review needed"
	}
	if s.EquityPerformance < 8.1 {
		return "equity-performance review needed"
	}
	if s.GovernanceQuality < 8.3 {
		return "governance review needed"
	}
	if s.CyberPhysicalSecurity < 8.1 {
		return "cyber-physical security review needed"
	}
	if s.PredictiveMaintenance < 8.1 {
		return "maintenance-capacity review needed"
	}
	return "promising but requires field validation"
}

func main() {
	strategies := []Strategy{
		{"Predictive Maintenance and Asset Renewal", 7.91, 8.4, 8.2, 8.2, 9.3, 2.8, 3.8},
		{"Cyber-Physical Security and Recovery Program", 7.85, 8.7, 8.0, 9.4, 8.0, 2.7, 3.7},
		{"Equity-Centered Climate Adaptation Portfolio", 8.15, 8.9, 9.3, 8.0, 8.1, 2.6, 3.9},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
