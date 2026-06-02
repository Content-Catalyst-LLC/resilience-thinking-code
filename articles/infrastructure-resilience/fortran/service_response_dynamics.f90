program service_response_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: service_level, redundancy_capacity, recovery_capacity, adaptive_capacity
  real :: shock_exposure, chronic_system_stress, interdependence_coupling
  real :: shock, chronic, compound, cascade, stress_load, response_capacity

  service_level = 0.86
  redundancy_capacity = 0.66
  recovery_capacity = 0.72
  adaptive_capacity = 0.70
  shock_exposure = 0.70
  chronic_system_stress = 0.58
  interdependence_coupling = 0.80

  print *, "time,service_level,stress_load,response_capacity,interdependence_coupling"

  do t = 1, steps
     if (t == 12) then
        shock = 0.82
        chronic = 0.56
        compound = 0.70
        cascade = 0.74
     else if (t == 27) then
        shock = 0.80
        chronic = 0.64
        compound = 0.72
        cascade = 0.78
     else if (t == 42) then
        shock = 0.84
        chronic = 0.60
        compound = 0.73
        cascade = 0.76
     else if (t == 56) then
        shock = 0.76
        chronic = 0.52
        compound = 0.68
        cascade = 0.86
     else
        shock = 0.05
        chronic = 0.14 + 0.0028 * real(t)
        compound = 0.10
        cascade = 0.12
     end if

     stress_load = 0.34 * shock + 0.18 * chronic + 0.18 * compound + 0.18 * cascade + 0.12 * interdependence_coupling
     response_capacity = max(0.0, min(1.0, 0.33 * redundancy_capacity + 0.30 * recovery_capacity + 0.24 * adaptive_capacity - 0.20 * shock_exposure - 0.12 * chronic_system_stress - 0.16 * interdependence_coupling))

     service_level = max(0.0, min(1.0, service_level - 0.32 * stress_load + 0.20 * response_capacity + 0.12 * recovery_capacity + 0.08 * adaptive_capacity - 0.08 * interdependence_coupling))
     interdependence_coupling = max(0.0, min(1.0, interdependence_coupling + 0.020 * stress_load - 0.012 * response_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", service_level, ",", stress_load, ",", response_capacity, ",", interdependence_coupling
  end do
end program service_response_dynamics
