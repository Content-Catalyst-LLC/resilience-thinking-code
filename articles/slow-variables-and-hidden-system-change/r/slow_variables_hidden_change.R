# Slow-variable hidden change workflow
#
# Run:
#   Rscript r/slow_variables_hidden_change.R
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

time_steps <- 1:120

slow_df <- tibble(
  time = time_steps,
  maintenance_backlog = numeric(length(time_steps)),
  public_trust = numeric(length(time_steps)),
  ecological_memory = numeric(length(time_steps)),
  climate_pressure = numeric(length(time_steps)),
  adaptive_capacity = numeric(length(time_steps)),
  threshold_distance = numeric(length(time_steps)),
  hidden_risk = numeric(length(time_steps)),
  fast_shock = numeric(length(time_steps)),
  system_function = numeric(length(time_steps))
)

slow_df$maintenance_backlog[1] <- 0.25
slow_df$public_trust[1] <- 0.72
slow_df$ecological_memory[1] <- 0.68
slow_df$climate_pressure[1] <- 0.22
slow_df$adaptive_capacity[1] <- 0.62
slow_df$threshold_distance[1] <- 0.74
slow_df$hidden_risk[1] <- 0.30
slow_df$system_function[1] <- 0.86

for (t in 2:length(time_steps)) {
  slow_df$maintenance_backlog[t] <-
    min(1, slow_df$maintenance_backlog[t - 1] + 0.006)

  slow_df$public_trust[t] <-
    max(0, slow_df$public_trust[t - 1] - 0.0035)

  slow_df$ecological_memory[t] <-
    max(0, slow_df$ecological_memory[t - 1] - 0.0025)

  slow_df$climate_pressure[t] <-
    min(1, slow_df$climate_pressure[t - 1] + 0.0045)

  slow_df$adaptive_capacity[t] <-
    max(
      0,
      min(
        1,
        0.35 * slow_df$public_trust[t] +
          0.30 * slow_df$ecological_memory[t] +
          0.20 * (1 - slow_df$maintenance_backlog[t]) +
          0.15 * (1 - slow_df$climate_pressure[t])
      )
    )

  slow_df$threshold_distance[t] <-
    max(
      0,
      1 -
        0.30 * slow_df$maintenance_backlog[t] -
        0.28 * slow_df$climate_pressure[t] -
        0.22 * (1 - slow_df$public_trust[t]) -
        0.20 * (1 - slow_df$ecological_memory[t])
    )

  slow_df$hidden_risk[t] <-
    min(
      1,
      0.32 * slow_df$maintenance_backlog[t] +
        0.30 * slow_df$climate_pressure[t] +
        0.22 * (1 - slow_df$public_trust[t]) +
        0.16 * (1 - slow_df$ecological_memory[t])
    )

  slow_df$fast_shock[t] <-
    if_else(t %in% c(72, 96), 0.32, 0)

  slow_df$system_function[t] <-
    max(
      0,
      min(
        1,
        slow_df$system_function[t - 1] -
          0.22 * slow_df$hidden_risk[t] -
          0.46 * slow_df$fast_shock[t] +
          0.18 * slow_df$adaptive_capacity[t]
      )
    )
}

slow_long <- slow_df %>%
  pivot_longer(
    cols = c(
      maintenance_backlog,
      public_trust,
      ecological_memory,
      climate_pressure,
      adaptive_capacity,
      threshold_distance,
      hidden_risk,
      system_function
    ),
    names_to = "variable",
    values_to = "value"
  )

summary_df <- slow_df %>%
  summarise(
    final_system_function = last(system_function),
    minimum_threshold_distance = min(threshold_distance),
    maximum_hidden_risk = max(hidden_risk),
    final_adaptive_capacity = last(adaptive_capacity)
  )

p1 <- ggplot(slow_long, aes(x = time, y = value, color = variable)) +
  geom_line(linewidth = 1) +
  labs(
    title = "Slow Variables and Hidden System Change",
    x = "Time Step",
    y = "Value",
    color = "Variable"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_slow_variables_hidden_change.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(slow_df, aes(x = time)) +
  geom_line(aes(y = threshold_distance, color = "Threshold Distance"), linewidth = 1.1) +
  geom_line(aes(y = hidden_risk, color = "Hidden Risk"), linewidth = 1.1) +
  geom_line(aes(y = system_function, color = "System Function"), linewidth = 1.1) +
  labs(
    title = "Threshold Distance, Hidden Risk, and System Function",
    x = "Time Step",
    y = "Value",
    color = "Metric"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_threshold_distance_hidden_risk.png"),
  plot = p2,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(slow_df, file.path(out_tables, "r_slow_variables_hidden_change_simulation.csv"))
write_csv(slow_long, file.path(out_tables, "r_slow_variables_hidden_change_long.csv"))
write_csv(summary_df, file.path(out_tables, "r_slow_variables_hidden_change_summary.csv"))

print(summary_df)
