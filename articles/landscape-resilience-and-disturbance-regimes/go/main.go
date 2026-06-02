package main

import "fmt"

type LandscapeProfile struct {
	Landscape  string
	Resilience float64
	Risk       float64
	Refugia    float64
	Memory     float64
}

func diagnostic(p LandscapeProfile) string {
	if p.Resilience >= 0.55 && p.Risk < 0.58 {
		return "stronger landscape-resilience profile"
	}
	if p.Risk >= 0.68 {
		return "high disturbance-regime risk"
	}
	if p.Refugia < 0.50 || p.Memory < 0.50 {
		return "refugia or ecological-memory concern"
	}
	return "mixed landscape-resilience profile"
}

func main() {
	profiles := []LandscapeProfile{
		{"Fire-Prone Forest Mosaic", 0.426, 0.585, 0.57, 0.62},
		{"Urban Watershed", 0.314, 0.704, 0.40, 0.42},
		{"River-Floodplain Landscape", 0.535, 0.528, 0.66, 0.70},
	}

	fmt.Println("landscape_type,landscape_resilience_profile,disturbance_risk_index,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.4f,%.4f,%s\n", p.Landscape, p.Resilience, p.Risk, diagnostic(p))
	}
}
