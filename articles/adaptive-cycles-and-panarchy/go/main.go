package main

import "fmt"

type CycleProfile struct {
	System       string
	Phase        string
	ReleaseRisk float64
	Renewal      float64
}

func diagnostic(p CycleProfile) string {
	if p.Phase == "K" && p.ReleaseRisk >= 0.62 {
		return "conservation-phase brittleness concern"
	}
	if p.Phase == "alpha" && p.Renewal >= 0.58 {
		return "strong reorganization potential"
	}
	if p.Phase == "r" && p.Renewal >= 0.55 {
		return "high experimentation and growth potential"
	}
	return "mixed adaptive-cycle profile"
}

func main() {
	profiles := []CycleProfile{
		{"Urban Stormwater System", "K", 0.71, 0.41},
		{"Wetland Restoration Program", "alpha", 0.38, 0.66},
		{"Community Recovery Network", "r", 0.42, 0.59},
	}

	fmt.Println("system,phase,release_risk,renewal_potential,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%s,%.4f,%.4f,%s\n", p.System, p.Phase, p.ReleaseRisk, p.Renewal, diagnostic(p))
	}
}
