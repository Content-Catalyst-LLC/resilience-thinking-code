# Local economic resilience strategy scoring workflow.
# Run: Rscript r/local_economic_resilience_strategies.R
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

strategies_path <- file.path(root, "data", "raw", "local_economic_resilience_strategies.csv")
scenarios_path <- file.path(root, "data", "raw", "local_resilience_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(strategies_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_strategies <- function(data, scenario_row) {
  data %>%
    mutate(
      local_resilience_value =
        scenario_row$liquidity_support_weight * liquidity_support +
        scenario_row$workforce_capacity_weight * workforce_capacity +
        scenario_row$supply_resilience_weight * supply_resilience +
        scenario_row$digital_readiness_weight * digital_readiness +
        scenario_row$public_capacity_weight * public_capacity +
        scenario_row$community_wealth_weight * community_wealth +
        scenario_row$equity_access_weight * equity_access -
        scenario_row$inequality_risk_weight * inequality_risk -
        scenario_row$implementation_burden_weight * implementation_burden,
      equity_gap = pmax(0, 8.5 - equity_access),
      liquidity_gap = pmax(0, 8.0 - liquidity_support),
      workforce_gap = pmax(0, 8.0 - workforce_capacity),
      adjusted_value =
        local_resilience_value -
        0.08 * equity_gap -
        0.06 * liquidity_gap -
        0.06 * workforce_gap,
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
    local_resilience_value =
      0.14 * liquidity_support +
      0.14 * workforce_capacity +
      0.12 * supply_resilience +
      0.12 * digital_readiness +
      0.14 * public_capacity +
      0.15 * community_wealth +
      0.16 * equity_access -
      0.07 * inequality_risk -
      0.06 * implementation_burden,
    equity_gap = pmax(0, 8.5 - equity_access),
    liquidity_gap = pmax(0, 8.0 - liquidity_support),
    workforce_gap = pmax(0, 8.0 - workforce_capacity),
    adjusted_value =
      local_resilience_value -
      0.08 * equity_gap -
      0.06 * liquidity_gap -
      0.06 * workforce_gap
  )

p1 <- ggplot(ranked_results, aes(x = strategy, y = adjusted_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Local Economic Resilience Strategy Value Across Priority Scenarios",
    x = "Strategy",
    y = "Adjusted Local Resilience Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_local_economic_resilience_strategy_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_local_economic_resilience_strategy_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_local_economic_resilience_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_local_economic_resilience_strategy_profiles.csv"))

print(top_rank_summary)
