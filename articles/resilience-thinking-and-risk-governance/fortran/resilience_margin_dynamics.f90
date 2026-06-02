program resilience_margin_dynamics
  implicit none

  integer, parameter :: steps = 84
  integer :: t
  real :: margin, disturbance, governance_response, adaptive_response
  real :: vulnerability_amplification, disturbance_effect
  real :: vulnerability, exposure, governance, adaptive, learning

  margin = 0.6667
  vulnerability = 0.64
  exposure = 0.78
  governance = 0.4591
  adaptive = 0.58
  learning = 0.52

  print *, "time,disturbance,resilience_margin,threshold_flag"

  do t = 1, steps
     disturbance = 0.05 + 0.025 * sin(real(t) / 7.0)
     if (mod(t, 8) == 0) disturbance = disturbance + 0.76

     governance_response = 0.018 * governance * (1.0 - 0.35 * 0.72)
     adaptive_response = 0.014 * adaptive + 0.010 * learning
     vulnerability_amplification = 0.020 * vulnerability + 0.010 * exposure
     disturbance_effect = disturbance * (0.35 + 0.55 * exposure)

     margin = margin - disturbance_effect - vulnerability_amplification + governance_response + adaptive_response

     if (margin < 0.75) then
        print '(I0,A,F7.4,A,F8.4,A,A)', t, ",", disturbance, ",", margin, ",", "threshold risk"
     else
        print '(I0,A,F7.4,A,F8.4,A,A)', t, ",", disturbance, ",", margin, ",", "viable margin"
     end if
  end do
end program resilience_margin_dynamics
