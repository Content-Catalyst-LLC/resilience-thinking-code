package main

import "fmt"

func main() {
	score := 0.18*8.4 + 0.18*8.8 + 0.16*8.5 + 0.14*8.2 + 0.13*8.2 + 0.16*8.5 - 0.04*2.8 - 0.01*3.8
	fmt.Printf("support_resilience_value=%.5f\n", score)
}
