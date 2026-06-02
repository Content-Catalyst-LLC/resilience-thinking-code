package main

import "fmt"

type Strategy struct {
	Name          string
	Value         float64
	CommonMode    float64
	Coordination  float64
	Justice       float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 7.15 && s.CommonMode <= 3.6 {
		return "strong containment profile"
	}
	if s.CommonMode >= 4.0 {
		return "common-mode failure review needed"
	}
	if s.Coordination < 7.5 {
		return "coordination readiness constraint"
	}
	if s.Justice < 7.5 {
		return "justice protection needs strengthening"
	}
	return "promising but requires validation"
}

func main() {
	strategies := []Strategy{
		{"Microgrid and Critical Service Islanding", 7.54, 3.5, 7.6, 7.3},
		{"Cross-Agency Emergency Coordination Cells", 7.28, 4.0, 8.7, 7.5},
		{"Neighborhood Resilience Hub Network", 7.41, 3.7, 8.0, 8.6},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
