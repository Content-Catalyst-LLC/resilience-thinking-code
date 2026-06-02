program organizational_function_dynamics
  implicit none
  integer :: t
  real :: f, learning, memory, strain, disruption, adaptive
  f = 0.84; learning = 0.90; memory = 0.88; strain = 0.30
  print *, "time,function,learning,memory,strain"
  do t = 1, 40
     if (t == 10 .or. t == 24) then
        disruption = 0.75
     else
        disruption = 0.07
     end if
     adaptive = 0.20*learning + 0.20*memory + 0.20*(1.0-strain) + 0.40*0.86
     strain = max(0.0, min(1.0, strain + 0.15*disruption - 0.10*0.86))
     f = max(0.0, min(1.0, f - 0.30*disruption + 0.22*adaptive - 0.15*strain))
     learning = max(0.0, min(1.0, learning + 0.06*disruption - 0.03*strain))
     memory = max(0.0, min(1.0, memory + 0.04*learning - 0.03*strain))
     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', t, ",", f, ",", learning, ",", memory, ",", strain
  end do
end program organizational_function_dynamics
