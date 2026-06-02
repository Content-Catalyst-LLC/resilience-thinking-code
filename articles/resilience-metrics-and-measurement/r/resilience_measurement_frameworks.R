# Resilience measurement framework scoring workflow
#
# Run:
#   Rscript r/resilience_measurement_frameworks.R
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

frameworks_path <- file.path(root, "data", "raw", "resilience_measurement_frameworks.csv")
scenarios_path <- file.path(root, "data", "raw", "resilience_measurement_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

frameworks <- read_csv(frameworks_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_frameworks <- function(data, scenario_row) {
  data %>%
    mutate(
      metric_value =
        scenario_row$resistance_coverage_weight * resistance_coverage +
        scenario_row$recovery_insight_weight * recovery_insight +
        scenario_row$adaptive_capacity_visibility_weight * adaptive_capacity_visibility +
        scenario_row$buffer_visibility_weight * buffer_visibility +
        scenario_row$justice_visibility_weight * justice_visibility +
        scenario_row$data_quality_transparency_weight * data_quality_transparency -
        scenario_row$threshold_blindness_weight * threshold_blindness,
      scenario = scenario_row$scenario
    ) %>%
    arrange(desc(metric_value)) %>%
    mutate(rank = row_number())
}

ranked_results <- scenarios %>%
  group_split(scenario) %>%
  map_dfr(~ score_frameworks(frameworks, .x[1, ]))

top_rank_summary <- ranked_results %>%
  filter(rank == 1) %>%
  count(framework, name = "times_ranked_first") %>%
  arrange(desc(times_ranked_first))

profiles <- frameworks %>%
  mutate(
    base_metric_value =
      0.16 * resistance_coverage +
      0.16 * recovery_insight +
      0.16 * adaptive_capacity_visibility +
      0.15 * buffer_visibility +
      0.13 * justice_visibility +
      0.10 * data_quality_transparency -
      0.14 * threshold_blindness
  )

p1 <- ggplot(ranked_results, aes(x = framework, y = metric_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Resilience Measurement Framework Value Across Priority Scenarios",
    x = "Framework",
    y = "Weighted Measurement Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_resilience_measurement_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(profiles, aes(x = reorder(framework, base_metric_value), y = base_metric_value)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Base Metric Value by Measurement Framework",
    x = "Framework",
    y = "Base Metric Value"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_base_metric_value.png"),
  plot = p2,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_resilience_measurement_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_resilience_measurement_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_resilience_measurement_profiles.csv"))

print(top_rank_summary)
