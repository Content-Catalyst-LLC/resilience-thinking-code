# Adaptive-cycle phase simulation workflow
#
# Run:
#   Rscript r/adaptive_cycle_phase_simulation.R
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

time_steps <- 1:120

adaptive_cycle_df <- tibble(
  time = time_steps,
  potential = numeric(length(time_steps)),
  connectedness = numeric(length(time_steps)),
  resilience = numeric(length(time_steps)),
  rigidity = numeric(length(time_steps)),
  memory = numeric(length(time_steps)),
  novelty = numeric(length(time_steps)),
  phase = character(length(time_steps))
)

adaptive_cycle_df$potential[1] <- 0.20
adaptive_cycle_df$connectedness[1] <- 0.15
adaptive_cycle_df$resilience[1] <- 0.82
adaptive_cycle_df$rigidity[1] <- 0.10
adaptive_cycle_df$memory[1] <- 0.55
adaptive_cycle_df$novelty[1] <- 0.15
adaptive_cycle_df$phase[1] <- "r"

growth_rate <- 0.11
connect_rate <- 0.08
rigidity_threshold <- 0.72
resilience_threshold <- 0.34
memory_strength <- 0.48

for (t in 2:length(time_steps)) {
  previous_phase <- adaptive_cycle_df$phase[t - 1]

  previous_potential <- adaptive_cycle_df$potential[t - 1]
  previous_connectedness <- adaptive_cycle_df$connectedness[t - 1]
  previous_resilience <- adaptive_cycle_df$resilience[t - 1]
  previous_rigidity <- adaptive_cycle_df$rigidity[t - 1]
  previous_memory <- adaptive_cycle_df$memory[t - 1]

  if (previous_phase %in% c("r", "K")) {
    adaptive_cycle_df$potential[t] <-
      previous_potential +
      growth_rate * previous_potential * (1 - previous_potential)

    adaptive_cycle_df$connectedness[t] <-
      min(1, previous_connectedness + connect_rate * (1 - previous_connectedness))

    adaptive_cycle_df$rigidity[t] <-
      min(1, previous_rigidity + 0.055 * adaptive_cycle_df$connectedness[t])

    adaptive_cycle_df$resilience[t] <-
      max(0, 1 - 0.62 * adaptive_cycle_df$connectedness[t] - 0.35 * adaptive_cycle_df$rigidity[t])

    adaptive_cycle_df$memory[t] <-
      min(1, previous_memory + 0.015 * adaptive_cycle_df$potential[t])

    adaptive_cycle_df$novelty[t] <-
      max(0.02, 0.25 * (1 - adaptive_cycle_df$connectedness[t]))

    adaptive_cycle_df$phase[t] <-
      if_else(adaptive_cycle_df$connectedness[t] > 0.55, "K", "r")

    if (
      adaptive_cycle_df$rigidity[t] > rigidity_threshold &&
      adaptive_cycle_df$resilience[t] < resilience_threshold
    ) {
      adaptive_cycle_df$phase[t] <- "Omega"
    }

  } else if (previous_phase == "Omega") {
    adaptive_cycle_df$potential[t] <- max(0.05, previous_potential * 0.42)
    adaptive_cycle_df$connectedness[t] <- max(0.08, previous_connectedness * 0.32)
    adaptive_cycle_df$rigidity[t] <- max(0.05, previous_rigidity * 0.38)
    adaptive_cycle_df$resilience[t] <- min(1, previous_resilience + 0.30)
    adaptive_cycle_df$memory[t] <- max(0.25, previous_memory * 0.86)
    adaptive_cycle_df$novelty[t] <- runif(1, 0.25, 0.45)
    adaptive_cycle_df$phase[t] <- "alpha"

  } else if (previous_phase == "alpha") {
    adaptive_cycle_df$potential[t] <-
      min(1, memory_strength * previous_memory + runif(1, 0.06, 0.18))

    adaptive_cycle_df$connectedness[t] <-
      min(1, previous_connectedness + runif(1, 0.015, 0.045))

    adaptive_cycle_df$rigidity[t] <-
      max(0.03, previous_rigidity + runif(1, -0.02, 0.015))

    adaptive_cycle_df$resilience[t] <-
      min(1, previous_resilience + runif(1, 0.025, 0.075))

    adaptive_cycle_df$memory[t] <-
      min(1, previous_memory + runif(1, -0.015, 0.025))

    adaptive_cycle_df$novelty[t] <-
      runif(1, 0.18, 0.38)

    adaptive_cycle_df$phase[t] <-
      if_else(
        adaptive_cycle_df$potential[t] > 0.32 &&
          adaptive_cycle_df$connectedness[t] < 0.50,
        "r",
        "alpha"
      )
  }
}

adaptive_long <- adaptive_cycle_df %>%
  pivot_longer(
    cols = c(potential, connectedness, resilience, rigidity, memory, novelty),
    names_to = "state_variable",
    values_to = "value"
  )

phase_summary <- adaptive_cycle_df %>%
  count(phase, name = "time_steps_in_phase")

p1 <- ggplot(adaptive_long, aes(x = time, y = value, color = state_variable)) +
  geom_line(linewidth = 1.05) +
  labs(
    title = "Stylized Adaptive Cycle State Variables",
    x = "Time Step",
    y = "Value",
    color = "State Variable"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_adaptive_cycle_state_variables.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(adaptive_cycle_df, aes(x = time, y = phase, color = phase)) +
  geom_point(size = 2.4) +
  labs(
    title = "Adaptive Cycle Phase Assignment",
    x = "Time Step",
    y = "Phase"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_adaptive_cycle_phase_assignment.png"),
  plot = p2,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(adaptive_cycle_df, file.path(out_tables, "r_adaptive_cycle_phase_simulation.csv"))
write_csv(adaptive_long, file.path(out_tables, "r_adaptive_cycle_phase_simulation_long.csv"))
write_csv(phase_summary, file.path(out_tables, "r_adaptive_cycle_phase_summary.csv"))

print(phase_summary)
