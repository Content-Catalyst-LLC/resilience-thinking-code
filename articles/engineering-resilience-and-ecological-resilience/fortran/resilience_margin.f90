program resilience_margin
  implicit none

  integer, parameter :: steps = 120
  integer :: t
  real :: basin_width, disturbance_load, adaptive_capacity, margin

  print *, "time,basin_width,disturbance_load,adaptive_capacity,resilience_margin"

  do t = 1, steps
     basin_width = 0.90 - 0.48 * real(t - 1) / real(steps - 1)
     disturbance_load = 0.10 + 0.62 * real(t - 1) / real(steps - 1)
     adaptive_capacity = 0.35 + 0.22 * sin(real(t) / 20.0)
     margin = basin_width - disturbance_load + adaptive_capacity

     print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4)', t, ",", basin_width, ",", disturbance_load, ",", adaptive_capacity, ",", margin
  end do
end program resilience_margin
