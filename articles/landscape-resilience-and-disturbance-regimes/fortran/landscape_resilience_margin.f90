program landscape_resilience_margin
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: condition, exposure, buffer_capacity, memory, recovery, refugia, social_exposure
  real :: disturbance, seasonal, shock, margin

  condition = 0.78
  exposure = 0.66
  buffer_capacity = 0.70
  memory = 0.72
  recovery = 0.64
  refugia = 1.0
  social_exposure = 0.54
  disturbance = 0.08 + 0.10 * exposure

  print *, "time,condition,disturbance,resilience_margin,threshold_flag"

  do t = 1, steps
     seasonal = 0.04 + 0.025 * sin(real(t) / 7.0)

     if (t == 18 .or. t == 36 .or. t == 55 .or. t == 70) then
        shock = 0.24
     else
        shock = 0.0
     end if

     disturbance = disturbance + 0.32 + seasonal + shock + 0.18 * 0.58 + 0.22 * exposure - 0.26 * buffer_capacity - 0.12 * refugia - 0.06 * 0.48
     if (disturbance < 0.0) disturbance = 0.0
     if (disturbance > 1.4) disturbance = 1.4

     condition = condition - 0.055 * disturbance + 0.018 * memory + 0.015 * recovery + 0.008 * refugia + 0.006 * 0.48
     if (condition < 0.0) condition = 0.0
     if (condition > 1.0) condition = 1.0

     margin = condition + buffer_capacity + memory + recovery + 0.25 * refugia + 0.20 * 0.48 - disturbance - exposure - 0.30 * social_exposure

     if (margin < 0.75) then
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", condition, ",", disturbance, ",", margin, ",", "threshold risk"
     else
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", condition, ",", disturbance, ",", margin, ",", "viable margin"
     end if
  end do
end program landscape_resilience_margin
