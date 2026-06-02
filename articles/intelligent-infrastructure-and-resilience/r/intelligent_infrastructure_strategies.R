# Intelligent infrastructure resilience strategy scoring workflow.
# Run: Rscript r/intelligent_infrastructure_strategies.R
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

strategies_path <- file.path(root, "data", "raw", "intelligent_infrastructure_strategies.csv")
scenarios_path <- file.path(root, "data", "raw", "intelligent_infrastructure_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(strategies_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_strategies <- function(data, scenario_row) {
  data %>%
    mutate(
      infrastructure_resilience_value =
        scenario_row$monitoring_value_weight * monitoring_value +
        scenario_row$predictive_maintenance_weight * predictive_maintenance +
        scenario_row$cyber_physical_security_weight * cyber_physical_security +
        scenario_row$digital_twin_capacity_weight * digital_twin_capacity +
        scenario_row$redundancy_and_fallback_weight * redundancy_and_fallback +
        scenario_row$climate_adaptation_weight * climate_adaptation +
        scenario_row$governance_quality_weight * governance_quality +
        scenario_row$equity_performance_weight * equity_performance +
        scenario_row$ecological_integration_weight * ecological_integration -
        scenario_row$fragility_risk_weight * fragility_risk -
        scenario_row$implementation_burden_weight * implementation_burden,
      governance_gap = pmax(0, 8.5 - governance_quality),
      equity_gap = pmax(0, 8.5 - equity_performance),
      redundancy_gap = pmax(0, 8.5 - redundancy_and_fallback),
      adjusted_value =
        infrastructure_resilience_value -
        0.07 * governance_gap -
        0.08 * equity_gap -
        0.07 * redundancy_gap,
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
    infrastructure_resilience_value =
      0.10 * monitoring_value +
      0.11 * predictive_maintenance +
      0.11 * cyber_physical_security +
      0.10 * digital_twin_capacity +
      0.11 * redundancy_and_fallback +
      0.11 * climate_adaptation +
      0.12 * governance_quality +
      0.12 * equity_performance +
      0.10 * ecological_integration -
      0.04 * fragility_risk -
      0.04 * implementation_burden
  )

p1 <- ggplot(ranked_results, aes(x = strategy, y = adjusted_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Intelligent Infrastructure Resilience Strategy Value Across Priority Scenarios",
    x = "Strategy",
    y = "Adjusted Infrastructure Resilience Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_intelligent_infrastructure_strategy_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_intelligent_infrastructure_strategy_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_intelligent_infrastructure_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_intelligent_infrastructure_strategy_profiles.csv"))

print(top_rank_summary)
