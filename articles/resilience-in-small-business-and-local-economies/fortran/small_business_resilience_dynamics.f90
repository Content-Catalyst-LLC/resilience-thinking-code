program small_business_resilience_dynamics
  implicit none

  integer, parameter :: steps = 96
  integer :: t
  real :: function_level, cash, owner_strain, customer_demand
  real :: workforce, supplier, digital, community, public_support, equity
  real :: shock, demand_loss, supplier_disruption, digital_disruption
  real :: rent_debt_pressure, workforce_stress, insurance_gap, support_delay, inequality_pressure
  real :: adaptive_capacity, shock_load, fragility_gap, revenue_pressure
  real :: strain_increase, strain_recovery, equity_adjusted_function, survival_risk

  function_level = 0.80
  cash = 0.36
  owner_strain = 0.64
  customer_demand = 0.72 + 0.10 * 0.88
  workforce = 0.58
  supplier = 0.50
  digital = 0.56
  community = 0.88
  public_support = 0.48
  equity = 0.46

  print *, "time,function,cash_runway,customer_demand,owner_strain,fragility_gap,equity_adjusted_function,survival_risk"

  do t = 1, steps
     if (t == 8) then
        shock = 0.58
        demand_loss = 0.86
        supplier_disruption = 0.42
        digital_disruption = 0.38
        rent_debt_pressure = 0.50
        workforce_stress = 0.46
        insurance_gap = 0.48
        support_delay = 0.52
        inequality_pressure = 0.64
     else
        shock = 0.06
        demand_loss = 0.10
        supplier_disruption = 0.08
        digital_disruption = 0.07
        rent_debt_pressure = 0.10 + 0.001 * real(t)
        workforce_stress = 0.09
        insurance_gap = 0.08
        support_delay = 0.10
        inequality_pressure = 0.12
     end if

     adaptive_capacity = 0.16 * cash + 0.16 * workforce + 0.14 * supplier + 0.14 * digital
     adaptive_capacity = adaptive_capacity + 0.16 * community + 0.14 * public_support + 0.10 * equity

     shock_load = 0.12 * shock + 0.15 * demand_loss + 0.13 * supplier_disruption
     shock_load = shock_load + 0.12 * digital_disruption + 0.15 * rent_debt_pressure
     shock_load = shock_load + 0.13 * workforce_stress + 0.10 * insurance_gap + 0.10 * support_delay

     fragility_gap = max(0.0, shock_load - adaptive_capacity)

     revenue_pressure = 0.28 * shock_load + 0.18 * fragility_gap - 0.08 * community - 0.06 * digital
     revenue_pressure = max(0.0, min(1.0, revenue_pressure))

     customer_demand = max(0.0, min(1.0, customer_demand - 0.16 * demand_loss + 0.06 * community + 0.03 * digital))
     cash = max(0.0, min(1.0, cash - 0.14 * revenue_pressure - 0.06 * rent_debt_pressure - 0.04 * insurance_gap + 0.07 * public_support + 0.04 * equity))

     strain_increase = 0.18 * shock_load + 0.15 * fragility_gap + 0.08 * max(0.0, 0.45 - cash)
     strain_recovery = 0.08 * workforce + 0.05 * community + 0.03 * public_support
     owner_strain = max(0.0, min(1.0, owner_strain + strain_increase - strain_recovery))

     function_level = function_level - 0.30 * shock_load - 0.16 * fragility_gap
     function_level = function_level + 0.16 * adaptive_capacity + 0.12 * cash + 0.09 * customer_demand - 0.10 * owner_strain
     function_level = max(0.0, min(1.0, function_level))

     equity_adjusted_function = max(0.0, min(1.0, function_level * (0.72 + 0.28 * equity) - 0.08 * owner_strain - 0.05 * inequality_pressure))
     survival_risk = max(0.0, min(1.0, 0.35 * (1.0 - function_level) + 0.35 * (1.0 - cash) + 0.20 * owner_strain + 0.10 * fragility_gap))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", cash, ",", customer_demand, ",", owner_strain, &
        ",", fragility_gap, ",", equity_adjusted_function, ",", survival_risk
  end do
end program small_business_resilience_dynamics
