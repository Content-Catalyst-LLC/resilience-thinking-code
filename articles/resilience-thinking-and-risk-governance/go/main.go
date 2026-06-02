package main

import "fmt"

type Profile struct {
	Name       string
	Risk       float64
	Governance float64
	Margin     float64
}

func diagnostic(margin float64) string {
	if margin < 1.05 {
		return "high governance-resilience concern"
	}
	if margin < 1.45 {
		return "moderate governance-resilience concern"
	}
	return "stronger governance-resilience position"
}

func main() {
	profiles := []Profile{
		{"Coastal City", 0.2524, 0.4591, 0.6667},
		{"Watershed Governance", 0.1910, 0.6776, 1.3666},
		{"Community Adaptation Network", 0.1372, 0.7790, 1.7318},
	}

	fmt.Println("system_type,risk_pressure,governance_capacity,resilience_margin,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.4f,%.4f,%.4f,%s\n", p.Name, p.Risk, p.Governance, p.Margin, diagnostic(p.Margin))
	}
}
