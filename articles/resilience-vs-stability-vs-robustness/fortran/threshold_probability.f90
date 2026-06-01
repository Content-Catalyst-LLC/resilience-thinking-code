program threshold_probability
  implicit none

  real :: adaptive, threshold, learning, redundancy, modularity
  real :: exposure, sensitivity, shock, protective, pressure, z, probability

  adaptive = 0.38
  threshold = 0.46
  learning = 0.33
  redundancy = 0.60
  modularity = 0.43
  exposure = 0.70
  sensitivity = 0.58
  shock = 0.52

  protective = 0.24*adaptive + 0.22*threshold + 0.18*learning + 0.18*redundancy + 0.18*modularity
  pressure = 0.32*exposure + 0.28*sensitivity + 0.40*shock
  z = -2.0 + 4.2*pressure - 3.8*protective
  probability = 1.0 / (1.0 + exp(-z))

  print *, "predicted_failure_probability"
  print '(F6.4)', probability
end program threshold_probability
