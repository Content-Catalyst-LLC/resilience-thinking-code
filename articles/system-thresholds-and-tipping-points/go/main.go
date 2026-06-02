package main

import "fmt"

type ThresholdProfile struct {
	System     string
	Risk       float64
	Protection float64
	Feedback   float64
	Recovery   float64
}

func diagnostic(p ThresholdProfile) string {
	if p.Risk >= 0.55 {
		return "high threshold-risk concern"
	}
	if p.Recovery < 0.38 {
		return "low recovery-speed concern"
	}
	if p.Feedback >= 0.72 {
		return "feedback amplification concern"
	}
	return "mixed threshold profile"
}

func main() {
	profiles := []ThresholdProfile{
		{"Urban Stormwater Network", 0.572, 0.388, 0.66, 0.36},
		{"Institutional Legitimacy System", 0.548, 0.402, 0.74, 0.32},
		{"Shallow Lake Nutrient System", 0.536, 0.430, 0.72, 0.42},
	}

	fmt.Println("system,threshold_risk,threshold_protection,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.4f,%.4f,%s\n", p.System, p.Risk, p.Protection, diagnostic(p))
	}
}
