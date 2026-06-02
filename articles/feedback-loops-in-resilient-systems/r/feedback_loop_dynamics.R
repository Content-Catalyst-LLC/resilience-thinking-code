# Feedback-loop dynamics workflow
#
# Run:
#   Rscript r/feedback_loop_dynamics.R
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

time_steps <- 1:80

alpha <- 0.065
reinforcing <- numeric(length(time_steps))
reinforcing[1] <- 10

for (t in 2:length(time_steps)) {
  reinforcing[t] <- reinforcing[t - 1] + alpha * reinforcing[t - 1]
}

beta <- 0.18
target <- 100
balancing <- numeric(length(time_steps))
balancing[1] <- 10

for (t in 2:length(time_steps)) {
  balancing[t] <- balancing[t - 1] + beta * (target - balancing[t - 1])
}

alpha2 <- 0.035
beta2 <- 0.12
target2 <- 75
combined <- numeric(length(time_steps))
combined[1] <- 20

for (t in 2:length(time_steps)) {
  combined[t] <- combined[t - 1] +
    alpha2 * combined[t - 1] -
    beta2 * (combined[t - 1] - target2)
}

alpha3 <- 0.03
beta3 <- 0.14
target3 <- 75
delay_steps <- 5

delayed_balancing <- numeric(length(time_steps))
delayed_balancing[1:(delay_steps + 1)] <- 20

for (t in (delay_steps + 2):length(time_steps)) {
  delayed_balancing[t] <- delayed_balancing[t - 1] +
    alpha3 * delayed_balancing[t - 1] -
    beta3 * (delayed_balancing[t - delay_steps] - target3)
}

feedback_df <- tibble(
  time = rep(time_steps, 4),
  value = c(reinforcing, balancing, combined, delayed_balancing),
  system_type = rep(
    c("Reinforcing", "Balancing", "Combined Reinforcing and Balancing", "Delayed Balancing"),
    each = length(time_steps)
  )
)

summary_df <- feedback_df %>%
  group_by(system_type) %>%
  summarise(
    initial_value = first(value),
    final_value = last(value),
    max_value = max(value),
    min_value = min(value),
    range_value = max(value) - min(value),
    .groups = "drop"
  )

p1 <- ggplot(feedback_df, aes(x = time, y = value, color = system_type)) +
  geom_line(linewidth = 1.1) +
  labs(
    title = "Feedback Loop Dynamics Over Time",
    x = "Time Step",
    y = "System Value",
    color = "System Type"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_feedback_loop_dynamics.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(feedback_df, file.path(out_tables, "r_feedback_loop_dynamics_over_time.csv"))
write_csv(summary_df, file.path(out_tables, "r_feedback_loop_summary.csv"))

print(summary_df)
