program feedback_delay_simulation
  implicit none

  integer, parameter :: steps = 80
  integer, parameter :: delay_steps = 5
  integer :: t, delayed_index
  real :: gain, balancing, target, overshoot
  real, dimension(steps + delay_steps + 2) :: x

  gain = 0.03
  balancing = 0.14
  target = 75.0
  x = 20.0

  print *, "time,value,target,gain,balancing,delay,overshoot"

  do t = 2, steps
     delayed_index = max(1, t - delay_steps)
     x(t) = x(t - 1) + gain * x(t - 1) - balancing * (x(delayed_index) - target)
     overshoot = max(0.0, x(t) - target)

     print '(I0,A,F9.5,A,F9.5,A,F9.5,A,F9.5,A,I0,A,F9.5)', &
        t, ",", x(t), ",", target, ",", gain, ",", balancing, ",", delay_steps, ",", overshoot
  end do
end program feedback_delay_simulation
