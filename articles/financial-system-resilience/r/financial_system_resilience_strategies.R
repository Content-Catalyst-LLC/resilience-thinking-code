# Financial system resilience strategy scoring workflow.
# Run: Rscript r/financial_system_resilience_strategies.R
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

strategies_path <- file.path(root, "data", "raw", "financial_resilience_strategies.csv")
scenarios_path <- file.path(root, "data", "raw", "financial_resilience_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(strategies_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_strategies <- function(data, scenario_row) {
  data %>%
    mutate(
      financial_resilience_value =
        scenario_row$capital_strength_weight * capital_strength +
        scenario_row$liquidity_resilience_weight * liquidity_resilience +
        scenario_row$infrastructure_robustness_weight * infrastructure_robustness +
        scenario_row$governance_capacity_weight * governance_capacity +
        scenario_row$inclusive_resilience_weight * inclusive_resilience -
        scenario_row$systemic_exposure_weight * systemic_exposure -
        scenario_row$implementation_burden_weight * implementation_burden,
      inclusion_gap = pmax(0, 8.0 - inclusive_resilience),
      infrastructure_gap = pmax(0, 8.0 - infrastructure_robustness),
      adjusted_value = financial_resilience_value - 0.07 * inclusion_gap - 0.06 * infrastructure_gap,
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
    financial_resilience_value =
      0.16 * capital_strength +
      0.16 * liquidity_resilience +
      0.16 * infrastructure_robustness +
      0.16 * governance_capacity +
      0.16 * inclusive_resilience -
      0.12 * systemic_exposure -
      0.08 * implementation_burden,
    inclusion_gap = pmax(0, 8.0 - inclusive_resilience),
    infrastructure_gap = pmax(0, 8.0 - infrastructure_robustness),
    adjusted_value = financial_resilience_value - 0.07 * inclusion_gap - 0.06 * infrastructure_gap
  )

p1 <- ggplot(ranked_results, aes(x = strategy, y = adjusted_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Financial System Resilience Strategy Value Across Priority Scenarios",
    x = "Strategy",
    y = "Adjusted Financial Resilience Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_financial_resilience_strategy_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_financial_resilience_strategy_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_financial_resilience_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_financial_resilience_strategy_profiles.csv"))

print(top_rank_summary)
