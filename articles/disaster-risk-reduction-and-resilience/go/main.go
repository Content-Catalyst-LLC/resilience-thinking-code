package main

import "fmt"

type Strategy struct {
	Name              string
	Value             float64
	MaladaptationRisk float64
	JusticeProtection float64
	CapacityEnhancement float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 7.35 && s.MaladaptationRisk <= 2.7 {
		return "strong DRR and resilience profile"
	}
	if s.MaladaptationRisk >= 3.6 {
		return "maladaptation review needed"
	}
	if s.JusticeProtection < 7.5 {
		return "justice protection needs strengthening"
	}
	if s.CapacityEnhancement < 7.2 {
		return "capacity constraint"
	}
	return "promising but requires scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Community Early Warning Network", 7.63, 2.6, 8.0, 8.7},
		{"Critical Infrastructure Hardening", 7.05, 3.8, 7.1, 7.6},
		{"Equitable Recovery and Housing Protection Program", 7.72, 2.4, 9.0, 8.3},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
