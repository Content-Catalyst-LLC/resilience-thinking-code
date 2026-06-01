# Validation Plan

A professional resilience-prediction workflow should include:

1. **Data provenance review**  
   Confirm what each variable measures, who collected it, and whose experience is missing.

2. **Train/test split by scenario and system type**  
   Avoid random splits that leak similar disturbance trajectories across training and test sets.

3. **Temporal validation**  
   When time-indexed observations exist, validate on future periods rather than only random holdouts.

4. **Stress testing**  
   Evaluate predictions under compound shocks, tail events, and low-frequency/high-impact disturbances.

5. **Calibration assessment**  
   Probabilities should be assessed for calibration, not only accuracy.

6. **Feature sensitivity**  
   Examine whether predictions rely too heavily on proxy variables for deprivation, disinvestment, or institutional neglect.

7. **Decision review**  
   Define what action a prediction triggers. A model that identifies risk but does not support repair, investment, or adaptation can become ethically dangerous.
