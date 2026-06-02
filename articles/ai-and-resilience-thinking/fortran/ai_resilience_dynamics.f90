program ai_resilience_dynamics
  implicit none

  integer, parameter :: steps = 96
  integer :: t
  real :: function_level, ai_risk, drift, human_strain
  real :: baseline, monitoring, forecasting, scenario_capacity, decision_support
  real :: governance, equity, human, local_knowledge, security
  real :: shock, climate_infra, data_shift, public_trust, cyber, resource
  real :: institutional, equity_pressure, drift_pressure
  real :: disturbance, ai_support, governance_buffer, drift_growth, drift_control
  real :: ai_risk_growth, ai_risk_control, fragility_gap
  real :: strain_increase, strain_recovery, equity_performance
  real :: ethical_adjusted_function, resilience_score

  function_level = 0.86
  baseline = 0.82
  monitoring = 0.84
  forecasting = 0.82
  scenario_capacity = 0.86
  decision_support = 0.84
  governance = 0.84
  equity = 0.84
  human = 0.86
  local_knowledge = 0.82
  security = 0.84
  ai_risk = 0.30
  drift = 0.20
  human_strain = 0.34

  print *, "time,function,ai_support,governance_buffer,model_drift,ai_risk,fragility_gap,human_strain,equity_performance,resilience_score"

  do t = 1, steps
     if (t == 10) then
        shock = 0.68
        climate_infra = 0.92
        data_shift = 0.54
        public_trust = 0.50
        cyber = 0.42
        resource = 0.66
        institutional = 0.58
        equity_pressure = 0.76
        drift_pressure = 0.58
     else
        shock = 0.06
        climate_infra = 0.09
        data_shift = 0.08 + 0.001 * real(t)
        public_trust = 0.08
        cyber = 0.08
        resource = 0.10
        institutional = 0.08
        equity_pressure = 0.10
        drift_pressure = 0.08 + 0.0015 * real(t)
     end if

     disturbance = 0.12 * shock + 0.13 * climate_infra + 0.13 * data_shift
     disturbance = disturbance + 0.12 * public_trust + 0.13 * cyber + 0.13 * resource
     disturbance = disturbance + 0.11 * institutional + 0.12 * equity_pressure + 0.11 * drift_pressure

     ai_support = 0.17 * monitoring + 0.15 * forecasting + 0.15 * scenario_capacity
     ai_support = ai_support + 0.15 * decision_support + 0.11 * governance + 0.09 * human
     ai_support = ai_support + 0.08 * equity + 0.05 * local_knowledge + 0.05 * security
     ai_support = max(0.0, min(1.0, ai_support))

     governance_buffer = 0.25 * governance + 0.21 * human + 0.20 * equity
     governance_buffer = governance_buffer + 0.16 * security + 0.12 * local_knowledge + 0.06 * scenario_capacity
     governance_buffer = max(0.0, min(1.0, governance_buffer))

     drift_growth = 0.020 * disturbance + 0.022 * drift_pressure + 0.016 * (1.0 - local_knowledge) + 0.012 * (1.0 - monitoring)
     drift_control = 0.035 * governance + 0.025 * human + 0.020 * scenario_capacity + 0.016 * local_knowledge
     drift = max(0.0, min(1.0, drift + drift_growth - drift_control))

     ai_risk_growth = 0.025 * disturbance + 0.035 * drift + 0.025 * (1.0 - governance)
     ai_risk_growth = ai_risk_growth + 0.024 * (1.0 - equity) + 0.018 * cyber
     ai_risk_control = 0.035 * governance + 0.025 * security + 0.025 * human + 0.014 * local_knowledge
     ai_risk = max(0.0, min(1.0, ai_risk + ai_risk_growth - ai_risk_control))

     fragility_gap = max(0.0, disturbance + 0.34 * ai_risk + 0.25 * drift - governance_buffer)

     strain_increase = 0.17 * disturbance + 0.15 * fragility_gap + 0.09 * ai_risk + 0.05 * resource
     strain_recovery = 0.08 * human + 0.06 * local_knowledge + 0.05 * governance
     human_strain = max(0.0, min(1.0, human_strain + strain_increase - strain_recovery))

     equity_performance = 0.36 * equity + 0.20 * local_knowledge + 0.17 * governance
     equity_performance = equity_performance + 0.11 * human + 0.08 * security - 0.12 * ai_risk
     equity_performance = equity_performance - 0.10 * drift - 0.08 * equity_pressure
     equity_performance = max(0.0, min(1.0, equity_performance))

     function_level = function_level - 0.28 * disturbance - 0.15 * fragility_gap
     function_level = function_level + 0.16 * baseline + 0.18 * ai_support + 0.12 * governance_buffer
     function_level = function_level + 0.10 * equity_performance - 0.11 * human_strain
     function_level = max(0.0, min(1.0, function_level))

     ethical_adjusted_function = max(0.0, min(1.0, function_level * (0.70 + 0.30 * equity_performance) - 0.08 * human_strain - 0.08 * ai_risk))

     resilience_score = 0.17 * function_level + 0.15 * baseline + 0.15 * ai_support
     resilience_score = resilience_score + 0.13 * governance_buffer + 0.12 * equity_performance
     resilience_score = resilience_score + 0.10 * (1.0 - ai_risk) + 0.08 * (1.0 - drift)
     resilience_score = resilience_score + 0.06 * (1.0 - human_strain) + 0.04 * local_knowledge
     resilience_score = max(0.0, min(1.0, resilience_score))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", function_level, ",", ai_support, ",", governance_buffer, ",", drift, ",", ai_risk, &
        ",", fragility_gap, ",", human_strain, ",", equity_performance, ",", resilience_score
  end do
end program ai_resilience_dynamics
