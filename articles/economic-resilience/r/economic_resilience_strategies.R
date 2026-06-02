# Economic resilience strategy scoring workflow.
# Run: Rscript r/economic_resilience_strategies.R
# Requires: install.packages("tidyverse")

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

strategies_path <- file.path(root, "data", "raw", "economic_resilience_strategies.csv")
scenarios_path <- file.path(root, "data", "raw", "economic_resilience_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(strategies_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_strategies <- function(data, scenario_row) {
  data %>%
    mutate(
      economic_resilience_value =
        scenario_row$resistance_weight * resistance +
        scenario_row$recovery_weight * recovery +
        scenario_row$adaptability_weight * adaptability +
        scenario_row$transformability_weight * transformability +
        scenario_row$equity_protection_weight * equity_protection +
        scenario_row$institutional_capacity_weight * institutional_capacity -
        scenario_row$implementation_burden_weight * implementation_burden,
      equity_gap = pmax(0, 8.3 - equity_protection),
      institutional_gap = pmax(0, 8.2 - institutional_capacity),
      adjusted_value = economic_resilience_value - 0.08 * equity_gap - 0.06 * institutional_gap,
      scenario = scenario_row$scenario
    ) %>%
    arrange(desc(adjusted_value)) %>%
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
    economic_resilience_value =
      0.16 * resistance +
      0.16 * recovery +
      0.17 * adaptability +
      0.17 * transformability +
      0.17 * equity_protection +
      0.17 * institutional_capacity -
      0.02 * implementation_burden,
    equity_gap = pmax(0, 8.3 - equity_protection),
    institutional_gap = pmax(0, 8.2 - institutional_capacity),
    adjusted_value = economic_resilience_value - 0.08 * equity_gap - 0.06 * institutional_gap
  )

p1 <- ggplot(ranked_results, aes(x = strategy, y = adjusted_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Economic Resilience Strategy Value Across Priority Scenarios",
    x = "Strategy",
    y = "Adjusted Economic Resilience Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_economic_resilience_strategy_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_economic_resilience_strategy_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_economic_resilience_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_economic_resilience_strategy_profiles.csv"))

print(top_rank_summary)
