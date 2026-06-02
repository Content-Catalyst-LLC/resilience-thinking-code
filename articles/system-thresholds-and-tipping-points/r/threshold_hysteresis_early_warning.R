# Threshold crossing, hysteresis, and early warning workflow
#
# Run:
#   Rscript r/threshold_hysteresis_early_warning.R
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

update_state <- function(x, pressure, r = 1.2, dt = 0.05) {
  x + dt * (r * x - x^3 + pressure)
}

forward_pressure <- seq(-0.8, 0.8, length.out = 160)
x_forward <- numeric(length(forward_pressure))
x_forward[1] <- -0.9

for (t in 2:length(forward_pressure)) {
  x_forward[t] <- update_state(x_forward[t - 1], forward_pressure[t])
}

forward_df <- tibble(
  step = 1:length(forward_pressure),
  pressure = forward_pressure,
  state = x_forward,
  direction = "Increasing Pressure"
)

backward_pressure <- seq(0.8, -0.8, length.out = 160)
x_backward <- numeric(length(backward_pressure))
x_backward[1] <- x_forward[length(x_forward)]

for (t in 2:length(backward_pressure)) {
  x_backward[t] <- update_state(x_backward[t - 1], backward_pressure[t])
}

backward_df <- tibble(
  step = 1:length(backward_pressure),
  pressure = backward_pressure,
  state = x_backward,
  direction = "Decreasing Pressure"
)

threshold_df <- bind_rows(forward_df, backward_df) %>%
  mutate(regime = if_else(state >= 0, "upper regime", "lower regime"))

rolling_window <- 16

early_warning_df <- forward_df %>%
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

p1 <- ggplot(threshold_df, aes(x = pressure, y = state, color = direction)) +
  geom_line(linewidth = 1.1) +
  labs(
    title = "Threshold Crossing and Hysteresis in a Nonlinear System",
    x = "External Pressure",
    y = "System State",
    color = "Path Direction"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_threshold_hysteresis_path.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(early_warning_df, aes(x = step)) +
  geom_line(aes(y = rolling_variance, color = "Rolling variance"), linewidth = 1) +
  geom_line(aes(y = rolling_autocorr, color = "Lag-1 autocorrelation"), linewidth = 1) +
  geom_line(aes(y = threshold_proximity_score, color = "Threshold proximity score"), linewidth = 1) +
  labs(
    title = "Stylized Early Warning Indicators",
    x = "Step",
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

write_csv(threshold_df, file.path(out_tables, "r_threshold_hysteresis_simulation.csv"))
write_csv(early_warning_df, file.path(out_tables, "r_threshold_early_warning_signals.csv"))

print(threshold_df)
print(early_warning_df)
