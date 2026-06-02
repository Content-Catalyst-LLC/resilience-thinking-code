program stock_flow_margin
  implicit none

  integer, parameter :: steps = 100
  integer :: t
  real :: vulnerability, disturbance, margin
  real :: reinforcing, repair, adaptive, buffer, threshold

  vulnerability = 0.35
  reinforcing = 0.18
  repair = 0.25
  adaptive = 0.70
  buffer = 0.65
  threshold = 0.25

  print *, "time,disturbance,vulnerability_stock,resilience_margin,threshold_flag"

  do t = 1, steps
     disturbance = 0.06 + 0.03 * sin(real(t) / 6.0)

     if (t == 20 .or. t == 40 .or. t == 65 .or. t == 83) then
        disturbance = disturbance + 0.30
     end if

     vulnerability = vulnerability + reinforcing * vulnerability + 0.35 * disturbance - repair * disturbance - 0.012 * adaptive
     if (vulnerability < 0.0) vulnerability = 0.0
     if (vulnerability > 2.0) vulnerability = 2.0

     margin = buffer + adaptive - vulnerability - 0.25 * disturbance

     if (margin < threshold) then
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", disturbance, ",", vulnerability, ",", margin, ",", "threshold risk"
     else
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", disturbance, ",", vulnerability, ",", margin, ",", "viable margin"
     end if
  end do
end program stock_flow_margin
