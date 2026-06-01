# Predictive Modeling Principles

This companion scaffold treats resilience prediction as a structured decision-support problem, not as a universal score.

## Modeling target

The synthetic target is `resilience_failure_risk`, a binary outcome indicating whether a system falls below a viable threshold margin after simulated disturbance.

## Feature families

- **Stability features:** equilibrium return, damping strength, return time.
- **Robustness features:** stress tolerance, safety margin, load capacity.
- **Resilience features:** adaptive capacity, learning capacity, threshold distance, redundancy, modularity.
- **Vulnerability features:** exposure, sensitivity, dependency concentration, disturbance load.
- **Scenario features:** shock intensity, shock frequency, compound disturbance index.

## Predictive use

A valid predictive model should be calibrated with real observations, tested against held-out conditions, evaluated for distribution shift, and interpreted in a decision process that includes local knowledge and ethical review.

## Important caution

A predictive resilience model can be harmful if it is used to label communities, institutions, or ecosystems as "low resilience" without addressing structural causes of vulnerability. Model outputs should guide inquiry and support investment, not justify abandonment.
