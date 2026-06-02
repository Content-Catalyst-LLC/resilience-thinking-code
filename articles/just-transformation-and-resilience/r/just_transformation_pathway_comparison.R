# Run: Rscript r/just_transformation_pathway_comparison.R
# Requires: install.packages("tidyverse")

suppressPackageStartupMessages(library(tidyverse))

args <- commandArgs(trailingOnly = FALSE)
file_arg <- args[grepl("^--file=", args)]
root <- if (length(file_arg) > 0) normalizePath(file.path(dirname(sub("^--file=", "", file_arg[1])), "..")) else getwd()

out_tables <- file.path(root, "outputs", "tables")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)

pathways <- read_csv(file.path(root, "data", "raw", "just_transformation_pathways.csv"), show_col_types = FALSE)
scenarios <- read_csv(file.path(root, "data", "raw", "just_transformation_priority_scenarios.csv"), show_col_types = FALSE)

score_one <- function(data, s) {
  data %>%
    mutate(
      just_transformation_value =
        s$resilience_capacity_weight * resilience_capacity +
        s$transformation_capacity_weight * transformation_capacity +
        s$equity_weight * equity +
        s$ecological_repair_weight * ecological_repair +
        s$governance_legitimacy_weight * governance_legitimacy +
        s$livelihood_protection_weight * livelihood_protection +
        s$exposure_reduction_weight * exposure_reduction -
        s$burden_shift_weight * burden_shift -
        s$lock_in_risk_weight * lock_in_risk -
        s$implementation_burden_weight * implementation_burden,
      justice_gap =
        0.24 * pmax(0, 8.5 - equity) +
        0.22 * pmax(0, 8.5 - governance_legitimacy) +
        0.20 * pmax(0, 8.5 - livelihood_protection) +
        0.18 * burden_shift +
        0.16 * lock_in_risk,
      adjusted_value = just_transformation_value - justice_gap,
      scenario = s$scenario,
      diagnostic = case_when(
        justice_gap >= 3.0 ~ "high justice-gap review needed",
        burden_shift >= 5.5 ~ "burden-shifting review needed",
        equity < 7.0 ~ "equity gap",
        governance_legitimacy < 7.0 ~ "governance legitimacy gap",
        livelihood_protection < 7.0 ~ "livelihood protection gap",
        TRUE ~ "just transformation candidate"
      )
    ) %>%
    arrange(desc(adjusted_value)) %>%
    mutate(rank = row_number())
}

rankings <- scenarios %>%
  group_split(scenario) %>%
  map_dfr(~ score_one(pathways, .x[1, ]))

top_summary <- rankings %>%
  filter(rank == 1) %>%
  count(pathway, name = "times_ranked_first") %>%
  arrange(desc(times_ranked_first))

write_csv(rankings, file.path(out_tables, "r_just_transformation_pathway_rankings.csv"))
write_csv(top_summary, file.path(out_tables, "r_just_transformation_top_rank_summary.csv"))

print(top_summary)
