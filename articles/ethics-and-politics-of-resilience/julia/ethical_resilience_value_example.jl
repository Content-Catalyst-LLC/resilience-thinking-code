using Printf

function ethical_resilience_value(p,e,g,r,a,b,i)
    return 0.24*p + 0.22*e + 0.18*g + 0.14*r + 0.14*a - 0.05*b - 0.03*i
end

score = ethical_resilience_value(8.4, 9.0, 8.6, 8.3, 8.8, 2.8, 3.8)
@printf("strategy,ethical_resilience_value\nPublic Housing Climate Retrofit Program,%.5f\n", score)
