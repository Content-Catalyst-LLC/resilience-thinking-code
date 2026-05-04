program viability_model
  implicit none

  integer, parameter :: steps = 30
  real :: viability(steps)
  real :: disturbance, adaptive_response
  integer :: t

  viability(1) = 1.0
  disturbance = 0.08
  adaptive_response = 0.09

  do t = 2, steps
     viability(t) = viability(t - 1) - disturbance + adaptive_response
     viability(t) = min(1.5, max(0.0, viability(t)))
  end do

  print *, "Viability simulation"

  do t = 1, steps
     print *, t, viability(t)
  end do

end program viability_model
