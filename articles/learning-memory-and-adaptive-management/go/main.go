package main

import "fmt"

type Strategy struct {
	Name              string
	Value             float64
	ForgettingPressure float64
	FeedbackUse       float64
	JusticeProtection float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 7.2 && s.ForgettingPressure <= 3.1 {
		return "strong adaptive-learning profile"
	}
	if s.ForgettingPressure >= 3.5 {
		return "forgetting-pressure review needed"
	}
	if s.FeedbackUse < 8.0 {
		return "feedback-use constraint"
	}
	if s.JusticeProtection < 7.5 {
		return "justice protection needs strengthening"
	}
	return "promising but requires validation"
}

func main() {
	strategies := []Strategy{
		{"Institutional After-Action Learning System", 7.42, 3.0, 8.3, 7.8},
		{"Community Knowledge and Early Warning Network", 7.51, 2.8, 8.0, 8.8},
		{"Safe-to-Fail Climate Adaptation Pilots", 7.19, 3.5, 7.9, 8.3},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
