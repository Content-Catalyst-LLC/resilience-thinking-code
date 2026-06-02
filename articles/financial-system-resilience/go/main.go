package main

import "fmt"

type Strategy struct {
	Name                     string
	Value                    float64
	ImplementationBurden     float64
	InclusiveResilience      float64
	InfrastructureRobustness  float64
	SystemicExposure         float64
	LiquidityResilience      float64
}

func diagnostic(s Strategy) string {
	if s.ImplementationBurden >= 3.7 {
		return "implementation-burden review needed"
	}
	if s.InclusiveResilience < 7.5 {
		return "financial-inclusion review needed"
	}
	if s.InfrastructureRobustness < 7.6 {
		return "infrastructure-resilience review needed"
	}
	if s.SystemicExposure >= 4.4 {
		return "systemic-exposure review needed"
	}
	if s.LiquidityResilience < 7.5 {
		return "liquidity-resilience review needed"
	}
	return "promising but requires stress testing"
}

func main() {
	strategies := []Strategy{
		{"Higher Capital and Liquidity Buffers", 4.96, 3.2, 7.4, 7.6, 3.9, 8.8},
		{"Payment and Clearing Infrastructure Hardening", 4.94, 3.5, 7.8, 9.2, 3.8, 7.8},
		{"Inclusive Finance and Household Balance Sheet Resilience", 4.89, 3.0, 9.2, 7.4, 4.0, 7.4},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
