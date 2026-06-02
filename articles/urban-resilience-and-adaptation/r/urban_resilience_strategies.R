# Urban resilience strategy scoring workflow
#
# Run:
#   Rscript r/urban_resilience_strategies.R
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

strategies_path <- file.path(root, "data", "raw", "urban_resilience_strategies.csv")
scenarios_path <- file.path(root, "data", "raw", "urban_resilience_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(strategies_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_strategies <- function(data, scenario_row) {
  data %>%
    mutate(
      resilience_value =
        scenario_row$exposure_reduction_weight * exposure_reduction +
        scenario_row$vulnerability_reduction_weight * vulnerability_reduction +
        scenario_row$service_continuity_weight * service_continuity +
        scenario_row$adaptive_capacity_weight * adaptive_capacity +
        scenario_row$ecological_buffering_weight * ecological_buffering +
        scenario_row$equity_protection_weight * equity_protection -
        scenario_row$maladaptation_risk_weight * maladaptation_risk,
      scenario = scenario_row$scenario
    ) %>%
    arrange(desc(resilience_value)) %>%
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
    base_resilience_value =
      0.16 * exposure_reduction +
      0.17 * vulnerability_reduction +
      0.17 * service_continuity +
      0.15 * adaptive_capacity +
      0.14 * ecological_buffering +
      0.15 * equity_protection -
      0.06 * maladaptation_risk,
    equity_adjusted_value = base_resilience_value * (0.72 + 0.028 * equity_protection)
  )

p1 <- ggplot(ranked_results, aes(x = strategy, y = resilience_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Urban Resilience Strategy Value Across Priority Scenarios",
    x = "Strategy",
    y = "Weighted Resilience Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_urban_resilience_strategy_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(profiles, aes(x = reorder(strategy, base_resilience_value), y = base_resilience_value)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Base Urban Resilience Value by Strategy",
    x = "Strategy",
    y = "Base Resilience Value"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_base_urban_resilience_value.png"),
  plot = p2,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_urban_resilience_strategy_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_urban_resilience_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_urban_resilience_strategy_profiles.csv"))

print(top_rank_summary)
