program food_water_performance_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: performance, infrastructure_support, ecosystem_condition, adaptive_capacity
  real :: climate_exposure, market_exposure, resource_coupling
  real :: climate, market, infra_disruption, ecosystem_stress, stress_load, response_capacity

  performance = 0.82
  infrastructure_support = 0.68
  ecosystem_condition = 0.56
  adaptive_capacity = 0.70
  climate_exposure = 0.76
  market_exposure = 0.58
  resource_coupling = 0.80

  print *, "time,performance,stress_load,response_capacity,resource_coupling"

  do t = 1, steps
     if (t == 12) then
        climate = 0.84
        market = 0.62
        infra_disruption = 0.54
        ecosystem_stress = 0.78
     else if (t == 27) then
        climate = 0.82
        market = 0.58
        infra_disruption = 0.76
        ecosystem_stress = 0.70
     else if (t == 42) then
        climate = 0.56
        market = 0.86
        infra_disruption = 0.58
        ecosystem_stress = 0.50
     else if (t == 56) then
        climate = 0.58
        market = 0.52
        infra_disruption = 0.72
        ecosystem_stress = 0.68
     else
        climate = 0.07
        market = 0.13
        infra_disruption = 0.10
        ecosystem_stress = 0.14 + 0.0025 * real(t)
     end if

     stress_load = 0.30 * climate + 0.20 * market + 0.18 * infra_disruption + 0.20 * ecosystem_stress + 0.12 * resource_coupling
     response_capacity = max(0.0, min(1.0, 0.30 * infrastructure_support + 0.28 * ecosystem_condition + 0.28 * adaptive_capacity - 0.20 * climate_exposure - 0.14 * market_exposure - 0.14 * resource_coupling))

     performance = max(0.0, min(1.0, performance - 0.34 * stress_load + 0.21 * response_capacity + 0.10 * infrastructure_support + 0.11 * ecosystem_condition + 0.09 * adaptive_capacity - 0.05 * resource_coupling))
     resource_coupling = max(0.0, min(1.0, resource_coupling + 0.018 * stress_load - 0.012 * response_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", performance, ",", stress_load, ",", response_capacity, ",", resource_coupling
  end do
end program food_water_performance_dynamics
