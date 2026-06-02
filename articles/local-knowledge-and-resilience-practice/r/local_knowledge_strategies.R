# Local knowledge and resilience practice strategy scoring workflow.
# Run: Rscript r/local_knowledge_strategies.R
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

strategies_path <- file.path(root, "data", "raw", "local_knowledge_strategies.csv")
scenarios_path <- file.path(root, "data", "raw", "local_knowledge_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(strategies_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_strategies <- function(data, scenario_row) {
  data %>%
    mutate(
      knowledge_integration_value =
        scenario_row$participation_access_weight * participation_access +
        scenario_row$knowledge_diversity_weight * knowledge_diversity +
        scenario_row$decision_influence_weight * decision_influence +
        scenario_row$trust_building_weight * trust_building +
        scenario_row$knowledge_protection_weight * knowledge_protection +
        scenario_row$reciprocity_weight * reciprocity +
        scenario_row$implementation_accountability_weight * implementation_accountability -
        scenario_row$implementation_burden_weight * implementation_burden,
      extraction_risk_gap = pmax(0, decision_influence - implementation_accountability),
      protection_gap = pmax(0, 8.4 - knowledge_protection),
      adjusted_value = knowledge_integration_value - 0.08 * extraction_risk_gap - 0.08 * protection_gap,
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
    knowledge_integration_value =
      0.14 * participation_access +
      0.14 * knowledge_diversity +
      0.15 * decision_influence +
      0.14 * trust_building +
      0.14 * knowledge_protection +
      0.14 * reciprocity +
      0.15 * implementation_accountability -
      0.02 * implementation_burden,
    extraction_risk_gap = pmax(0, decision_influence - implementation_accountability),
    protection_gap = pmax(0, 8.4 - knowledge_protection),
    adjusted_value = knowledge_integration_value - 0.08 * extraction_risk_gap - 0.08 * protection_gap
  )

p1 <- ggplot(ranked_results, aes(x = strategy, y = adjusted_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Local-Knowledge Integration Strategy Value Across Priority Scenarios",
    x = "Strategy",
    y = "Adjusted Knowledge Integration Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_local_knowledge_strategy_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_local_knowledge_strategy_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_local_knowledge_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_local_knowledge_strategy_profiles.csv"))

print(top_rank_summary)
