using Printf

function resilience_value(a,b,t,g,q,d,c,e,i)
    return 0.16*a + 0.14*b + 0.16*t + 0.14*g + 0.14*q + 0.12*d + 0.14*c - 0.05*e - 0.05*i
end

score = resilience_value(8.7, 8.0, 8.4, 8.6, 9.1, 7.4, 8.3, 3.9, 3.2)
@printf("strategy,resilience_value\nCommunity Resilience and Mutual Aid Infrastructure,%.5f\n", score)
