package main

import "fmt"

func main() {
	score := 0.13*8.6 + 0.16*8.5 + 0.16*9.0 + 0.13*8.0 + 0.14*8.7 + 0.13*8.2 + 0.13*8.8 - 0.03*2.7 - 0.02*2.9 - 0.01*3.8
	fmt.Printf("just_transformation_value=%.5f\n", score)
}
