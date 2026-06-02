program urban_function_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, infrastructure, community, ecology, adaptive
  real :: hazard_exposure, chronic_stress, dependency
  real :: hazard, infra_disruption, health, housing, market, dependency_amplification
  real :: stress_load, response_capacity

  function_level = 0.78
  infrastructure = 0.56
  community = 0.62
  ecology = 0.44
  adaptive = 0.64
  hazard_exposure = 0.82
  chronic_stress = 0.68
  dependency = 0.70

  print *, "time,urban_function,stress_load,response_capacity,dependency_coupling"

  do t = 1, steps
     if (t == 12) then
        hazard = 0.86
        infra_disruption = 0.72
        health = 0.84
        housing = 0.78
        market = 0.52
        dependency_amplification = 0.76
     else if (t == 27) then
        hazard = 0.84
        infra_disruption = 0.78
        health = 0.66
        housing = 0.74
        market = 0.56
        dependency_amplification = 0.78
     else if (t == 42) then
        hazard = 0.76
        infra_disruption = 0.88
        health = 0.78
        housing = 0.66
        market = 0.58
        dependency_amplification = 0.88
     else
        hazard = 0.06
        infra_disruption = 0.10
        health = 0.13
        housing = 0.14 + 0.0025 * real(t)
        market = 0.12
        dependency_amplification = 0.14
     end if

     stress_load = 0.25 * hazard + 0.19 * infra_disruption + 0.17 * health + 0.17 * housing + 0.10 * market + 0.12 * dependency_amplification + 0.10 * dependency
     response_capacity = max(0.0, min(1.0, 0.26 * infrastructure + 0.24 * community + 0.20 * ecology + 0.24 * adaptive - 0.18 * hazard_exposure - 0.12 * chronic_stress - 0.12 * dependency))

     function_level = max(0.0, min(1.0, function_level - 0.32 * stress_load + 0.18 * response_capacity + 0.10 * infrastructure + 0.09 * community + 0.08 * ecology + 0.08 * adaptive - 0.06 * dependency))
     dependency = max(0.0, min(1.0, dependency + 0.020 * stress_load - 0.011 * response_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", stress_load, ",", response_capacity, ",", dependency
  end do
end program urban_function_dynamics
