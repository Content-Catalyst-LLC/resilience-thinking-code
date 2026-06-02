program functional_resilience_margin
  implicit none

  integer, parameter :: steps = 100
  integer :: t
  real :: functional_output, redundancy, response_diversity
  real :: memory, connectivity, exposure
  real :: seasonal, shock, disturbance, margin

  functional_output = 2.4
  redundancy = 4.0
  response_diversity = 0.055
  memory = 0.60
  connectivity = 0.54
  exposure = 0.66

  print *, "time,functional_output,redundancy,response_diversity,disturbance,resilience_margin,threshold_flag"

  do t = 1, steps
     seasonal = 0.055 + 0.025 * sin(real(t) / 9.0)

     if (t == 24 .or. t == 47 .or. t == 70 .or. t == 88) then
        shock = 0.32
     else
        shock = 0.0
     end if

     disturbance = seasonal + shock + 0.18 * exposure

     functional_output = functional_output - 0.030 * disturbance + 0.010 * memory
     if (functional_output < 0.0) functional_output = 0.0

     redundancy = redundancy - 0.018 * disturbance + 0.004 * connectivity
     if (redundancy < 0.0) redundancy = 0.0

     response_diversity = response_diversity - 0.003 * disturbance + 0.001 * memory
     if (response_diversity < 0.0) response_diversity = 0.0

     margin = functional_output + 0.055 * redundancy + response_diversity + memory + connectivity - disturbance - exposure

     if (margin < 1.20) then
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", functional_output, ",", redundancy, ",", response_diversity, ",", disturbance, ",", margin, ",", "threshold risk"
     else
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", functional_output, ",", redundancy, ",", response_diversity, ",", disturbance, ",", margin, ",", "viable margin"
     end if
  end do
end program functional_resilience_margin
