program adaptive_cycle_transition
  implicit none

  integer, parameter :: steps = 120
  integer :: t, release_flag
  real :: potential, connectedness, resilience, rigidity, memory, novelty
  character(len=8) :: phase

  potential = 0.20
  connectedness = 0.15
  resilience = 0.82
  rigidity = 0.10
  memory = 0.55
  novelty = 0.15
  phase = "r"

  print *, "time,phase,potential,connectedness,resilience,rigidity,memory,novelty,release_flag"

  do t = 1, steps
     if (trim(phase) == "r" .or. trim(phase) == "K") then
        potential = min(1.0, potential + 0.11 * potential * (1.0 - potential))
        connectedness = min(1.0, connectedness + 0.08 * (1.0 - connectedness))
        rigidity = min(1.0, rigidity + 0.055 * connectedness)
        resilience = max(0.0, 1.0 - 0.62 * connectedness - 0.35 * rigidity)
        memory = min(1.0, memory + 0.015 * potential)
        novelty = max(0.02, 0.25 * (1.0 - connectedness))

        if (connectedness > 0.55) then
           phase = "K"
        else
           phase = "r"
        end if

        if (rigidity > 0.72 .and. resilience < 0.34) then
           phase = "Omega"
        end if

     else if (trim(phase) == "Omega") then
        potential = max(0.05, potential * 0.42)
        connectedness = max(0.08, connectedness * 0.32)
        rigidity = max(0.05, rigidity * 0.38)
        resilience = min(1.0, resilience + 0.30)
        memory = max(0.25, memory * 0.86)
        novelty = 0.32
        phase = "alpha"

     else if (trim(phase) == "alpha") then
        novelty = 0.24
        potential = min(1.0, 0.48 * memory + 0.12)
        connectedness = min(1.0, connectedness + 0.03)
        rigidity = max(0.03, rigidity - 0.004)
        resilience = min(1.0, resilience + 0.05)
        memory = min(1.0, memory + 0.005)

        if (potential > 0.32 .and. connectedness < 0.50) then
           phase = "r"
        else
           phase = "alpha"
        end if
     end if

     if (trim(phase) == "Omega") then
        release_flag = 1
     else
        release_flag = 0
     end if

     print '(I0,A,A,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,F7.4,A,I0)', &
        t, ",", trim(phase), ",", potential, ",", connectedness, ",", resilience, ",", rigidity, ",", memory, ",", novelty, ",", release_flag
  end do
end program adaptive_cycle_transition
