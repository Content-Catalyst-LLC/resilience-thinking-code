package main

import "fmt"

type FeedbackProfile struct {
	System     string
	Risk       float64
	DelaySteps int
	Balancing  float64
	Signal     float64
}

func diagnostic(p FeedbackProfile) string {
	if p.Risk >= 0.12 {
		return "high feedback-risk concern"
	}
	if p.DelaySteps >= 7 {
		return "delay and overshoot concern"
	}
	if p.Balancing < 0.10 {
		return "weak balancing feedback concern"
	}
	if p.Signal < 0.48 {
		return "feedback blindness concern"
	}
	return "mixed feedback profile"
}

func main() {
	profiles := []FeedbackProfile{
		{"Climate Ice Albedo Loop", 0.138, 8, 0.070, 0.42},
		{"Community Mutual Aid Loop", 0.022, 2, 0.160, 0.72},
		{"Fire Suppression Fuel Loop", 0.147, 9, 0.090, 0.46},
	}

	fmt.Println("system,feedback_risk,diagnostic")
	for _, p := range profiles {
		fmt.Printf("%s,%.5f,%s\n", p.System, p.Risk, diagnostic(p))
	}
}
