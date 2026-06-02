package main

import "fmt"

type Framework struct {
	Name               string
	Value              float64
	ThresholdBlindness float64
	Justice            float64
	DataQuality        float64
}

func diagnostic(f Framework) string {
	if f.Value >= 5.95 && f.ThresholdBlindness <= 3.4 {
		return "strong hybrid measurement profile"
	}
	if f.ThresholdBlindness >= 4.8 {
		return "threshold blindness review needed"
	}
	if f.Justice < 7.2 {
		return "justice visibility needs strengthening"
	}
	if f.DataQuality < 7.3 {
		return "data-quality transparency constraint"
	}
	return "promising but requires validation"
}

func main() {
	frameworks := []Framework{
		{"Indicator Dashboard", 4.85, 5.2, 6.8, 7.2},
		{"Participatory Resilience Assessment", 5.37, 4.3, 8.8, 7.1},
		{"Hybrid Structural and Dynamic Assessment", 6.16, 3.2, 8.1, 8.5},
	}

	fmt.Println("framework,value,diagnostic")
	for _, f := range frameworks {
		fmt.Printf("%s,%.5f,%s\n", f.Name, f.Value, diagnostic(f))
	}
}
