using Printf

function scenario_value(horizon, weak, stress, pathways, participation, modeling, governance, equity, transformation, risk, implementation)
    return 0.10*horizon + 0.10*weak + 0.11*stress + 0.12*pathways + 0.11*participation +
           0.10*modeling + 0.12*governance + 0.12*equity + 0.12*transformation -
           0.04*risk - 0.04*implementation
end

score = scenario_value(8.2, 8.4, 8.5, 9.4, 8.3, 8.5, 8.9, 8.5, 8.7, 2.7, 3.7)
@printf("strategy,scenario_resilience_value\nAdaptive Pathways and Trigger Framework,%.5f\n", score)
