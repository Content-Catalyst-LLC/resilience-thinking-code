package main

import "fmt"

type RegimeProfile struct {
	System     string
	Risk       float64
	Recovery   float64
	Monitoring float64
	Justice    float64
}

func diagnostic(p RegimeProfile) string {
	if p.Risk >= 0.55 {
		return "high regime-shift risk concern"
	}
	if p.Recovery < 0.38 {
		return "critical slowing and weak recovery concern"
	}
	if p.Monitoring < 0.50 {
		return "monitoring quality concern"
	}
	if p.Justice < 0.45 {
		return "unequal warning and justice visibility concern"
	}
	return "mixed regime profile"
}

func main() {
	profiles := []RegimeProfile{
		{"Urban Stormwater Service Regime", 0.57, 0.36, 0.52, 0.46},
		{"Institutional Legitimacy Regime", 0.56, 0.32, 0.50, 0.42},
		{"Coral Reef Community Regime", 0.60, 0.34, 0.54, 0.48},
	}

	fmt.Println("system,regime_risk,recovery_speed,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.5f,%.5f,%s\n", p.System, p.Risk, p.Recovery, diagnostic(p))
	}
}
