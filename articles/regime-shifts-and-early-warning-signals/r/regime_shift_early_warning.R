# Regime shifts and early warning workflow
#
# Run:
#   Rscript r/regime_shift_early_warning.R
#
# Requires:
#   install.packages("tidyverse")

suppressPackageStartupMessages({
  library(tidyverse)
})

script_args <- commandArgs(trailingOnly = FALSE)
file_arg <- script_args[grepl("^--file=", script_args)]
if (length(file_arg) > 0) {
  root <- normalizePath(file.path(dirname(sub("^--file=", "", file_arg[1])), ".."))
} else {
  root <- getwd()
}

out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

set.seed(42)

update_state <- function(x, pressure, r = 1.2, dt = 0.05) {
  x + dt * (r * x - x^3 + pressure)
}

steps <- 180
pressure <- seq(-0.75, 0.85, length.out = steps)
state <- numeric(steps)
state[1] <- -0.90
noise_sd <- 0.018

for (t in 2:steps) {
  state[t] <- update_state(state[t - 1], pressure[t]) +
    rnorm(1, mean = 0, sd = noise_sd)
}

regime_df <- tibble(
  time = 1:steps,
  pressure = pressure,
  state = state,
  regime = if_else(state >= 0, "upper regime", "lower regime")
)

rolling_window <- 18

early_warning_df <- regime_df %>%
  mutate(
    rolling_variance = sapply(seq_along(state), function(i) {
      if (i < rolling_window) return(NA_real_)
      var(state[(i - rolling_window + 1):i])
    }),
    rolling_autocorr = sapply(seq_along(state), function(i) {
      if (i < rolling_window) return(NA_real_)
      segment <- state[(i - rolling_window + 1):i]
      cor(segment[-length(segment)], segment[-1])
    }),
    recovery_speed_proxy = 1 - rolling_autocorr,
    threshold_proximity_score =
      (percent_rank(rolling_variance) + percent_rank(rolling_autocorr)) / 2
  )

transition_time <- early_warning_df %>%
  filter(regime == "upper regime") %>%
  slice(1) %>%
  pull(time)

if (length(transition_time) == 0) {
  transition_time <- NA_integer_
}

summary_df <- early_warning_df %>%
  summarise(
    transition_time = transition_time,
    max_rolling_variance = max(rolling_variance, na.rm = TRUE),
    max_rolling_autocorr = max(rolling_autocorr, na.rm = TRUE),
    min_recovery_speed_proxy = min(recovery_speed_proxy, na.rm = TRUE),
    max_threshold_proximity_score = max(threshold_proximity_score, na.rm = TRUE)
  )

p1 <- ggplot(regime_df, aes(x = pressure, y = state, color = regime)) +
  geom_line(linewidth = 1.1) +
  labs(
    title = "Nonlinear Regime Shift Under Rising Pressure",
    x = "External Pressure",
    y = "System State",
    color = "Regime"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_regime_shift_path.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(early_warning_df, aes(x = time)) +
  geom_line(aes(y = rolling_variance, color = "Rolling Variance"), linewidth = 1) +
  geom_line(aes(y = rolling_autocorr, color = "Lag-1 Autocorrelation"), linewidth = 1) +
  geom_line(aes(y = threshold_proximity_score, color = "Threshold Proximity Score"), linewidth = 1) +
  labs(
    title = "Early Warning Indicators Before Regime Shift",
    x = "Time Step",
    y = "Value",
    color = "Indicator"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_early_warning_indicators.png"),
  plot = p2,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(regime_df, file.path(out_tables, "r_regime_shift_simulation.csv"))
write_csv(early_warning_df, file.path(out_tables, "r_early_warning_indicators.csv"))
write_csv(summary_df, file.path(out_tables, "r_regime_shift_summary.csv"))

print(summary_df)
