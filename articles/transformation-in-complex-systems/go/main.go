package main

import "fmt"

type Pathway struct {
	Name          string
	Readiness     float64
	Justice       float64
	Governance    float64
	StructuralRisk float64
}

func diagnostic(p Pathway) string {
	if p.Readiness >= 7.55 && p.StructuralRisk <= 4.1 {
		return "high readiness with manageable structural risk"
	}
	if p.Justice < 7.5 {
		return "justice contribution needs stronger design"
	}
	if p.Governance < 7.4 {
		return "governance readiness constraint"
	}
	return "promising but requires participatory validation"
}

func main() {
	pathways := []Pathway{
		{"Climate-Resilient Urban Redesign", 7.86, 8.4, 7.8, 4.0},
		{"Institutional Governance Reform", 7.72, 8.2, 8.4, 4.1},
		{"Energy System Transition", 7.62, 7.1, 7.4, 4.2},
	}

	fmt.Println("pathway,readiness,diagnostic")
	for _, p := range pathways {
		fmt.Printf("%s,%.5f,%s\n", p.Name, p.Readiness, diagnostic(p))
	}
}
