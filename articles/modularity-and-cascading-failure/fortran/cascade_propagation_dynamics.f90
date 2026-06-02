program cascade_propagation_dynamics
  implicit none

  integer, parameter :: steps = 60
  integer :: t
  real :: failed_share, disturbance, coupling, redundancy, isolation_capacity, common_mode

  failed_share = 0.08
  coupling = 0.66
  redundancy = 0.56
  isolation_capacity = 0.50
  common_mode = 0.44

  print *, "time,failed_share,disturbance,coupling,redundancy,isolation_capacity,common_mode"

  do t = 1, steps
     if (t == 12 .or. t == 36) then
        disturbance = 0.28
     else
        disturbance = 0.04
     end if

     failed_share = min(1.0, max(0.0, &
        failed_share + &
        0.30 * disturbance + &
        0.18 * coupling + &
        0.12 * common_mode - &
        0.16 * redundancy - &
        0.15 * isolation_capacity))

     print '(I0,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5,A,F8.5)', &
        t, ",", failed_share, ",", disturbance, ",", coupling, ",", redundancy, ",", isolation_capacity, ",", common_mode
  end do
end program cascade_propagation_dynamics
