program service_resilience_margin
  implicit none

  integer, parameter :: steps = 100
  integer :: t
  real :: condition, functional_capacity, redundancy, memory, governance, exposure, access
  real :: seasonal, shock, disturbance, repair, erosion, service_flow, margin

  condition = 0.62
  functional_capacity = 0.58
  redundancy = 0.48
  memory = 0.52
  governance = 0.55
  exposure = 0.70
  access = 0.52

  print *, "time,disturbance,ecosystem_condition,functional_capacity,service_flow,resilience_margin,threshold_flag"

  do t = 1, steps
     seasonal = 0.04 + 0.020 * sin(real(t) / 8.0)

     if (t == 22 .or. t == 45 .or. t == 67 .or. t == 84) then
        shock = 0.25
     else
        shock = 0.0
     end if

     disturbance = seasonal + shock + 0.18 * exposure
     repair = 0.010 * redundancy + 0.009 * memory + 0.008 * governance
     erosion = disturbance * (0.42 + exposure)

     condition = condition - 0.045 * erosion + repair
     if (condition < 0.01) condition = 0.01
     if (condition > 1.0) condition = 1.0

     functional_capacity = functional_capacity - 0.030 * erosion + 0.006 * redundancy
     if (functional_capacity < 0.01) functional_capacity = 0.01
     if (functional_capacity > 1.0) functional_capacity = 1.0

     service_flow = condition * functional_capacity * (1.0 - 0.35 * disturbance)
     if (service_flow < 0.0) service_flow = 0.0
     if (service_flow > 1.0) service_flow = 1.0

     margin = condition + functional_capacity + redundancy + memory + governance + 0.35 * access - disturbance - exposure

     if (margin < 1.30) then
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", disturbance, ",", condition, ",", functional_capacity, ",", service_flow, ",", margin, ",", "threshold risk"
     else
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", disturbance, ",", condition, ",", functional_capacity, ",", service_flow, ",", margin, ",", "viable margin"
     end if
  end do
end program service_resilience_margin
