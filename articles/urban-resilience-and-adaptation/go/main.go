package main

import "fmt"

type Strategy struct {
	Name                string
	Value               float64
	MaladaptationRisk   float64
	EquityProtection    float64
	EcologicalBuffering float64
	ServiceContinuity   float64
}

func diagnostic(s Strategy) string {
	if s.Value >= 7.75 && s.MaladaptationRisk <= 2.7 {
		return "strong urban resilience profile"
	}
	if s.MaladaptationRisk >= 3.4 {
		return "maladaptation review needed"
	}
	if s.EquityProtection < 8.0 {
		return "equity protection needs strengthening"
	}
	if s.EcologicalBuffering < 7.5 {
		return "ecological buffering needs strengthening"
	}
	if s.ServiceContinuity < 8.0 {
		return "service continuity needs strengthening"
	}
	return "promising but requires urban scenario validation"
}

func main() {
	strategies := []Strategy{
		{"Heat-Resilient Housing Retrofit Program", 7.92, 2.9, 8.6, 7.4, 8.1},
		{"Critical Service Microgrid and Water Backup Program", 7.69, 3.5, 7.8, 7.2, 8.8},
		{"Anti-Displacement Climate Adaptation Framework", 7.91, 2.5, 9.1, 7.5, 7.7},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
