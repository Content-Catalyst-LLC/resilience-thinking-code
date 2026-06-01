program threshold_persistence
  implicit none

  integer, parameter :: steps = 160
  integer :: t
  real :: x, r, dt, pressure

  x = -0.9
  r = 1.1
  dt = 0.05

  print *, "time,pressure,threshold_state"

  do t = 1, steps
     pressure = -0.45 + 1.30 * real(t - 1) / real(steps - 1)

     if (t > 1) then
        x = x + dt * (r * x - x**3 + pressure)
     end if

     print '(I0,A,F8.5,A,F8.5)', t, ",", pressure, ",", x
  end do
end program threshold_persistence
