program climate_stress_response
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, adaptive_capacity, recovery_capacity, exposure, vulnerability
  real :: threshold_proximity, shock, slow_stress, compound_risk, stress_load, adaptive_response

  function_level = 0.82
  adaptive_capacity = 0.58
  recovery_capacity = 0.62
  exposure = 0.72
  vulnerability = 0.68
  threshold_proximity = 0.52

  print *, "time,function_level,stress_load,adaptive_response,threshold_proximity"

  do t = 1, steps
     if (t == 12) then
        shock = 0.82
        slow_stress = 0.64
        compound_risk = 0.70
     else if (t == 28) then
        shock = 0.80
        slow_stress = 0.58
        compound_risk = 0.66
     else if (t == 43) then
        shock = 0.76
        slow_stress = 0.72
        compound_risk = 0.74
     else if (t == 59) then
        shock = 0.84
        slow_stress = 0.60
        compound_risk = 0.73
     else
        shock = 0.05
        slow_stress = 0.18 + 0.003 * real(t)
        compound_risk = 0.12
     end if

     stress_load = 0.45 * shock + 0.24 * slow_stress + 0.18 * compound_risk + 0.13 * threshold_proximity
     adaptive_response = max(0.0, min(1.0, 0.42 * adaptive_capacity + 0.35 * recovery_capacity - 0.28 * exposure - 0.20 * vulnerability))

     function_level = max(0.0, min(1.0, function_level - 0.36 * stress_load + 0.22 * adaptive_response + 0.12 * recovery_capacity - 0.08 * threshold_proximity))
     threshold_proximity = max(0.0, min(1.0, threshold_proximity + 0.02 * stress_load - 0.012 * adaptive_response))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", stress_load, ",", adaptive_response, ",", threshold_proximity
  end do
end program climate_stress_response
