program dashboard_score_dynamics
  implicit none

  integer, parameter :: steps = 60
  integer :: t
  real :: exposure, recovery, adaptive, buffer, justice
  real :: threshold_risk, missingness
  real :: naive_score, threshold_adjusted, uncertainty_adjusted

  exposure = 0.62
  recovery = 0.70
  adaptive = 0.58
  buffer = 0.64
  justice = 0.50
  threshold_risk = 0.46
  missingness = 0.18

  print *, "time,naive_score,threshold_adjusted_score,uncertainty_adjusted_score,threshold_risk,missingness"

  do t = 1, steps
     if (t == 20 .or. t == 42) then
        threshold_risk = min(1.0, threshold_risk + 0.08)
        missingness = min(1.0, missingness + 0.03)
     else
        threshold_risk = min(1.0, threshold_risk + 0.002)
        missingness = max(0.0, missingness - 0.001)
     end if

     naive_score = 0.17 * exposure + 0.18 * recovery + 0.19 * adaptive + 0.16 * buffer + 0.16 * justice
     threshold_adjusted = naive_score - 0.09 * threshold_risk
     uncertainty_adjusted = threshold_adjusted - 0.05 * missingness

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", naive_score, ",", threshold_adjusted, ",", uncertainty_adjusted, ",", threshold_risk, ",", missingness
  end do
end program dashboard_score_dynamics
