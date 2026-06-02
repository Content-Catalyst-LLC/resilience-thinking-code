package main

import "fmt"

type SlowVariableProfile struct {
	System    string
	Risk      float64
	Distance  float64
	Monitoring float64
	Justice    float64
}

func diagnostic(p SlowVariableProfile) string {
	if p.Risk >= 0.58 && p.Distance <= 0.45 {
		return "high hidden-risk and narrowing threshold-distance concern"
	}
	if p.Monitoring < 0.50 {
		return "monitoring and signal-quality concern"
	}
	if p.Justice < 0.45 {
		return "justice visibility and slow-harm concern"
	}
	return "mixed slow-variable profile"
}

func main() {
	profiles := []SlowVariableProfile{
		{"Urban Stormwater System", 0.59, 0.41, 0.54, 0.48},
		{"Institutional Legitimacy System", 0.56, 0.46, 0.46, 0.40},
		{"Community Heat Resilience System", 0.60, 0.39, 0.52, 0.42},
	}

	fmt.Println("system,hidden_risk,threshold_distance,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.5f,%.5f,%s\n", p.System, p.Risk, p.Distance, diagnostic(p))
	}
}
