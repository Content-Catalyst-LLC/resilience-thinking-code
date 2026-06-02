program health_system_function_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, prevention, detection, continuity, workforce, trust, adaptive
  real :: hazard_exposure, chronic_stress, dependency
  real :: hazard, surge, service_disruption, workforce_burden, trust_pressure, supply, dependency_amplification
  real :: stress_load, response_capacity

  function_level = 0.78
  prevention = 0.70
  detection = 0.72
  continuity = 0.66
  workforce = 0.64
  trust = 0.68
  adaptive = 0.70
  hazard_exposure = 0.74
  chronic_stress = 0.68
  dependency = 0.72

  print *, "time,health_system_function,stress_load,response_capacity,dependency_coupling"

  do t = 1, steps
     if (t == 12) then
        hazard = 0.84
        surge = 0.86
        service_disruption = 0.62
        workforce_burden = 0.78
        trust_pressure = 0.82
        supply = 0.70
        dependency_amplification = 0.78
     else
        hazard = 0.06
        surge = 0.11
        service_disruption = 0.09
        workforce_burden = 0.14 + 0.0025 * real(t)
        trust_pressure = 0.12
        supply = 0.10
        dependency_amplification = 0.12
     end if

     stress_load = 0.20 * hazard + 0.20 * surge + 0.16 * service_disruption + 0.16 * workforce_burden + 0.10 * trust_pressure + 0.08 * supply + 0.10 * dependency_amplification + 0.08 * dependency
     response_capacity = max(0.0, min(1.0, 0.16 * prevention + 0.17 * detection + 0.18 * continuity + 0.17 * workforce + 0.16 * trust + 0.16 * adaptive - 0.16 * hazard_exposure - 0.12 * chronic_stress - 0.10 * dependency))

     function_level = max(0.0, min(1.0, function_level - 0.34 * stress_load + 0.18 * response_capacity + 0.08 * prevention + 0.08 * detection + 0.09 * continuity + 0.08 * workforce + 0.07 * trust + 0.07 * adaptive - 0.05 * dependency))
     dependency = max(0.0, min(1.0, dependency + 0.020 * stress_load - 0.011 * response_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", stress_load, ",", response_capacity, ",", dependency
  end do
end program health_system_function_dynamics
