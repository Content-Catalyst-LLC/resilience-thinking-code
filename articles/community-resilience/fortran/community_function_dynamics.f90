program community_function_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, social, institution, access, economy, information, adaptive
  real :: hazard_exposure, chronic_stress, dependency
  real :: hazard, service, institutional_pressure, communication, economic, care, dependency_amplification
  real :: stress_load, response_capacity

  function_level = 0.80
  social = 0.84
  institution = 0.68
  access = 0.62
  economy = 0.64
  information = 0.70
  adaptive = 0.76
  hazard_exposure = 0.70
  chronic_stress = 0.60
  dependency = 0.64

  print *, "time,community_function,stress_load,response_capacity,dependency_coupling"

  do t = 1, steps
     if (t == 12) then
        hazard = 0.86
        service = 0.78
        institutional_pressure = 0.66
        communication = 0.58
        economic = 0.62
        care = 0.74
        dependency_amplification = 0.78
     else
        hazard = 0.06
        service = 0.11
        institutional_pressure = 0.12
        communication = 0.10
        economic = 0.11
        care = 0.12 + 0.0018 * real(t)
        dependency_amplification = 0.12
     end if

     stress_load = 0.18 * hazard + 0.17 * service + 0.15 * institutional_pressure + 0.14 * communication + 0.13 * economic + 0.13 * care + 0.10 * dependency_amplification + 0.08 * dependency
     response_capacity = max(0.0, min(1.0, 0.17 * social + 0.17 * institution + 0.16 * access + 0.14 * economy + 0.16 * information + 0.20 * adaptive - 0.16 * hazard_exposure - 0.12 * chronic_stress - 0.10 * dependency))

     function_level = max(0.0, min(1.0, function_level - 0.34 * stress_load + 0.18 * response_capacity + 0.09 * social + 0.08 * institution + 0.08 * access + 0.07 * economy + 0.08 * information + 0.09 * adaptive - 0.05 * dependency))
     dependency = max(0.0, min(1.0, dependency + 0.020 * stress_load - 0.011 * response_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", stress_load, ",", response_capacity, ",", dependency
  end do
end program community_function_dynamics
