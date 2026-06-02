program function_under_disturbance
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, disturbance, redundancy, diversity, common_mode_risk

  function_level = 0.86
  redundancy = 0.72
  diversity = 0.70
  common_mode_risk = 0.34

  print *, "time,function_level,disturbance,redundancy,diversity,common_mode_risk"

  do t = 1, steps
     if (t == 25 .or. t == 55) then
        disturbance = 0.34
     else
        disturbance = 0.06
     end if

     function_level = min(1.0, max(0.0, &
        function_level - &
        0.42 * disturbance + &
        0.16 * redundancy + &
        0.14 * diversity - &
        0.12 * common_mode_risk))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", disturbance, ",", redundancy, ",", diversity, ",", common_mode_risk
  end do
end program function_under_disturbance
