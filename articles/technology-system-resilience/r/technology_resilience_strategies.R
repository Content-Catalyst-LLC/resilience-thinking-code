# Technology resilience strategy scoring workflow.
# Run: Rscript r/technology_resilience_strategies.R
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

strategies_path <- file.path(root, "data", "raw", "technology_resilience_strategies.csv")
scenarios_path <- file.path(root, "data", "raw", "technology_resilience_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(strategies_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_strategies <- function(data, scenario_row) {
  data %>%
    mutate(
      technology_resilience_value =
        scenario_row$architecture_weight * architecture +
        scenario_row$redundancy_weight * redundancy +
        scenario_row$observability_weight * observability +
        scenario_row$cybersecurity_weight * cybersecurity +
        scenario_row$data_integrity_weight * data_integrity +
        scenario_row$maintainability_weight * maintainability +
        scenario_row$governance_weight * governance +
        scenario_row$human_safeguards_weight * human_safeguards +
        scenario_row$vendor_contingency_weight * vendor_contingency -
        scenario_row$technical_debt_risk_weight * technical_debt_risk -
        scenario_row$implementation_burden_weight * implementation_burden,
      maintainability_gap = pmax(0, 8.3 - maintainability),
      governance_gap = pmax(0, 8.3 - governance),
      human_gap = pmax(0, 8.2 - human_safeguards),
      vendor_gap = pmax(0, 8.0 - vendor_contingency),
      adjusted_value =
        technology_resilience_value -
        0.06 * maintainability_gap -
        0.06 * governance_gap -
        0.07 * human_gap -
        0.05 * vendor_gap,
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
    technology_resilience_value =
      0.10 * architecture +
      0.10 * redundancy +
      0.10 * observability +
      0.11 * cybersecurity +
      0.11 * data_integrity +
      0.11 * maintainability +
      0.11 * governance +
      0.11 * human_safeguards +
      0.10 * vendor_contingency -
      0.03 * technical_debt_risk -
      0.02 * implementation_burden,
    maintainability_gap = pmax(0, 8.3 - maintainability),
    governance_gap = pmax(0, 8.3 - governance),
    human_gap = pmax(0, 8.2 - human_safeguards),
    vendor_gap = pmax(0, 8.0 - vendor_contingency),
    adjusted_value =
      technology_resilience_value -
      0.06 * maintainability_gap -
      0.06 * governance_gap -
      0.07 * human_gap -
      0.05 * vendor_gap
  )

p1 <- ggplot(ranked_results, aes(x = strategy, y = adjusted_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Technology Resilience Strategy Value Across Priority Scenarios",
    x = "Strategy",
    y = "Adjusted Technology Resilience Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_technology_resilience_strategy_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_technology_resilience_strategy_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_technology_resilience_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_technology_resilience_strategy_profiles.csv"))

print(top_rank_summary)
