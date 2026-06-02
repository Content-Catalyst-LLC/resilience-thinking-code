using Printf

function just_transformation_value(r,t,e,eco,g,l,x,b,k,i)
    return 0.13*r + 0.16*t + 0.16*e + 0.13*eco + 0.14*g + 0.13*l + 0.13*x - 0.03*b - 0.02*k - 0.01*i
end

score = just_transformation_value(8.4, 8.9, 8.7, 9.2, 8.8, 8.5, 9.0, 2.9, 2.8, 4.0)
@printf("pathway,just_transformation_value\nParticipatory Retreat and Wetland Restoration,%.5f\n", score)
