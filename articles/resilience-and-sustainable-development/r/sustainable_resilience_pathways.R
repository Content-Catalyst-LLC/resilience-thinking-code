# Sustainable resilience pathway scoring workflow.
# Run: Rscript r/sustainable_resilience_pathways.R
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

pathways_path <- file.path(root, "data", "raw", "sustainable_resilience_pathways.csv")
scenarios_path <- file.path(root, "data", "raw", "sustainable_resilience_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

pathways <- read_csv(pathways_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_pathways <- function(data, scenario_row) {
  data %>%
    mutate(
      viability_value =
        scenario_row$resilience_weight * resilience +
        scenario_row$ecological_integrity_weight * ecological_integrity +
        scenario_row$social_inclusion_weight * social_inclusion +
        scenario_row$economic_sufficiency_weight * economic_sufficiency +
        scenario_row$governance_capacity_weight * governance_capacity +
        scenario_row$adaptive_capacity_weight * adaptive_capacity -
        scenario_row$resource_pressure_weight * resource_pressure -
        scenario_row$implementation_burden_weight * implementation_burden,
      boundary_adjusted_viability =
        viability_value -
        pmax(0, resource_pressure - 3.8) * 0.20 -
        pmax(0, 8.2 - social_inclusion) * 0.12 -
        pmax(0, 8.2 - ecological_integrity) * 0.12,
      scenario = scenario_row$scenario
    ) %>%
    arrange(desc(viability_value)) %>%
    mutate(rank = row_number())
}

ranked_results <- scenarios %>%
  group_split(scenario) %>%
  map_dfr(~ score_pathways(pathways, .x[1, ]))

top_rank_summary <- ranked_results %>%
  filter(rank == 1) %>%
  count(pathway, name = "times_ranked_first") %>%
  arrange(desc(times_ranked_first))

profiles <- pathways %>%
  mutate(
    viability_value =
      0.18 * resilience +
      0.17 * ecological_integrity +
      0.16 * social_inclusion +
      0.14 * economic_sufficiency +
      0.14 * governance_capacity +
      0.15 * adaptive_capacity -
      0.04 * resource_pressure -
      0.02 * implementation_burden,
    boundary_adjusted_viability =
      viability_value -
      pmax(0, resource_pressure - 3.8) * 0.20 -
      pmax(0, 8.2 - social_inclusion) * 0.12 -
      pmax(0, 8.2 - ecological_integrity) * 0.12
  )

p1 <- ggplot(ranked_results, aes(x = pathway, y = viability_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Sustainable Resilience Pathway Value Across Priority Scenarios",
    x = "Pathway",
    y = "Weighted Viability Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_sustainable_resilience_pathway_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_sustainable_resilience_pathway_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_sustainable_resilience_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_sustainable_resilience_pathway_profiles.csv"))

print(top_rank_summary)
