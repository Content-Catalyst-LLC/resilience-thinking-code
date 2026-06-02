program regime_shift_simulation
  implicit none

  integer, parameter :: steps = 180
  integer :: t
  real :: pressure, start_pressure, end_pressure, x

  start_pressure = -0.75
  end_pressure = 0.85
  x = -0.90

  print *, "time,pressure,state,regime"

  do t = 1, steps
     pressure = start_pressure + (end_pressure - start_pressure) * real(t - 1) / real(steps - 1)
     if (t > 1) then
        x = x + 0.05 * (1.2 * x - x**3 + pressure)
     end if

     if (x >= 0.0) then
        print '(I0,A,F9.5,A,F9.5,A,A)', t, ",", pressure, ",", x, ",", "upper regime"
     else
        print '(I0,A,F9.5,A,F9.5,A,A)', t, ",", pressure, ",", x, ",", "lower regime"
     end if
  end do
end program regime_shift_simulation
