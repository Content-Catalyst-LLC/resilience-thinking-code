program supply_chain_flow_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: flow, coordination, equity_sensitivity
  real :: supplier_concentration, chokepoint, inventory_thinness
  real :: climate_exposure, cyber_dependency, labor_vulnerability, infrastructure_fragility
  real :: shock, supplier_failure, logistics, demand, inventory, cyber, climate
  real :: labor, coordination_stress, equity_burden
  real :: exposure, disruption_load, adaptive_response, equity_penalty
  real :: infrastructure_penalty, cyber_penalty, equity_adjusted_flow

  flow = 0.78
  supplier_concentration = 0.74
  chokepoint = 0.88
  inventory_thinness = 0.82
  climate_exposure = 0.74
  cyber_dependency = 0.76
  labor_vulnerability = 0.72
  infrastructure_fragility = 0.86
  coordination = 0.70
  equity_sensitivity = 0.76

  print *, "time,flow_performance,disruption_load,adaptive_response,inventory_thinness,supplier_concentration,equity_adjusted_flow"

  do t = 1, steps
     if (t == 12) then
        shock = 0.86
        supplier_failure = 0.62
        logistics = 0.94
        demand = 0.72
        inventory = 0.82
        cyber = 0.66
        climate = 0.70
        labor = 0.72
        coordination_stress = 0.82
        equity_burden = 0.76
     else
        shock = 0.06
        supplier_failure = 0.10
        logistics = 0.10
        demand = 0.11
        inventory = 0.10 + 0.001 * real(t)
        cyber = 0.10
        climate = 0.11
        labor = 0.10
        coordination_stress = 0.10
        equity_burden = 0.22
     end if

     exposure = 0.14 * supplier_concentration + 0.14 * chokepoint + 0.13 * inventory_thinness
     exposure = exposure + 0.13 * climate_exposure + 0.13 * cyber_dependency
     exposure = exposure + 0.13 * labor_vulnerability + 0.14 * infrastructure_fragility

     disruption_load = 0.10 * shock + 0.13 * supplier_failure + 0.13 * logistics
     disruption_load = disruption_load + 0.11 * demand + 0.12 * inventory + 0.12 * cyber
     disruption_load = disruption_load + 0.12 * climate + 0.10 * labor + 0.10 * coordination_stress
     disruption_load = disruption_load + 0.08 * exposure

     adaptive_response = 0.14 * (1.0 - supplier_concentration) + 0.14 * (1.0 - chokepoint)
     adaptive_response = adaptive_response + 0.12 * (1.0 - inventory_thinness)
     adaptive_response = adaptive_response + 0.12 * (1.0 - climate_exposure)
     adaptive_response = adaptive_response + 0.12 * (1.0 - cyber_dependency)
     adaptive_response = adaptive_response + 0.12 * (1.0 - labor_vulnerability)
     adaptive_response = adaptive_response + 0.12 * (1.0 - infrastructure_fragility)
     adaptive_response = adaptive_response + 0.16 * coordination
     adaptive_response = max(0.0, min(1.0, adaptive_response))

     equity_penalty = max(0.0, equity_burden + labor_vulnerability - 1.35) * 0.10
     infrastructure_penalty = max(0.0, infrastructure_fragility + logistics + climate - 2.00) * 0.07
     cyber_penalty = max(0.0, cyber_dependency + cyber - 1.35) * 0.07

     flow = flow - 0.32 * disruption_load + 0.22 * adaptive_response + 0.08 * coordination
     flow = flow - equity_penalty - infrastructure_penalty - cyber_penalty
     flow = max(0.0, min(1.0, flow))

     inventory_thinness = max(0.0, min(1.0, inventory_thinness + 0.012 * demand + 0.012 * inventory - 0.010 * adaptive_response))
     supplier_concentration = max(0.0, min(1.0, supplier_concentration + 0.010 * supplier_failure - 0.008 * adaptive_response))
     equity_adjusted_flow = max(0.0, min(1.0, flow * (0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40))))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", flow, ",", disruption_load, ",", adaptive_response, &
        ",", inventory_thinness, ",", supplier_concentration, ",", equity_adjusted_flow
  end do
end program supply_chain_flow_dynamics
