package main

import "fmt"

type FunctionProfile struct {
	Function    string
	Resilience  float64
	Redundancy  float64
	ResponseDiv float64
	Exposure    float64
}

func diagnostic(p FunctionProfile) string {
	if p.Resilience >= 0.58 && p.ResponseDiv >= 0.55 {
		return "stronger function-resilience profile"
	}
	if p.Redundancy < 0.50 || p.ResponseDiv < 0.50 {
		return "redundancy or response-diversity concern"
	}
	if p.Exposure >= 0.70 {
		return "high disturbance exposure"
	}
	return "mixed profile requiring monitoring"
}

func main() {
	profiles := []FunctionProfile{
		{"Pollination", 0.468, 0.52, 0.49, 0.72},
		{"Nutrient Cycling", 0.602, 0.66, 0.61, 0.56},
		{"Predation Regulation", 0.470, 0.48, 0.44, 0.64},
	}

	fmt.Println("ecosystem_function,functional_resilience_profile,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.4f,%s\n", p.Function, p.Resilience, diagnostic(p))
	}
}
