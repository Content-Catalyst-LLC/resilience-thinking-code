package main

import "fmt"

func main() {
	score := 0.12*8.2 + 0.20*8.7 + 0.16*8.0 + 0.16*9.0 + 0.18*8.4 + 0.14*7.8 - 0.03*2.8 - 0.01*3.7
	fmt.Printf("adaptive_resilience_value=%.5f\n", score)
}
