# Transformation pathway scoring workflow
#
# Run:
#   Rscript r/transformation_pathways.R
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

pathways_path <- file.path(root, "data", "raw", "transformation_pathways.csv")
scenarios_path <- file.path(root, "data", "raw", "transformation_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

pathways <- read_csv(pathways_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_pathways <- function(data, scenario_row) {
  data %>%
    mutate(
      transformation_value =
        scenario_row$adaptive_support_weight * adaptive_support +
        scenario_row$transformability_weight * transformability +
        scenario_row$governance_readiness_weight * governance_readiness +
        scenario_row$justice_contribution_weight * justice_contribution +
        scenario_row$ecological_viability_weight * ecological_viability +
        scenario_row$legitimacy_weight * legitimacy +
        scenario_row$resource_feasibility_weight * resource_feasibility -
        scenario_row$structural_risk_weight * structural_risk,
      scenario = scenario_row$scenario
    ) %>%
    arrange(desc(transformation_value)) %>%
    mutate(rank = row_number())
}

ranked_results <- scenarios %>%
  group_split(scenario) %>%
  map_dfr(~ score_pathways(pathways, .x[1, ]))

top_rank_summary <- ranked_results %>%
  filter(rank == 1) %>%
  count(pathway, name = "times_ranked_first") %>%
  arrange(desc(times_ranked_first))

readiness <- pathways %>%
  mutate(
    transformation_readiness =
      0.18 * adaptive_support +
      0.20 * transformability +
      0.18 * governance_readiness +
      0.16 * justice_contribution +
      0.14 * ecological_viability +
      0.08 * legitimacy +
      0.06 * resource_feasibility -
      0.10 * structural_risk
  )

p1 <- ggplot(ranked_results, aes(x = pathway, y = transformation_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Transformation Pathway Value Across Strategic Priority Scenarios",
    x = "Pathway",
    y = "Weighted Transformation Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_transformation_pathway_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(readiness, aes(x = reorder(pathway, transformation_readiness), y = transformation_readiness)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Transformation Readiness by Pathway",
    x = "Pathway",
    y = "Transformation Readiness"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_transformation_readiness.png"),
  plot = p2,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_transformation_pathway_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_transformation_top_rank_summary.csv"))
write_csv(readiness, file.path(out_tables, "r_transformation_readiness.csv"))

print(top_rank_summary)
