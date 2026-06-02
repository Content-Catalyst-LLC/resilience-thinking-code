program maladaptive_lock_in_dynamics
  implicit none
  integer :: t
  real :: persistence, harm, lock_in, burden, transformation, ecology, equity
  real :: shock, maladaptive_risk, adaptive_resilience

  persistence = 0.70
  harm = 0.42
  lock_in = 0.44
  burden = 0.28
  transformation = 0.82
  ecology = 0.86
  equity = 0.84

  print *, "time,persistence,harm,lock_in,equity,ecology,maladaptive_risk,adaptive_resilience"
  do t = 1, 24
     if (mod(t, 8) == 0) then
        shock = 0.28
     else
        shock = 0.04
     end if

     persistence = max(0.0, min(1.0, persistence + 0.04 * shock + 0.02 * lock_in - 0.03 * transformation))
     harm = max(0.0, min(1.0, harm + 0.035 * persistence + 0.030 * burden + 0.025 * shock - 0.060 * transformation - 0.030 * ecology))
     lock_in = max(0.0, min(1.0, lock_in + 0.030 * persistence + 0.020 * shock - 0.055 * transformation))
     ecology = max(0.0, min(1.0, ecology - 0.025 * harm + 0.040 * transformation))
     equity = max(0.0, min(1.0, equity - 0.030 * burden - 0.020 * harm + 0.045 * transformation))

     maladaptive_risk = max(0.0, min(1.0, 0.30*persistence + 0.28*harm + 0.22*lock_in + 0.15*burden - 0.20*transformation - 0.10*equity))
     adaptive_resilience = max(0.0, min(1.0, 0.24*transformation + 0.20*ecology + 0.20*equity + 0.16*(1.0-harm) + 0.12*(1.0-lock_in) + 0.08*persistence - 0.16*maladaptive_risk))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', t, ",", persistence, ",", harm, ",", lock_in, ",", equity, ",", ecology, ",", maladaptive_risk, ",", adaptive_resilience
  end do
end program maladaptive_lock_in_dynamics
