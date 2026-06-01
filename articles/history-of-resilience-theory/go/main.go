package main

import "fmt"

type Phase struct {
	Name                string
	Year                int
	ConceptualScope     float64
	GovernanceRelevance  float64
	SystemComplexity     float64
	JusticeRelevance     float64
}

func influenceScore(p Phase) float64 {
	return 0.35*p.ConceptualScope +
		0.25*p.GovernanceRelevance +
		0.25*p.SystemComplexity +
		0.15*p.JusticeRelevance
}

func main() {
	phases := []Phase{
		{"Holling 1973", 1973, 0.35, 0.18, 0.42, 0.08},
		{"Social-Ecological Systems", 2004, 0.78, 0.70, 0.86, 0.42},
		{"Critical Resilience and Justice", 2015, 0.96, 0.96, 0.96, 0.94},
	}

	fmt.Println("period,start_year,influence_score")
	for _, p := range phases {
		fmt.Printf("%s,%d,%.4f\n", p.Name, p.Year, influenceScore(p))
	}
}
