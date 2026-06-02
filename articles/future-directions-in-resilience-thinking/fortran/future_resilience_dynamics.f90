program future_resilience_dynamics
  implicit none
  integer :: t
  real :: performance, adaptive_capacity, friction, transformation, shock

  performance = 0.82
  adaptive_capacity = 0.74
  friction = 0.28
  transformation = 0.58

  print *, "time,performance,adaptive_capacity,recovery_friction,transformation"
  do t = 1, 24
     if (mod(t, 8) == 0) then
        shock = 0.30
     else
        shock = 0.06
     end if
     adaptive_capacity = min(1.0, adaptive_capacity + 0.01 + 0.02 * transformation)
     friction = max(0.0, friction + 0.01 * shock - 0.02 * adaptive_capacity)
     performance = max(0.0, min(1.0, performance - 0.18 * shock + 0.09 * adaptive_capacity - 0.06 * friction + 0.04 * transformation))
     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', t, ",", performance, ",", adaptive_capacity, ",", friction, ",", transformation
  end do
end program future_resilience_dynamics
