program governance_function_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: function_level, learning, flexibility, coordination, knowledge
  real :: legitimacy, accountability, dependency, equity_sensitivity
  real :: uncertainty_exposure, chronic_stress
  real :: shock, uncertainty, coordination_stress, legitimacy_pressure
  real :: information_stress, legal_stress, equity_burden, dependency_amplification
  real :: stress_load, response_capacity, accountability_gap, legitimacy_gap
  real :: equity_adjustment, equity_adjusted_function

  function_level = 0.77
  learning = 0.78
  flexibility = 0.76
  coordination = 0.80
  knowledge = 0.74
  legitimacy = 0.72
  accountability = 0.74
  dependency = 0.76
  equity_sensitivity = 0.88
  uncertainty_exposure = 0.84
  chronic_stress = 0.66

  print *, "time,governance_function,stress_load,response_capacity,dependency,equity_adjusted"

  do t = 1, steps
     if (t == 12) then
        shock = 0.82
        uncertainty = 0.92
        coordination_stress = 0.70
        legitimacy_pressure = 0.66
        information_stress = 0.78
        legal_stress = 0.64
        equity_burden = 0.82
        dependency_amplification = 0.76
     else
        shock = 0.06
        uncertainty = 0.12
        coordination_stress = 0.10
        legitimacy_pressure = 0.10
        information_stress = 0.10
        legal_stress = 0.09 + 0.0015 * real(t)
        equity_burden = 0.22
        dependency_amplification = 0.12
     end if

     stress_load = 0.16 * shock + 0.17 * uncertainty + 0.17 * coordination_stress
     stress_load = stress_load + 0.15 * legitimacy_pressure + 0.13 * information_stress
     stress_load = stress_load + 0.12 * legal_stress + 0.10 * dependency_amplification
     stress_load = stress_load + 0.08 * dependency

     response_capacity = 0.18 * learning + 0.14 * flexibility + 0.18 * coordination
     response_capacity = response_capacity + 0.15 * knowledge + 0.16 * legitimacy
     response_capacity = response_capacity + 0.15 * accountability - 0.14 * uncertainty_exposure
     response_capacity = response_capacity - 0.12 * chronic_stress - 0.10 * dependency
     response_capacity = max(0.0, min(1.0, response_capacity))

     accountability_gap = max(0.0, flexibility - accountability)
     legitimacy_gap = max(0.0, 0.74 - legitimacy)
     equity_adjustment = 0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40)

     function_level = function_level - 0.33 * stress_load + 0.18 * response_capacity
     function_level = function_level + 0.09 * learning + 0.07 * flexibility + 0.09 * coordination
     function_level = function_level + 0.08 * knowledge + 0.08 * legitimacy + 0.08 * accountability
     function_level = function_level - 0.05 * dependency - 0.08 * accountability_gap
     function_level = function_level - 0.06 * legitimacy_gap
     function_level = max(0.0, min(1.0, function_level))

     dependency = max(0.0, min(1.0, dependency + 0.020 * stress_load - 0.011 * response_capacity))
     equity_adjusted_function = max(0.0, min(1.0, function_level * equity_adjustment))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", stress_load, ",", response_capacity, &
        ",", dependency, ",", equity_adjusted_function
  end do
end program governance_function_dynamics
