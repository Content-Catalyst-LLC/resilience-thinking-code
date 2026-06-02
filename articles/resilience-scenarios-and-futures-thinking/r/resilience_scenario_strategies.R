# Run: Rscript r/resilience_scenario_strategies.R
# Requires: install.packages("tidyverse")

suppressPackageStartupMessages(library(tidyverse))

args <- commandArgs(trailingOnly = FALSE)
file_arg <- args[grepl("^--file=", args)]
root <- if (length(file_arg) > 0) normalizePath(file.path(dirname(sub("^--file=", "", file_arg[1])), "..")) else getwd()

out_tables <- file.path(root, "outputs", "tables")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(file.path(root, "data", "raw", "resilience_scenario_strategies.csv"), show_col_types = FALSE)

profiles <- strategies %>%
  mutate(
    scenario_resilience_value =
      0.10 * horizon_scanning +
      0.10 * weak_signal_detection +
      0.11 * stress_testing +
      0.12 * adaptive_pathways +
      0.11 * participation +
      0.10 * data_modeling +
      0.12 * governance_integration +
      0.12 * equity_sensitivity +
      0.12 * transformation_potential -
      0.04 * scenario_design_risk -
      0.04 * implementation_burden,
    diagnostic = case_when(
      implementation_burden >= 3.9 ~ "implementation-burden review needed",
      scenario_design_risk >= 3.0 ~ "scenario-design risk review needed",
      participation < 8.2 ~ "participation review needed",
      equity_sensitivity < 8.2 ~ "equity review needed",
      governance_integration < 8.4 ~ "governance integration review needed",
      TRUE ~ "promising but requires iterative revision"
    )
  ) %>%
  arrange(desc(scenario_resilience_value))

write_csv(profiles, file.path(out_tables, "r_resilience_scenario_strategy_profiles.csv"))
print(profiles)
