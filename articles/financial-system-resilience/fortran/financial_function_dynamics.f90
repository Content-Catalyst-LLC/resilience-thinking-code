program financial_function_dynamics
  implicit none

  integer, parameter :: steps = 90
  integer :: t
  real :: financial_function, governance_capacity, inclusion_sensitivity
  real :: leverage_pressure, liquidity_fragility, common_asset_exposure
  real :: operational_dependency, climate_financial_exposure, nonbank_exposure, household_fragility
  real :: shock, credit_loss, liquidity_run, fire_sale, operational, climate
  real :: nonbank, household, policy_stress, inclusion_burden
  real :: systemic_exposure, stress_load, stabilizing_capacity
  real :: inclusion_penalty, liquidity_penalty, operational_penalty, inclusion_adjusted_function

  financial_function = 0.76
  leverage_pressure = 0.82
  liquidity_fragility = 0.88
  common_asset_exposure = 0.74
  operational_dependency = 0.70
  climate_financial_exposure = 0.66
  nonbank_exposure = 0.64
  household_fragility = 0.70
  governance_capacity = 0.74
  inclusion_sensitivity = 0.78

  print *, "time,financial_function,stress_load,stabilizing_capacity,liquidity_fragility,household_fragility,inclusion_adjusted_function"

  do t = 1, steps
     if (t == 12) then
        shock = 0.88
        credit_loss = 0.70
        liquidity_run = 0.96
        fire_sale = 0.82
        operational = 0.66
        climate = 0.60
        nonbank = 0.68
        household = 0.78
        policy_stress = 0.82
        inclusion_burden = 0.78
     else
        shock = 0.06
        credit_loss = 0.10
        liquidity_run = 0.10 + 0.001 * real(t)
        fire_sale = 0.10
        operational = 0.10
        climate = 0.10 + 0.001 * real(t)
        nonbank = 0.10
        household = 0.11
        policy_stress = 0.10
        inclusion_burden = 0.24
     end if

     systemic_exposure = 0.14 * leverage_pressure + 0.15 * liquidity_fragility
     systemic_exposure = systemic_exposure + 0.14 * common_asset_exposure + 0.13 * operational_dependency
     systemic_exposure = systemic_exposure + 0.13 * climate_financial_exposure + 0.13 * nonbank_exposure
     systemic_exposure = systemic_exposure + 0.13 * household_fragility

     stress_load = 0.10 * shock + 0.12 * credit_loss + 0.14 * liquidity_run + 0.13 * fire_sale
     stress_load = stress_load + 0.12 * operational + 0.12 * climate + 0.12 * nonbank
     stress_load = stress_load + 0.10 * household + 0.10 * policy_stress + 0.08 * systemic_exposure

     stabilizing_capacity = 0.14 * (1.0 - leverage_pressure) + 0.14 * (1.0 - liquidity_fragility)
     stabilizing_capacity = stabilizing_capacity + 0.13 * (1.0 - common_asset_exposure)
     stabilizing_capacity = stabilizing_capacity + 0.12 * (1.0 - operational_dependency)
     stabilizing_capacity = stabilizing_capacity + 0.12 * (1.0 - climate_financial_exposure)
     stabilizing_capacity = stabilizing_capacity + 0.12 * (1.0 - nonbank_exposure)
     stabilizing_capacity = stabilizing_capacity + 0.12 * (1.0 - household_fragility)
     stabilizing_capacity = stabilizing_capacity + 0.18 * governance_capacity
     stabilizing_capacity = max(0.0, min(1.0, stabilizing_capacity))

     inclusion_penalty = max(0.0, inclusion_burden + household_fragility - 1.35) * 0.10
     liquidity_penalty = max(0.0, liquidity_fragility + liquidity_run - 1.35) * 0.08
     operational_penalty = max(0.0, operational_dependency + operational - 1.35) * 0.07

     financial_function = financial_function - 0.32 * stress_load + 0.22 * stabilizing_capacity
     financial_function = financial_function + 0.08 * governance_capacity - inclusion_penalty - liquidity_penalty - operational_penalty
     financial_function = max(0.0, min(1.0, financial_function))

     liquidity_fragility = max(0.0, min(1.0, liquidity_fragility + 0.012 * liquidity_run + 0.010 * fire_sale - 0.010 * stabilizing_capacity))
     household_fragility = max(0.0, min(1.0, household_fragility + 0.012 * household + 0.010 * inclusion_burden - 0.010 * stabilizing_capacity))
     inclusion_adjusted_function = max(0.0, min(1.0, financial_function * (0.72 + 0.28 * (1.0 - inclusion_burden + inclusion_sensitivity * 0.40))))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", financial_function, ",", stress_load, ",", stabilizing_capacity, &
        ",", liquidity_fragility, ",", household_fragility, ",", inclusion_adjusted_function
  end do
end program financial_function_dynamics
