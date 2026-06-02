package main

import "fmt"

type System struct {
	Name          string
	Score         float64
	ThresholdRisk float64
	Justice       float64
	Missingness   float64
}

func diagnostic(s System) string {
	if s.ThresholdRisk >= 0.50 {
		return "threshold risk review required"
	}
	if s.Justice <= 0.52 {
		return "justice visibility review required"
	}
	if s.Missingness >= 0.24 {
		return "missing-data review required"
	}
	return "no immediate red flag"
}

func main() {
	systems := []System{
		{"Urban Water Network", 0.55, 0.46, 0.50, 0.18},
		{"Community Cooling Network", 0.49, 0.55, 0.72, 0.26},
		{"Wetland Floodplain System", 0.61, 0.38, 0.58, 0.14},
	}

	fmt.Println("system,score,diagnostic")
	for _, s := range systems {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Score, diagnostic(s))
	}
}
