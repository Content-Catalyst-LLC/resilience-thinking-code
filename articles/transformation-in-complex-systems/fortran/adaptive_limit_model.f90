program adaptive_limit_model
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: viability, adaptive_capacity, structural_rigidity
  real :: stress, transformative_capacity

  viability = 0.72
  adaptive_capacity = 0.62
  structural_rigidity = 0.36
  stress = 0.30
  transformative_capacity = 0.22

  print *, "time,viability,adaptive_capacity,structural_rigidity,stress,transformative_capacity"

  do t = 1, steps
     stress = min(1.0, max(0.0, stress + 0.006))
     structural_rigidity = min(1.0, max(0.0, structural_rigidity + 0.002))
     adaptive_capacity = min(1.0, max(0.0, adaptive_capacity - 0.0015 * stress + 0.001 * transformative_capacity))

     if (t >= 40) then
        transformative_capacity = min(1.0, max(0.0, transformative_capacity + 0.007))
     end if

     viability = min(1.0, max(0.0, &
        viability + &
        0.12 * adaptive_capacity - &
        0.10 * structural_rigidity - &
        0.16 * stress + &
        0.08 * transformative_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", viability, ",", adaptive_capacity, ",", structural_rigidity, ",", stress, ",", transformative_capacity
  end do
end program adaptive_limit_model
