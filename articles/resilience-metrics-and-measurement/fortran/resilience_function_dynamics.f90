program resilience_function_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, shock, adaptive_response, delayed_erosion

  function_level = 0.90
  adaptive_response = 0.46
  delayed_erosion = 0.08

  print *, "time,function_level,shock,adaptive_response,delayed_erosion"

  do t = 1, steps
     if (t == 20 .or. t == 50) then
        shock = 0.34
     else
        shock = 0.05
     end if

     delayed_erosion = min(1.0, max(0.0, delayed_erosion + 0.002 * shock - 0.001 * adaptive_response))
     adaptive_response = min(1.0, max(0.0, adaptive_response + 0.003 - 0.002 * delayed_erosion))

     function_level = min(1.0, max(0.0, &
        function_level - &
        0.35 * shock + &
        0.18 * adaptive_response - &
        0.12 * delayed_erosion))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", shock, ",", adaptive_response, ",", delayed_erosion
  end do
end program resilience_function_dynamics
