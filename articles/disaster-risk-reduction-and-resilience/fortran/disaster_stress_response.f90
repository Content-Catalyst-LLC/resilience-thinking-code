program disaster_stress_response
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, preparedness_capacity, recovery_capacity
  real :: hazard_exposure, vulnerability, dependency_coupling
  real :: shock, slow_stress, compound_risk, cascade, stress_load, response_capacity

  function_level = 0.80
  preparedness_capacity = 0.58
  recovery_capacity = 0.60
  hazard_exposure = 0.72
  vulnerability = 0.66
  dependency_coupling = 0.62

  print *, "time,function_level,stress_load,response_capacity,dependency_coupling"

  do t = 1, steps
     if (t == 12) then
        shock = 0.82
        slow_stress = 0.56
        compound_risk = 0.68
        cascade = 0.70
     else if (t == 28) then
        shock = 0.80
        slow_stress = 0.64
        compound_risk = 0.72
        cascade = 0.76
     else if (t == 43) then
        shock = 0.84
        slow_stress = 0.60
        compound_risk = 0.73
        cascade = 0.72
     else if (t == 59) then
        shock = 0.76
        slow_stress = 0.72
        compound_risk = 0.74
        cascade = 0.68
     else
        shock = 0.05
        slow_stress = 0.16 + 0.0025 * real(t)
        compound_risk = 0.10
        cascade = 0.12
     end if

     stress_load = 0.38 * shock + 0.20 * slow_stress + 0.18 * compound_risk + 0.16 * cascade + 0.08 * dependency_coupling
     response_capacity = max(0.0, min(1.0, 0.45 * preparedness_capacity + 0.34 * recovery_capacity - 0.24 * hazard_exposure - 0.18 * vulnerability - 0.12 * dependency_coupling))

     function_level = max(0.0, min(1.0, function_level - 0.34 * stress_load + 0.23 * response_capacity + 0.13 * recovery_capacity - 0.07 * dependency_coupling))
     dependency_coupling = max(0.0, min(1.0, dependency_coupling + 0.018 * stress_load - 0.010 * response_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", stress_load, ",", response_capacity, ",", dependency_coupling
  end do
end program disaster_stress_response
