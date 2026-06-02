program knowledge_function_dynamics
  implicit none

  integer, parameter :: steps = 80
  integer :: t
  real :: knowledge_function, institutional_trust, participation_capacity
  real :: knowledge_diversity, decision_access, privacy_risk, community_control
  real :: followthrough, equity_sensitivity, extraction_risk
  real :: shock, participation_burden, trust_pressure, information_stress
  real :: privacy_exposure, decision_delay, reciprocity_gap, accountability_gap
  real :: extraction_pressure, knowledge_stress, protective_capacity
  real :: protection_penalty, extraction_penalty, participation_penalty
  real :: equity_adjusted_function

  knowledge_function = 0.72
  institutional_trust = 0.66
  participation_capacity = 0.78
  knowledge_diversity = 0.80
  decision_access = 0.68
  privacy_risk = 0.72
  community_control = 0.70
  followthrough = 0.64
  equity_sensitivity = 0.88
  extraction_risk = 0.76

  print *, "time,knowledge_function,knowledge_stress,protective_capacity,institutional_trust,extraction_risk,equity_adjusted_function"

  do t = 1, steps
     if (t == 12) then
        shock = 0.80
        participation_burden = 0.90
        trust_pressure = 0.72
        information_stress = 0.76
        privacy_exposure = 0.66
        decision_delay = 0.78
        reciprocity_gap = 0.72
        accountability_gap = 0.74
        extraction_pressure = 0.70
     else
        shock = 0.06
        participation_burden = 0.12
        trust_pressure = 0.10
        information_stress = 0.10
        privacy_exposure = 0.10
        decision_delay = 0.11 + 0.001 * real(t)
        reciprocity_gap = 0.10
        accountability_gap = 0.11
        extraction_pressure = 0.12
     end if

     knowledge_stress = 0.13 * shock + 0.14 * participation_burden + 0.14 * trust_pressure
     knowledge_stress = knowledge_stress + 0.12 * information_stress + 0.15 * privacy_exposure
     knowledge_stress = knowledge_stress + 0.12 * decision_delay + 0.10 * reciprocity_gap
     knowledge_stress = knowledge_stress + 0.12 * accountability_gap + 0.13 * extraction_pressure
     knowledge_stress = knowledge_stress + 0.08 * extraction_risk

     protective_capacity = 0.15 * institutional_trust + 0.15 * participation_capacity
     protective_capacity = protective_capacity + 0.14 * knowledge_diversity + 0.14 * decision_access
     protective_capacity = protective_capacity + 0.15 * (1.0 - privacy_risk) + 0.14 * community_control
     protective_capacity = protective_capacity + 0.15 * followthrough + 0.08 * equity_sensitivity
     protective_capacity = max(0.0, min(1.0, protective_capacity))

     protection_penalty = max(0.0, privacy_risk + privacy_exposure - 1.35) * 0.10
     extraction_penalty = max(0.0, extraction_risk + extraction_pressure - 1.35) * 0.10
     participation_penalty = max(0.0, participation_burden - participation_capacity) * 0.08

     knowledge_function = knowledge_function - 0.30 * knowledge_stress + 0.20 * protective_capacity
     knowledge_function = knowledge_function + 0.08 * institutional_trust + 0.08 * participation_capacity
     knowledge_function = knowledge_function + 0.08 * knowledge_diversity + 0.08 * decision_access
     knowledge_function = knowledge_function + 0.08 * community_control + 0.08 * followthrough
     knowledge_function = knowledge_function - protection_penalty - extraction_penalty - participation_penalty
     knowledge_function = max(0.0, min(1.0, knowledge_function))

     institutional_trust = max(0.0, min(1.0, institutional_trust + 0.010 * followthrough - 0.012 * trust_pressure - 0.010 * extraction_pressure))
     extraction_risk = max(0.0, min(1.0, extraction_risk + 0.014 * extraction_pressure + 0.010 * privacy_exposure - 0.010 * community_control))
     equity_adjusted_function = max(0.0, min(1.0, knowledge_function * (0.72 + 0.28 * equity_sensitivity)))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", knowledge_function, ",", knowledge_stress, ",", protective_capacity, &
        ",", institutional_trust, ",", extraction_risk, ",", equity_adjusted_function
  end do
end program knowledge_function_dynamics
