package main

import "fmt"

func main() {
	score := 0.16*8.9 + 0.14*7.7 + 0.16*8.8 + 0.14*9.2 + 0.14*8.8 + 0.12*8.1 + 0.14*8.5 - 0.05*3.9 - 0.05*3.5
	fmt.Printf("resilience_value=%.5f\n", score)
}
