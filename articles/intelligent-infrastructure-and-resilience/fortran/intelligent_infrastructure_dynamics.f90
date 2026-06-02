program intelligent_infrastructure_dynamics
  implicit none

  integer, parameter :: steps = 96
  integer :: t
  real :: function_level, backlog, operator_strain, data_trust
  real :: physical, monitoring, maintenance, cyber_security, redundancy, governance, equity, ecology
  real :: shock, climate_stress, cyber_stress, data_stress, dependency_stress
  real :: maintenance_stress, operator_stress, equity_pressure, governance_pressure
  real :: disturbance, intelligence_value, response_capacity, fragility_gap
  real :: backlog_growth, maintenance_investment, strain_increase, strain_recovery
  real :: equity_access, resilience_score

  function_level = 0.87
  physical = 0.84
  monitoring = 0.84
  maintenance = 0.86
  cyber_security = 0.86
  redundancy = 0.84
  governance = 0.86
  equity = 0.84
  ecology = 0.82
  backlog = 0.30
  operator_strain = 0.34
  data_trust = monitoring

  print *, "time,function,intelligence_value,response_capacity,fragility_gap,maintenance_backlog,data_trust,operator_strain,equity_access,resilience_score"

  do t = 1, steps
     if (t == 10) then
        shock = 0.66
        climate_stress = 0.92
        cyber_stress = 0.42
        data_stress = 0.48
        dependency_stress = 0.64
        maintenance_stress = 0.62
        operator_stress = 0.70
        equity_pressure = 0.86
        governance_pressure = 0.66
     else
        shock = 0.06
        climate_stress = 0.08 + 0.001 * real(t)
        cyber_stress = 0.06
        data_stress = 0.06
        dependency_stress = 0.08
        maintenance_stress = 0.10 + 0.0015 * real(t)
        operator_stress = 0.08
        equity_pressure = 0.09
        governance_pressure = 0.08
     end if

     disturbance = 0.11 * shock + 0.14 * climate_stress + 0.13 * cyber_stress
     disturbance = disturbance + 0.12 * data_stress + 0.13 * dependency_stress
     disturbance = disturbance + 0.13 * maintenance_stress + 0.10 * operator_stress
     disturbance = disturbance + 0.07 * equity_pressure + 0.07 * governance_pressure

     intelligence_value = 0.23 * data_trust + 0.21 * maintenance + 0.16 * governance
     intelligence_value = intelligence_value + 0.14 * equity + 0.14 * ecology + 0.12 * monitoring
     intelligence_value = max(0.0, min(1.0, intelligence_value))

     response_capacity = 0.17 * physical + 0.17 * redundancy + 0.17 * cyber_security
     response_capacity = response_capacity + 0.17 * governance + 0.13 * maintenance
     response_capacity = response_capacity + 0.12 * equity + 0.07 * ecology
     response_capacity = max(0.0, min(1.0, response_capacity))

     fragility_gap = max(0.0, disturbance + 0.25 * backlog + 0.14 * cyber_stress + 0.12 * dependency_stress - response_capacity)

     backlog_growth = 0.018 + 0.030 * climate_stress + 0.024 * disturbance + 0.016 * maintenance_stress
     maintenance_investment = 0.046 * maintenance + 0.030 * governance + 0.014 * physical
     backlog = max(0.0, min(1.0, backlog + backlog_growth - maintenance_investment))

     data_trust = data_trust - 0.11 * data_stress - 0.08 * cyber_stress - 0.04 * dependency_stress
     data_trust = data_trust + 0.060 * governance + 0.040 * cyber_security + 0.030 * monitoring
     data_trust = max(0.0, min(1.0, data_trust))

     strain_increase = 0.15 * disturbance + 0.13 * fragility_gap + 0.09 * backlog
     strain_increase = strain_increase + 0.08 * dependency_stress + 0.05 * operator_stress
     strain_recovery = 0.08 * governance + 0.06 * redundancy + 0.04 * maintenance
     operator_strain = max(0.0, min(1.0, operator_strain + strain_increase - strain_recovery))

     equity_access = 0.40 * equity + 0.18 * governance + 0.17 * redundancy + 0.12 * ecology
     equity_access = equity_access + 0.08 * physical - 0.11 * fragility_gap - 0.07 * operator_strain - 0.06 * equity_pressure
     equity_access = max(0.0, min(1.0, equity_access))

     function_level = function_level - 0.27 * disturbance - 0.16 * fragility_gap - 0.11 * backlog
     function_level = function_level + 0.17 * response_capacity + 0.15 * intelligence_value
     function_level = function_level + 0.10 * equity_access + 0.05 * data_trust - 0.09 * operator_strain
     function_level = max(0.0, min(1.0, function_level))

     resilience_score = 0.18 * function_level + 0.15 * response_capacity + 0.14 * intelligence_value
     resilience_score = resilience_score + 0.12 * data_trust + 0.12 * equity_access
     resilience_score = resilience_score + 0.10 * ecology + 0.10 * (1.0 - backlog) + 0.09 * (1.0 - operator_strain)
     resilience_score = max(0.0, min(1.0, resilience_score))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", intelligence_value, ",", response_capacity, ",", fragility_gap, &
        ",", backlog, ",", data_trust, ",", operator_strain, ",", equity_access, ",", resilience_score
  end do
end program intelligent_infrastructure_dynamics
