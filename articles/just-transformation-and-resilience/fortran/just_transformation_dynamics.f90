program just_transformation_dynamics
  implicit none
  integer :: step
  real :: exposure, capacity, transformation, protection, ecology, legitimacy
  real :: burden, lock_in, trust, shock, climate_pressure
  real :: transformation_capacity, justice_gap, justice_adjusted_resilience

  exposure = 0.72
  capacity = 0.84
  transformation = 0.88
  protection = 0.86
  ecology = 0.90
  legitimacy = 0.88
  burden = 0.30
  lock_in = 0.28
  trust = 0.50

  print *, "time,exposure,capacity,protection,ecology,trust,lock_in,justice_gap,justice_adjusted_resilience"

  do step = 1, 24
     if (mod(step, 8) == 0) then
        shock = 0.30
     else
        shock = 0.04
     end if

     climate_pressure = 0.18 + 0.006 * step + 0.25 * shock

     exposure = max(0.0, min(1.0, exposure + 0.04 * climate_pressure + 0.03 * lock_in - 0.07 * transformation - 0.05 * ecology - 0.04 * capacity))
     capacity = max(0.0, min(1.0, capacity + 0.04 * legitimacy + 0.03 * transformation - 0.03 * shock))
     protection = max(0.0, min(1.0, protection + 0.04 * capacity + 0.03 * legitimacy - 0.04 * burden - 0.02 * shock))
     trust = max(0.0, min(1.0, trust + 0.05 * legitimacy + 0.04 * protection - 0.06 * burden - 0.03 * shock))
     lock_in = max(0.0, min(1.0, lock_in + 0.025 * shock + 0.025 * burden - 0.060 * transformation - 0.035 * capacity))
     ecology = max(0.0, min(1.0, ecology + 0.035 * transformation + 0.025 * capacity - 0.025 * climate_pressure))

     transformation_capacity = max(0.0, min(1.0, 0.26 * transformation + 0.20 * capacity + 0.18 * legitimacy + 0.15 * protection + 0.12 * ecology + 0.09 * trust))
     justice_gap = max(0.0, min(1.0, 0.30 * burden + 0.24 * lock_in + 0.20 * exposure - 0.18 * protection - 0.16 * legitimacy))
     justice_adjusted_resilience = max(0.0, min(1.0, 0.24 * transformation_capacity + 0.18 * protection + 0.18 * ecology + 0.16 * trust + 0.14 * (1.0 - exposure) + 0.10 * (1.0 - lock_in) - 0.20 * justice_gap))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', step, ",", exposure, ",", capacity, ",", protection, ",", ecology, ",", trust, ",", lock_in, ",", justice_gap, ",", justice_adjusted_resilience
  end do
end program just_transformation_dynamics
