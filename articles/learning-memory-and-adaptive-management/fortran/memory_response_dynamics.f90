program memory_response_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, memory, adaptive_capacity, shock
  real :: learning_rate, feedback_use, governance_capacity, forgetting_pressure, monitoring_quality
  real :: monitoring_signal, learning

  function_level = 0.88
  memory = 0.78
  adaptive_capacity = 0.55
  learning_rate = 0.15
  feedback_use = 0.72
  governance_capacity = 0.76
  forgetting_pressure = 0.28
  monitoring_quality = 0.78

  print *, "time,function_level,memory,adaptive_capacity,shock,learning"

  do t = 1, steps
     if (t == 15) then
        shock = 0.35
     else if (t == 32) then
        shock = 0.22
     else if (t == 50) then
        shock = 0.40
     else if (t == 67) then
        shock = 0.28
     else
        shock = 0.04
     end if

     monitoring_signal = min(1.0, max(0.0, monitoring_quality * shock))
     learning = learning_rate * monitoring_signal * feedback_use * governance_capacity

     memory = min(1.0, max(0.0, 0.78 * memory + learning - 0.05 * forgetting_pressure))

     adaptive_capacity = min(1.0, max(0.0, &
        0.82 * adaptive_capacity + 0.12 * memory + 0.10 * governance_capacity - 0.06 * forgetting_pressure))

     function_level = min(1.0, max(0.0, &
        function_level - 0.42 * shock + 0.24 * adaptive_capacity + 0.10 * memory - 0.05 * forgetting_pressure))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", memory, ",", adaptive_capacity, ",", shock, ",", learning
  end do
end program memory_response_dynamics
