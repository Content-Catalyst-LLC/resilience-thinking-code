using Printf

function adaptive_value(p,h,l,e,t,eco,b,i)
    return 0.12*p + 0.20*h + 0.16*l + 0.16*e + 0.18*t + 0.14*eco - 0.03*b - 0.01*i
end

score = adaptive_value(7.6, 8.8, 8.6, 8.7, 8.9, 9.0, 2.9, 4.0)
@printf("strategy,adaptive_resilience_value\nFloodplain Restoration and Housing Transition,%.5f\n", score)
