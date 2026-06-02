program adaptive_capacity_viability
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: capacity, vulnerability, rigidity, exposure, slack, trust
  real :: viability, seasonal, shock, disturbance, response_space

  capacity = 0.58
  vulnerability = 0.62
  rigidity = 0.55
  exposure = 0.70
  slack = 0.50
  trust = 0.57
  viability = 1.0

  print *, "time,disturbance,adaptive_capacity,rigidity,response_space,viability,threshold_flag"

  do t = 1, steps
     seasonal = 0.04 + 0.025 * sin(real(t) / 8.0)

     if (mod(t, 10) == 0) then
        shock = 0.22
     else
        shock = 0.0
     end if

     disturbance = 0.26 + seasonal + shock + 0.18 * exposure

     capacity = capacity + 0.010 + 0.006 * 0.50 - 0.010 * rigidity
     if (capacity < 0.0) capacity = 0.0
     if (capacity > 1.2) capacity = 1.2

     rigidity = rigidity + 0.010 + 0.004 * disturbance - 0.006 * 0.50
     if (rigidity < 0.0) rigidity = 0.0
     if (rigidity > 1.0) rigidity = 1.0

     response_space = capacity + 0.35 * slack + 0.25 * trust - rigidity - 0.25 * vulnerability

     viability = viability - 0.46 * disturbance + 0.25 * capacity + 0.08 * response_space - 0.12 * rigidity
     if (viability < 0.0) viability = 0.0
     if (viability > 1.2) viability = 1.2

     if (viability < 0.45) then
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", disturbance, ",", capacity, ",", rigidity, ",", response_space, ",", viability, ",", "threshold risk"
     else
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", disturbance, ",", capacity, ",", rigidity, ",", response_space, ",", viability, ",", "viable margin"
     end if
  end do
end program adaptive_capacity_viability
