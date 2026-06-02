package main

import "fmt"

type Profile struct {
	Name       string
	Systems    float64
	Resilience float64
}

func diagnostic(systems, resilience float64) string {
	if systems < 0.55 && resilience < 0.55 {
		return "weak structure visibility and weak resilience capacity"
	}
	if systems >= 0.65 && resilience >= 0.65 {
		return "strong structural understanding and resilience capacity"
	}
	if systems > resilience {
		return "structure visible but resilience capacity needs strengthening"
	}
	return "resilience capacity exists but structure needs clearer mapping"
}

func main() {
	profiles := []Profile{
		{"Watershed Governance", 0.66, 0.62},
		{"Supply Chain Network", 0.45, 0.39},
		{"Community Adaptation System", 0.74, 0.70},
	}

	fmt.Println("system_type,systems_score,resilience_score,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.4f,%.4f,%s\n", p.Name, p.Systems, p.Resilience, diagnostic(p.Systems, p.Resilience))
	}
}
