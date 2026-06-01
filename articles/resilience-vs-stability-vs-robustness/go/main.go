package main

import (
	"fmt"
	"math"
)

func sigmoid(z float64) float64 {
	return 1.0 / (1.0 + math.Exp(-z))
}

func predictFailure(adaptive, threshold, learning, redundancy, modularity, exposure, sensitivity, shock float64) float64 {
	protective := 0.24*adaptive + 0.22*threshold + 0.18*learning + 0.18*redundancy + 0.18*modularity
	pressure := 0.32*exposure + 0.28*sensitivity + 0.40*shock
	return sigmoid(-2.0 + 4.2*pressure - 3.8*protective)
}

func main() {
	scenarios := map[string][]float64{
		"stable_but_brittle":     {0.28, 0.32, 0.24, 0.35, 0.34, 0.64, 0.62, 0.45},
		"robust_but_inflexible": {0.38, 0.46, 0.33, 0.60, 0.43, 0.70, 0.58, 0.52},
		"adaptive_resilient":    {0.88, 0.80, 0.86, 0.73, 0.70, 0.52, 0.46, 0.50},
	}

	fmt.Println("scenario,predicted_failure_probability")
	for name, x := range scenarios {
		p := predictFailure(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
		fmt.Printf("%s,%.4f\n", name, p)
	}
}
