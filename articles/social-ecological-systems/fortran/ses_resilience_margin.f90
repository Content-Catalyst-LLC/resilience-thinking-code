program ses_resilience_margin
  implicit none

  integer, parameter :: steps = 90
  integer :: t
  real :: ecology, social_pressure, extraction, margin
  real :: governance, livelihood_pressure, climate_pressure, market_shock
  real :: r, k, q, ecological_growth, climate_effect, governance_repair, market_pulse

  ecology = 0.75
  social_pressure = 0.55
  governance = 0.60
  livelihood_pressure = 0.55
  climate_pressure = 0.58
  market_shock = 0.38

  r = 0.08
  k = 1.0
  q = 0.10

  print *, "time,ecology,social_pressure,extraction,resilience_margin,threshold_flag"

  do t = 1, steps
     extraction = q * social_pressure * ecology
     ecological_growth = r * ecology * (1.0 - ecology / k)
     climate_effect = 0.022 * climate_pressure
     governance_repair = 0.017 * governance

     ecology = ecology + ecological_growth - extraction - climate_effect + governance_repair
     if (ecology < 0.01) ecology = 0.01
     if (ecology > 1.20) ecology = 1.20

     if (t == 20 .or. t == 42 .or. t == 68) then
        market_pulse = 0.035 * market_shock
     else
        market_pulse = 0.0
     end if

     social_pressure = social_pressure + 0.050 * livelihood_pressure + 0.028 * (1.0 - governance) + market_pulse - 0.043 * ecology
     if (social_pressure < 0.05) social_pressure = 0.05
     if (social_pressure > 1.20) social_pressure = 1.20

     margin = ecology + governance + 0.35 * (1.0 - livelihood_pressure) - social_pressure - 0.35 * climate_pressure

     if (margin < 0.20) then
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", ecology, ",", social_pressure, ",", extraction, ",", margin, ",", "threshold risk"
     else
        print '(I0,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,A)', t, ",", ecology, ",", social_pressure, ",", extraction, ",", margin, ",", "viable margin"
     end if
  end do
end program ses_resilience_margin
