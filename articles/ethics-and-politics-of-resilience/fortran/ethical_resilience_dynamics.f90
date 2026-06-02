program ethical_resilience_dynamics
  implicit none
  integer :: t
  real :: protection, equity, legitimacy, recognition, accountability, burden, score

  protection = 7.9
  equity = 8.5
  legitimacy = 8.9
  recognition = 8.7
  accountability = 8.3
  burden = 3.4

  print *, "time,protection,equity,legitimacy,recognition,accountability,burden,ethical_resilience_value"
  do t = 1, 20
     accountability = min(10.0, accountability + 0.03)
     legitimacy = min(10.0, legitimacy + 0.02)
     burden = max(1.0, burden - 0.025)
     score = 0.24*protection + 0.22*equity + 0.18*legitimacy + 0.14*recognition + 0.14*accountability - 0.05*burden - 0.03*3.1
     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', t, ",", protection, ",", equity, ",", legitimacy, ",", recognition, ",", accountability, ",", burden, ",", score
  end do
end program ethical_resilience_dynamics
