package main

import "fmt"

type Strategy struct {
	Name                         string
	Value                        float64
	ImplementationBurden         float64
	KnowledgeProtection          float64
	DecisionInfluence            float64
	ParticipationAccess          float64
	ImplementationAccountability float64
}

func diagnostic(s Strategy) string {
	if s.ImplementationBurden >= 3.5 {
		return "implementation-burden review needed"
	}
	if s.KnowledgeProtection < 8.2 {
		return "knowledge-protection safeguards need strengthening"
	}
	if s.DecisionInfluence < 8.0 {
		return "decision-influence review needed"
	}
	if s.ParticipationAccess < 8.2 {
		return "participation-access review needed"
	}
	if s.ImplementationAccountability < 8.2 {
		return "implementation-accountability review needed"
	}
	return "promising but requires community validation"
}

func main() {
	strategies := []Strategy{
		{"Participatory Risk Mapping and Action Triggers", 8.42, 3.2, 8.0, 8.4, 8.7, 8.5},
		{"Indigenous Knowledge Governance Protocol", 8.80, 3.5, 9.4, 8.8, 8.4, 8.7},
		{"Funded Community Resilience Advisory Council", 8.79, 3.3, 8.5, 9.1, 9.0, 9.0},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
