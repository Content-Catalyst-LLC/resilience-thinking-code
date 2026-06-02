program institutional_function_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, legitimacy, capacity, flexibility, coordination, learning, accountability
  real :: stress_exposure, chronic_stress, dependency
  real :: shock, legitimacy_pressure, capacity_burden, coordination_stress, information_stress
  real :: legal_stress, dependency_amplification, stress_load, response_capacity, weakest_condition, threshold_penalty

  function_level = 0.78
  legitimacy = 0.72
  capacity = 0.74
  flexibility = 0.68
  coordination = 0.80
  learning = 0.70
  accountability = 0.72
  stress_exposure = 0.78
  chronic_stress = 0.62
  dependency = 0.78

  print *, "time,institutional_function,stress_load,response_capacity,dependency_coupling"

  do t = 1, steps
     if (t == 12) then
        shock = 0.82
        legitimacy_pressure = 0.90
        capacity_burden = 0.66
        coordination_stress = 0.70
        information_stress = 0.78
        legal_stress = 0.62
        dependency_amplification = 0.76
     else
        shock = 0.06
        legitimacy_pressure = 0.11
        capacity_burden = 0.12
        coordination_stress = 0.10
        information_stress = 0.10
        legal_stress = 0.09 + 0.0015 * real(t)
        dependency_amplification = 0.12
     end if

     stress_load = 0.18 * shock + 0.17 * legitimacy_pressure + 0.16 * capacity_burden + 0.16 * coordination_stress + 0.13 * information_stress + 0.12 * legal_stress + 0.10 * dependency_amplification + 0.08 * dependency
     response_capacity = max(0.0, min(1.0, 0.17 * legitimacy + 0.18 * capacity + 0.14 * flexibility + 0.18 * coordination + 0.17 * learning + 0.16 * accountability - 0.16 * stress_exposure - 0.12 * chronic_stress - 0.10 * dependency))

     weakest_condition = min(legitimacy, capacity, coordination, accountability)
     threshold_penalty = max(0.0, 0.72 - weakest_condition) * 0.16

     function_level = max(0.0, min(1.0, function_level - 0.34 * stress_load + 0.18 * response_capacity + 0.08 * legitimacy + 0.09 * capacity + 0.07 * flexibility + 0.09 * coordination + 0.08 * learning + 0.08 * accountability - 0.05 * dependency - threshold_penalty))
     dependency = max(0.0, min(1.0, dependency + 0.020 * stress_load - 0.011 * response_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", stress_load, ",", response_capacity, ",", dependency
  end do
end program institutional_function_dynamics
