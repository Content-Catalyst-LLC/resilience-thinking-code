package main

import "fmt"

type Strategy struct {
	Name              string
	Value             float64
	CascadingExposure float64
	EquityProtection  float64
	Redundancy        float64
	AdaptiveCapacity  float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 7.45 && s.CascadingExposure <= 3.6 {
		return "strong infrastructure resilience profile"
	}
	if s.CascadingExposure >= 4.0 {
		return "cascade review needed"
	}
	if s.EquityProtection < 7.8 {
		return "equity protection needs strengthening"
	}
	if s.Redundancy < 7.8 {
		return "redundancy constraint"
	}
	if s.AdaptiveCapacity < 8.0 {
		return "adaptive capacity constraint"
	}
	return "promising but requires infrastructure scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Grid Redundancy and Microgrid Expansion", 7.78, 3.9, 7.8, 8.9, 8.2},
		{"Flood-Resilient Transport Retrofit Program", 7.28, 4.1, 7.6, 7.6, 7.9},
		{"Equitable Critical Service Restoration Program", 7.79, 3.4, 8.9, 8.0, 8.1},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
