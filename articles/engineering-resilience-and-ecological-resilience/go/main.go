package main

import "fmt"

type Profile struct {
	Name       string
	Eng        float64
	Eco        float64
	Exposure   float64
	Sensitivity float64
}

func band(gap float64) string {
	if gap < -0.18 {
		return "engineering-heavy"
	}
	if gap > 0.18 {
		return "ecological-adaptive"
	}
	return "balanced"
}

func main() {
	profiles := []Profile{
		{"Hardened Infrastructure", 0.82, 0.45, 0.62, 0.58},
		{"Wetland System", 0.43, 0.69, 0.54, 0.44},
		{"Distributed Energy Network", 0.71, 0.62, 0.66, 0.52},
	}

	fmt.Println("system_type,engineering_resilience,ecological_resilience,gap,diagnostic")
	for _, p := range profiles {
		gap := p.Eco - p.Eng
		fmt.Printf("%s,%.4f,%.4f,%.4f,%s\n", p.Name, p.Eng, p.Eco, gap, band(gap))
	}
}
