program economic_function_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: economic_function, institutional_capacity, equity_sensitivity
  real :: sector_concentration, household_fragility, firm_fragility
  real :: financial_exposure, labor_rigidity, infrastructure_exposure, climate_exposure
  real :: shock, demand, supply, finance, labor, infrastructure, climate, fiscal, equity_burden
  real :: fragility, stress_load, adaptive_response, equity_penalty, fiscal_penalty, equity_adjusted_function

  economic_function = 0.74
  sector_concentration = 0.88
  household_fragility = 0.70
  firm_fragility = 0.72
  financial_exposure = 0.64
  labor_rigidity = 0.70
  infrastructure_exposure = 0.68
  climate_exposure = 0.62
  institutional_capacity = 0.70
  equity_sensitivity = 0.86

  print *, "time,economic_function,stress_load,adaptive_response,household_fragility,firm_fragility,equity_adjusted_function"

  do t = 1, steps
     if (t == 12) then
        shock = 0.84
        demand = 0.82
        supply = 0.70
        finance = 0.72
        labor = 0.88
        infrastructure = 0.60
        climate = 0.56
        fiscal = 0.72
        equity_burden = 0.88
     else
        shock = 0.06
        demand = 0.11
        supply = 0.10
        finance = 0.09 + 0.001 * real(t)
        labor = 0.10
        infrastructure = 0.10
        climate = 0.11
        fiscal = 0.10 + 0.001 * real(t)
        equity_burden = 0.22
     end if

     fragility = 0.13 * sector_concentration + 0.15 * household_fragility
     fragility = fragility + 0.13 * firm_fragility + 0.14 * financial_exposure
     fragility = fragility + 0.12 * labor_rigidity + 0.13 * infrastructure_exposure
     fragility = fragility + 0.13 * climate_exposure

     stress_load = 0.13 * shock + 0.13 * demand + 0.13 * supply + 0.14 * finance
     stress_load = stress_load + 0.12 * labor + 0.13 * infrastructure + 0.12 * climate
     stress_load = stress_load + 0.12 * fiscal + 0.08 * fragility

     adaptive_response = 0.16 * (1.0 - sector_concentration)
     adaptive_response = adaptive_response + 0.14 * (1.0 - household_fragility)
     adaptive_response = adaptive_response + 0.14 * (1.0 - firm_fragility)
     adaptive_response = adaptive_response + 0.14 * (1.0 - financial_exposure)
     adaptive_response = adaptive_response + 0.13 * (1.0 - labor_rigidity)
     adaptive_response = adaptive_response + 0.13 * (1.0 - infrastructure_exposure)
     adaptive_response = adaptive_response + 0.12 * (1.0 - climate_exposure)
     adaptive_response = adaptive_response + 0.16 * institutional_capacity
     adaptive_response = max(0.0, min(1.0, adaptive_response))

     equity_penalty = max(0.0, equity_burden + household_fragility - 1.35) * 0.10
     fiscal_penalty = max(0.0, fiscal + financial_exposure - 1.35) * 0.07

     economic_function = economic_function - 0.32 * stress_load + 0.22 * adaptive_response
     economic_function = economic_function + 0.08 * institutional_capacity - equity_penalty - fiscal_penalty
     economic_function = max(0.0, min(1.0, economic_function))

     household_fragility = max(0.0, min(1.0, household_fragility + 0.012 * demand + 0.010 * labor + 0.010 * equity_burden - 0.010 * adaptive_response))
     firm_fragility = max(0.0, min(1.0, firm_fragility + 0.012 * supply + 0.012 * finance - 0.010 * adaptive_response))
     equity_adjusted_function = max(0.0, min(1.0, economic_function * (0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40))))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", economic_function, ",", stress_load, ",", adaptive_response, &
        ",", household_fragility, ",", firm_fragility, ",", equity_adjusted_function
  end do
end program economic_function_dynamics
