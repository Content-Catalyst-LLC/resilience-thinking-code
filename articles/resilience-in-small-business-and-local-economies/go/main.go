package main

import "fmt"

type Strategy struct {
	Name                 string
	Value                float64
	LiquiditySupport     float64
	WorkforceCapacity    float64
	EquityAccess         float64
	InequalityRisk       float64
	ImplementationBurden float64
}

func diagnostic(s Strategy) string {
	if s.ImplementationBurden >= 3.7 {
		return "implementation-burden review needed"
	}
	if s.InequalityRisk >= 3.1 {
		return "inequality-risk review needed"
	}
	if s.LiquiditySupport < 7.6 {
		return "liquidity-support review needed"
	}
	if s.WorkforceCapacity < 7.6 {
		return "workforce-capacity review needed"
	}
	if s.EquityAccess < 8.3 {
		return "equity-access review needed"
	}
	return "promising but requires local validation"
}

func main() {
	strategies := []Strategy{
		{"Emergency Microgrant and Liquidity Fund", 7.42, 9.2, 7.4, 8.6, 2.8, 3.0},
		{"Community Development Finance and Patient Capital", 7.55, 8.7, 7.5, 8.9, 2.7, 3.5},
		{"Local Procurement and Anchor Institution Access", 7.44, 7.6, 7.8, 8.4, 3.0, 3.6},
	}

	fmt.Println("strategy,value,diagnostic")
	for _, s := range strategies {
		fmt.Printf("%s,%.5f,%s\n", s.Name, s.Value, diagnostic(s))
	}
}
