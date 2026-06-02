program resilience_future_dynamics
  implicit none
  integer :: t
  real :: f, v, trust, adaptive_buffer, score

  f = 0.82
  v = 0.38
  trust = 0.58

  print *, "time,function,vulnerability,trust,resilience_score"
  do t = 1, 20
     adaptive_buffer = 0.76
     f = max(0.0, min(1.0, f - 0.03 - 0.02*v + 0.06*adaptive_buffer + 0.03*trust))
     v = max(0.0, min(1.0, v + 0.01 - 0.04*adaptive_buffer))
     trust = max(0.0, min(1.0, trust + 0.02 - 0.03*v))
     score = max(0.0, min(1.0, 0.35*f + 0.25*adaptive_buffer + 0.20*trust + 0.20*(1.0-v)))
     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', t, ",", f, ",", v, ",", trust, ",", score
  end do
end program resilience_future_dynamics
