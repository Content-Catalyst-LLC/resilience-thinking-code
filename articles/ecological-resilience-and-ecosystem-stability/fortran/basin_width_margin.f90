program basin_width_margin
  implicit none
  integer, parameter :: steps = 140
  integer :: t
  real :: basin_width, disturbance_load, regenerative_capacity, margin

  print *, "time,basin_width,disturbance_load,regenerative_capacity,resilience_margin,threshold_flag"
  do t = 1, steps
     basin_width = 0.85 - 0.47 * real(t - 1) / real(steps - 1)
     disturbance_load = 0.10 + 0.68 * real(t - 1) / real(steps - 1)
     regenerative_capacity = 0.36 + 0.18 * sin(real(t) / 18.0)
     margin = basin_width - disturbance_load + regenerative_capacity
     if (margin < 0.15) then
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", basin_width, ",", disturbance_load, ",", regenerative_capacity, ",", margin, ",", "threshold risk"
     else
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", basin_width, ",", disturbance_load, ",", regenerative_capacity, ",", margin, ",", "viable margin"
     end if
  end do
end program basin_width_margin
