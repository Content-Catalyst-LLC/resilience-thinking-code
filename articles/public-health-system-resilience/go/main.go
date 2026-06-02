package main

import "fmt"

type Strategy struct {
	Name                 string
	Value                float64
	ImplementationBurden float64
	Trust                float64
	EquityProtection     float64
	ServiceContinuity    float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 8.15 && s.ImplementationBurden <= 3.0 {
		return "strong public health resilience profile"
	}
	if s.ImplementationBurden >= 3.5 {
		return "implementation burden review needed"
	}
	if s.Trust < 7.8 {
		return "trust and communication review needed"
	}
	if s.EquityProtection < 8.0 {
		return "equity protection needs strengthening"
	}
	if s.ServiceContinuity < 8.0 {
		return "service continuity needs strengthening"
	}
	return "promising but requires public health scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Integrated Surveillance and Laboratory Modernization", 8.02, 3.5, 7.5, 7.7, 7.9},
		{"Community Health Trust and Outreach Network", 8.36, 2.8, 9.0, 8.9, 8.1},
		{"Equity-Centered Emergency Preparedness Framework", 8.48, 3.0, 8.7, 9.1, 8.2},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
