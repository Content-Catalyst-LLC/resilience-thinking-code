# Learning, memory, and adaptive management strategy scoring workflow
#
# Run:
#   Rscript r/adaptive_management_strategies.R
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

strategies_path <- file.path(root, "data", "raw", "adaptive_management_strategies.csv")
scenarios_path <- file.path(root, "data", "raw", "adaptive_management_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(strategies_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_strategies <- function(data, scenario_row) {
  data %>%
    mutate(
      adaptive_learning_value =
        scenario_row$monitoring_quality_weight * monitoring_quality +
        scenario_row$memory_retention_weight * memory_retention +
        scenario_row$feedback_use_weight * feedback_use +
        scenario_row$governance_flexibility_weight * governance_flexibility +
        scenario_row$community_knowledge_weight * community_knowledge +
        scenario_row$justice_protection_weight * justice_protection +
        scenario_row$implementation_reliability_weight * implementation_reliability -
        scenario_row$forgetting_pressure_weight * forgetting_pressure,
      scenario = scenario_row$scenario
    ) %>%
    arrange(desc(adaptive_learning_value)) %>%
    mutate(rank = row_number())
}

ranked_results <- scenarios %>%
  group_split(scenario) %>%
  map_dfr(~ score_strategies(strategies, .x[1, ]))

top_rank_summary <- ranked_results %>%
  filter(rank == 1) %>%
  count(strategy, name = "times_ranked_first") %>%
  arrange(desc(times_ranked_first))

profiles <- strategies %>%
  mutate(
    base_adaptive_learning_value =
      0.15 * monitoring_quality +
      0.15 * memory_retention +
      0.17 * feedback_use +
      0.14 * governance_flexibility +
      0.12 * community_knowledge +
      0.11 * justice_protection +
      0.09 * implementation_reliability -
      0.07 * forgetting_pressure
  )

p1 <- ggplot(ranked_results, aes(x = strategy, y = adaptive_learning_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Adaptive Management Strategy Value Across Learning Priorities",
    x = "Strategy",
    y = "Weighted Adaptive Learning Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_adaptive_management_strategy_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(profiles, aes(x = reorder(strategy, base_adaptive_learning_value), y = base_adaptive_learning_value)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Base Adaptive Learning Value by Strategy",
    x = "Strategy",
    y = "Base Adaptive Learning Value"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_base_adaptive_learning_value.png"),
  plot = p2,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_adaptive_management_strategy_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_adaptive_management_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_adaptive_management_strategy_profiles.csv"))

print(top_rank_summary)
