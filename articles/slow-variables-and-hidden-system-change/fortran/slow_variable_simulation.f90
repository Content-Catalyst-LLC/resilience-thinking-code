program slow_variable_simulation
  implicit none

  integer, parameter :: steps = 120
  integer :: t
  real :: maintenance_backlog, public_trust, ecological_memory
  real :: climate_pressure, adaptive_capacity, threshold_distance
  real :: hidden_risk, fast_shock, system_function

  maintenance_backlog = 0.25
  public_trust = 0.72
  ecological_memory = 0.68
  climate_pressure = 0.22
  system_function = 0.86

  print *, "time,maintenance_backlog,public_trust,ecological_memory,climate_pressure,adaptive_capacity,threshold_distance,hidden_risk,fast_shock,system_function"

  do t = 1, steps
     maintenance_backlog = min(1.0, max(0.0, maintenance_backlog + 0.006))
     public_trust = min(1.0, max(0.0, public_trust - 0.0035))
     ecological_memory = min(1.0, max(0.0, ecological_memory - 0.0025))
     climate_pressure = min(1.0, max(0.0, climate_pressure + 0.0045))

     adaptive_capacity = min(1.0, max(0.0, &
        0.35 * public_trust + &
        0.30 * ecological_memory + &
        0.20 * (1.0 - maintenance_backlog) + &
        0.15 * (1.0 - climate_pressure)))

     threshold_distance = min(1.0, max(0.0, &
        1.0 - &
        0.30 * maintenance_backlog - &
        0.28 * climate_pressure - &
        0.22 * (1.0 - public_trust) - &
        0.20 * (1.0 - ecological_memory)))

     hidden_risk = min(1.0, max(0.0, &
        0.32 * maintenance_backlog + &
        0.30 * climate_pressure + &
        0.22 * (1.0 - public_trust) + &
        0.16 * (1.0 - ecological_memory)))

     if (t == 72 .or. t == 96) then
        fast_shock = 0.32
     else
        fast_shock = 0.0
     end if

     system_function = min(1.0, max(0.0, &
        system_function - &
        0.22 * hidden_risk - &
        0.46 * fast_shock + &
        0.18 * adaptive_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", maintenance_backlog, ",", public_trust, ",", ecological_memory, ",", &
        climate_pressure, ",", adaptive_capacity, ",", threshold_distance, ",", &
        hidden_risk, ",", fast_shock, ",", system_function
  end do
end program slow_variable_simulation
