program development_quality_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: development_quality, adaptive, equity_sensitivity, resource_pressure, governance_constraint
  real :: climate_exposure, ecological_stress, social_vulnerability, economic_fragility, infrastructure_exposure
  real :: shock, climate, overshoot, economic, infrastructure, governance, equity_burden, pressure_spike
  real :: stress_load, response_capacity, boundary_penalty, equity_adjustment

  development_quality = 0.76
  climate_exposure = 0.84
  ecological_stress = 0.62
  social_vulnerability = 0.88
  economic_fragility = 0.66
  infrastructure_exposure = 0.78
  governance_constraint = 0.70
  adaptive = 0.74
  equity_sensitivity = 0.92
  resource_pressure = 0.78

  print *, "time,development_quality,stress_load,response_capacity,resource_pressure,equity_adjusted_quality"

  do t = 1, steps
     if (t == 12) then
        shock = 0.84
        climate = 0.90
        overshoot = 0.62
        economic = 0.68
        infrastructure = 0.76
        governance = 0.70
        equity_burden = 0.92
        pressure_spike = 0.76
     else
        shock = 0.06
        climate = 0.11
        overshoot = 0.11 + 0.0015 * real(t)
        economic = 0.10
        infrastructure = 0.10
        governance = 0.11
        equity_burden = 0.22
        pressure_spike = 0.12
     end if

     stress_load = 0.16 * shock + 0.16 * climate + 0.18 * overshoot + 0.13 * economic + 0.13 * infrastructure + 0.12 * governance + 0.12 * pressure_spike + 0.08 * resource_pressure
     response_capacity = max(0.0, min(1.0, 0.18 * adaptive + 0.16 * (1.0 - social_vulnerability) + 0.15 * (1.0 - economic_fragility) + 0.15 * (1.0 - infrastructure_exposure) + 0.15 * (1.0 - governance_constraint) + 0.14 * (1.0 - ecological_stress) + 0.07 * (1.0 - climate_exposure)))

     boundary_penalty = max(0.0, resource_pressure + pressure_spike - 1.30) * 0.11
     equity_adjustment = 0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40)

     development_quality = max(0.0, min(1.0, development_quality - 0.32 * stress_load + 0.20 * response_capacity + 0.10 * adaptive - 0.09 * resource_pressure - 0.08 * governance_constraint - boundary_penalty))
     resource_pressure = max(0.0, min(1.0, resource_pressure + 0.015 * overshoot + 0.010 * pressure_spike - 0.010 * response_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", development_quality, ",", stress_load, ",", response_capacity, ",", resource_pressure, ",", max(0.0, min(1.0, development_quality * equity_adjustment))
  end do
end program development_quality_dynamics
