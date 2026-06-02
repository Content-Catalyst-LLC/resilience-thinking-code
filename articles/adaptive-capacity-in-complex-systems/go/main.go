package main

import "fmt"

type AdaptiveProfile struct {
	System        string
	Capacity      float64
	Vulnerability float64
	Rigidity      float64
}

func diagnostic(p AdaptiveProfile) string {
	if p.Capacity >= 0.58 && p.Vulnerability < 0.55 {
		return "stronger adaptive-capacity profile"
	}
	if p.Vulnerability >= 0.66 {
		return "high adaptive-vulnerability concern"
	}
	if p.Rigidity >= 0.62 {
		return "rigidity and lock-in concern"
	}
	return "mixed adaptive-capacity profile"
}

func main() {
	profiles := []AdaptiveProfile{
		{"Ecological System", 0.590, 0.510, 0.34},
		{"Infrastructure System", 0.420, 0.690, 0.66},
		{"Regional Food System", 0.500, 0.640, 0.55},
	}

	fmt.Println("system_type,adaptive_capacity,adaptive_vulnerability,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.4f,%.4f,%s\n", p.System, p.Capacity, p.Vulnerability, diagnostic(p))
	}
}
