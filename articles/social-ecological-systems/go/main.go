package main

import "fmt"

type Profile struct {
	Name          string
	Resilience    float64
	Vulnerability float64
	Governance    float64
}

func diagnostic(p Profile) string {
	if p.Resilience >= 0.52 && p.Vulnerability < 0.55 {
		return "stronger SES resilience profile"
	}
	if p.Vulnerability >= 0.66 {
		return "high coupled vulnerability"
	}
	if p.Governance < 0.58 {
		return "governance capacity concern"
	}
	return "mixed SES resilience profile"
}

func main() {
	profiles := []Profile{
		{"Fishery", 0.432, 0.675, 0.61},
		{"Forest Commons", 0.552, 0.520, 0.72},
		{"Urban Watershed", 0.420, 0.642, 0.54},
	}

	fmt.Println("system_type,ses_resilience_profile,coupled_vulnerability,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.4f,%.4f,%s\n", p.Name, p.Resilience, p.Vulnerability, diagnostic(p))
	}
}
