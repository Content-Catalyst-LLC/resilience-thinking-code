package main

import "fmt"

func main() {
	score := 0.24*8.0 + 0.22*9.2 + 0.18*8.4 + 0.14*8.2 + 0.14*8.9 - 0.05*2.9 - 0.03*3.6
	fmt.Printf("ethical_resilience_value=%.5f\n", score)
}
