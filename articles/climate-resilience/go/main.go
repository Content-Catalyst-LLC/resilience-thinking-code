package main

import "fmt"

type Strategy struct {
	Name              string
	Value             float64
	MaladaptationRisk float64
	JusticeProtection float64
	AdaptiveCapacity  float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 7.35 && s.MaladaptationRisk <= 3.1 {
		return "strong climate resilience profile"
	}
	if s.MaladaptationRisk >= 3.7 {
		return "maladaptation review needed"
	}
	if s.JusticeProtection < 7.8 {
		return "justice protection needs strengthening"
	}
	if s.AdaptiveCapacity < 8.0 {
		return "adaptive capacity constraint"
	}
	return "promising but requires scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Community-Led Floodplain Adaptation", 7.62, 2.8, 8.8, 8.2},
		{"Distributed Energy and Critical Service Microgrids", 7.22, 3.8, 7.6, 8.0},
		{"Integrated Climate Risk Governance Framework", 7.51, 3.2, 8.1, 8.7},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
