program dynamic_viability
  implicit none

  integer, parameter :: steps = 60
  integer :: t
  real :: viability, disturbance, exposure, sensitivity
  real :: redundancy, modularity, adaptive_capacity
  real :: load, protection, adaptive_response, margin, threshold_distance, risk_pressure

  viability = 1.0
  exposure = 0.58
  sensitivity = 0.54
  redundancy = 0.61
  modularity = 0.56
  adaptive_capacity = 0.72
  threshold_distance = 0.63
  risk_pressure = 0.55 * exposure + 0.45 * sensitivity

  print *, "time_step,viability,margin"

  do t = 1, steps
     disturbance = 0.055

     if (t == 12) disturbance = disturbance + 0.20
     if (t == 24) disturbance = disturbance + 0.28
     if (t == 37) disturbance = disturbance + 0.23
     if (t == 48) disturbance = disturbance + 0.31

     load = disturbance * (0.65 + exposure) * (0.55 + sensitivity)
     protection = 0.35 * redundancy + 0.25 * modularity
     adaptive_response = 0.03 * adaptive_capacity

     viability = viability - load * (1.0 - 0.45 * protection) + adaptive_response
     if (viability < 0.0) viability = 0.0
     if (viability > 1.25) viability = 1.25

     margin = viability + threshold_distance - risk_pressure
     print '(I0,A,F6.4,A,F6.4)', t, ",", viability, ",", margin
  end do
end program dynamic_viability
