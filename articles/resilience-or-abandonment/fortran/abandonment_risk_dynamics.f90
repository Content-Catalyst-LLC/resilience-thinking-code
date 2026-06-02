program abandonment_risk_dynamics
  implicit none
  integer :: t
  real :: exposure, recovery, trust, support, governance, capacity, burden, transformation
  real :: shock, support_strength, abandonment_risk, justice_resilience

  exposure = 0.66
  recovery = 0.82
  trust = 0.50
  support = 0.84
  governance = 0.80
  capacity = 0.82
  burden = 0.28
  transformation = 0.74

  print *, "time,exposure,recovery,trust,support_strength,abandonment_risk,justice_adjusted_resilience"
  do t = 1, 24
     if (mod(t, 8) == 0) then
        shock = 0.32
     else
        shock = 0.05
     end if

     exposure = max(0.0, min(1.0, exposure + 0.02 + 0.06 * shock - 0.08 * transformation - 0.06 * capacity))
     recovery = max(0.0, min(1.0, recovery + 0.04 * support + 0.04 * capacity + 0.03 * governance - 0.05 * shock))
     trust = max(0.0, min(1.0, trust + 0.05 * governance + 0.04 * recovery + 0.03 * support - 0.07 * burden - 0.04 * shock))
     support_strength = max(0.0, min(1.0, 0.28 * support + 0.24 * recovery + 0.20 * governance + 0.16 * capacity + 0.12 * trust))
     abandonment_risk = max(0.0, min(1.0, exposure + 0.45 * burden + 0.25 * shock - support_strength))
     justice_resilience = max(0.0, min(1.0, 0.32 * support_strength + 0.22 * recovery + 0.18 * trust + 0.16 * transformation + 0.12 * (1.0 - exposure) - 0.20 * abandonment_risk))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', t, ",", exposure, ",", recovery, ",", trust, ",", support_strength, ",", abandonment_risk, ",", justice_resilience
  end do
end program abandonment_risk_dynamics
