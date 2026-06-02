program strategic_slack_dynamics
  implicit none

  integer, parameter :: steps = 90
  integer :: t
  real :: function_level, slack_stock, strain
  real :: financial, workforce, operational, knowledge, network, governance, ethics
  real :: shock, financial_stress, workforce_stress, operational_stress, knowledge_stress
  real :: network_stress, governance_stress, ethical_burden, consumption_pressure
  real :: disruption_load, adaptive_response, fragility_gap
  real :: strain_increase, strain_recovery, slack_consumption, slack_rebuilding
  real :: ethical_adjusted_function, resilience_score

  function_level = 0.84
  financial = 0.76
  workforce = 0.80
  operational = 0.78
  knowledge = 0.82
  network = 0.76
  governance = 0.82
  ethics = 0.84
  strain = 0.32
  slack_stock = 0.16 * financial + 0.16 * workforce + 0.15 * operational
  slack_stock = slack_stock + 0.15 * knowledge + 0.14 * network + 0.14 * governance + 0.10 * ethics

  print *, "time,function,slack_stock,adaptive_response,fragility_gap,workforce_strain,resilience_score"

  do t = 1, steps
     if (t == 10) then
        shock = 0.72
        financial_stress = 0.58
        workforce_stress = 0.54
        operational_stress = 0.76
        knowledge_stress = 0.50
        network_stress = 0.92
        governance_stress = 0.64
        ethical_burden = 0.68
        consumption_pressure = 0.78
     else
        shock = 0.06
        financial_stress = 0.10
        workforce_stress = 0.10
        operational_stress = 0.10
        knowledge_stress = 0.08 + 0.001 * real(t)
        network_stress = 0.10
        governance_stress = 0.09
        ethical_burden = 0.20
        consumption_pressure = 0.12
     end if

     disruption_load = 0.10 * shock + 0.13 * financial_stress + 0.15 * workforce_stress
     disruption_load = disruption_load + 0.14 * operational_stress + 0.12 * knowledge_stress
     disruption_load = disruption_load + 0.13 * network_stress + 0.11 * governance_stress + 0.12 * ethical_burden

     adaptive_response = 0.13 * financial + 0.17 * workforce + 0.14 * operational
     adaptive_response = adaptive_response + 0.15 * knowledge + 0.13 * network
     adaptive_response = adaptive_response + 0.16 * governance + 0.12 * ethics
     adaptive_response = max(0.0, min(1.0, adaptive_response))

     fragility_gap = max(0.0, disruption_load - slack_stock)

     strain_increase = 0.20 * disruption_load + 0.18 * fragility_gap
     strain_recovery = 0.10 * workforce + 0.08 * ethics + 0.04 * governance
     strain = max(0.0, min(1.0, strain + strain_increase - strain_recovery))

     function_level = function_level - 0.34 * disruption_load + 0.22 * adaptive_response
     function_level = function_level + 0.18 * slack_stock + 0.08 * governance
     function_level = function_level - 0.18 * strain - 0.10 * fragility_gap
     function_level = max(0.0, min(1.0, function_level))

     slack_consumption = 0.09 * disruption_load + 0.08 * fragility_gap + 0.05 * consumption_pressure
     slack_rebuilding = 0.020 * financial + 0.020 * governance + 0.015 * knowledge + 0.010 * network
     slack_stock = max(0.0, min(1.0, slack_stock - slack_consumption + slack_rebuilding))

     ethical_adjusted_function = max(0.0, min(1.0, function_level * (0.72 + 0.28 * ethics) - 0.10 * strain - 0.06 * ethical_burden))

     resilience_score = 0.20 * function_level + 0.18 * slack_stock + 0.16 * adaptive_response
     resilience_score = resilience_score + 0.14 * ethical_adjusted_function + 0.12 * (1.0 - strain)
     resilience_score = resilience_score + 0.10 * governance + 0.10 * ethics
     resilience_score = max(0.0, min(1.0, resilience_score))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", slack_stock, ",", adaptive_response, &
        ",", fragility_gap, ",", strain, ",", resilience_score
  end do
end program strategic_slack_dynamics
