package main

import "fmt"

type ServiceProfile struct {
	Service    string
	Flow       float64
	Resilience float64
	Access     float64
	Threshold  float64
}

func diagnostic(p ServiceProfile) string {
	if p.Flow >= 0.70 && p.Resilience < 0.55 {
		return "high current flow but weak resilience profile"
	}
	if p.Resilience >= 0.60 && p.Threshold >= 0.55 {
		return "stronger service-resilience profile"
	}
	if p.Access < 0.50 {
		return "equity and access concern"
	}
	return "mixed service-resilience profile"
}

func main() {
	profiles := []ServiceProfile{
		{"Pollination", 0.72, 0.49, 0.52, 0.48},
		{"Water Purification", 0.74, 0.62, 0.61, 0.62},
		{"Urban Cooling", 0.64, 0.48, 0.42, 0.49},
	}

	fmt.Println("service,current_service_flow,service_resilience_profile,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.4f,%.4f,%s\n", p.Service, p.Flow, p.Resilience, diagnostic(p))
	}
}
