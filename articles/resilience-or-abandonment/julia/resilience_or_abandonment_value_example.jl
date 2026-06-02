using Printf

function support_value(p,s,a,g,t,x,b,i)
    return 0.18*p + 0.18*s + 0.16*a + 0.14*g + 0.13*t + 0.16*x - 0.04*b - 0.01*i
end

score = support_value(8.5, 8.6, 8.7, 8.5, 8.4, 8.7, 2.7, 3.9)
@printf("strategy,support_resilience_value\nDrainage Repair and Social Protection Package,%.5f\n", score)
