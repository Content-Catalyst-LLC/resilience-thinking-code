# Resilience indicator and dashboard-risk scoring workflow
#
# Run:
#   Rscript r/resilience_dashboard_designs.R
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

designs_path <- file.path(root, "data", "raw", "dashboard_designs.csv")
scenarios_path <- file.path(root, "data", "raw", "dashboard_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

designs <- read_csv(designs_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_dashboards <- function(data, scenario_row) {
  data %>%
    mutate(
      dashboard_value =
        scenario_row$indicator_coverage_weight * indicator_coverage +
        scenario_row$threshold_sensitivity_weight * threshold_sensitivity +
        scenario_row$justice_visibility_weight * justice_visibility +
        scenario_row$uncertainty_transparency_weight * uncertainty_transparency +
        scenario_row$decision_trigger_clarity_weight * decision_trigger_clarity +
        scenario_row$learning_integration_weight * learning_integration -
        scenario_row$dashboard_risk_weight * dashboard_risk,
      scenario = scenario_row$scenario
    ) %>%
    arrange(desc(dashboard_value)) %>%
    mutate(rank = row_number())
}

ranked_results <- scenarios %>%
  group_split(scenario) %>%
  map_dfr(~ score_dashboards(designs, .x[1, ]))

top_rank_summary <- ranked_results %>%
  filter(rank == 1) %>%
  count(dashboard, name = "times_ranked_first") %>%
  arrange(desc(times_ranked_first))

profiles <- designs %>%
  mutate(
    base_dashboard_value =
      0.15 * indicator_coverage +
      0.17 * threshold_sensitivity +
      0.16 * justice_visibility +
      0.14 * uncertainty_transparency +
      0.16 * decision_trigger_clarity +
      0.14 * learning_integration -
      0.08 * dashboard_risk
  )

p1 <- ggplot(ranked_results, aes(x = dashboard, y = dashboard_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Resilience Dashboard Design Value Across Priorities",
    x = "Dashboard Design",
    y = "Weighted Dashboard Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_resilience_dashboard_design_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(profiles, aes(x = reorder(dashboard, base_dashboard_value), y = base_dashboard_value)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Base Dashboard Value by Design",
    x = "Dashboard Design",
    y = "Base Dashboard Value"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_base_dashboard_value.png"),
  plot = p2,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_resilience_dashboard_design_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_resilience_dashboard_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_resilience_dashboard_design_profiles.csv"))

print(top_rank_summary)
