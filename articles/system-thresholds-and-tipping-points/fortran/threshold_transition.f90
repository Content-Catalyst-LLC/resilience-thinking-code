program threshold_transition
  implicit none

  integer, parameter :: steps = 160
  integer :: i
  real :: start_pressure, end_pressure, pressure, x, xb

  start_pressure = -0.8
  end_pressure = 0.8
  x = -0.9

  print *, "direction,step,pressure,state,regime"

  do i = 1, steps
     pressure = start_pressure + (end_pressure - start_pressure) * real(i - 1) / real(steps - 1)
     if (i > 1) then
        x = x + 0.05 * (1.2 * x - x**3 + pressure)
     end if

     if (x >= 0.0) then
        print '(A,A,I0,A,F8.5,A,F8.5,A,A)', "Increasing Pressure", ",", i, ",", pressure, ",", x, ",", "upper regime"
     else
        print '(A,A,I0,A,F8.5,A,F8.5,A,A)', "Increasing Pressure", ",", i, ",", pressure, ",", x, ",", "lower regime"
     end if
  end do

  xb = x

  do i = 1, steps
     pressure = end_pressure + (start_pressure - end_pressure) * real(i - 1) / real(steps - 1)
     if (i > 1) then
        xb = xb + 0.05 * (1.2 * xb - xb**3 + pressure)
     end if

     if (xb >= 0.0) then
        print '(A,A,I0,A,F8.5,A,F8.5,A,A)', "Decreasing Pressure", ",", i, ",", pressure, ",", xb, ",", "upper regime"
     else
        print '(A,A,I0,A,F8.5,A,F8.5,A,A)', "Decreasing Pressure", ",", i, ",", pressure, ",", xb, ",", "lower regime"
     end if
  end do
end program threshold_transition
