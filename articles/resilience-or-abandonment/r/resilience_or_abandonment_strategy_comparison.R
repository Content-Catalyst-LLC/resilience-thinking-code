# Run: Rscript r/resilience_or_abandonment_strategy_comparison.R
# Requires: install.packages("tidyverse")

suppressPackageStartupMessages(library(tidyverse))

args <- commandArgs(trailingOnly = FALSE)
file_arg <- args[grepl("^--file=", args)]
root <- if (length(file_arg) > 0) normalizePath(file.path(dirname(sub("^--file=", "", file_arg[1])), "..")) else getwd()

out_tables <- file.path(root, "outputs", "tables")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(file.path(root, "data", "raw", "resilience_or_abandonment_strategies.csv"), show_col_types = FALSE)
scenarios <- read_csv(file.path(root, "data", "raw", "abandonment_priority_scenarios.csv"), show_col_types = FALSE)

score_one <- function(data, s) {
  data %>%
    mutate(
      support_resilience_value =
        s$protective_effectiveness_weight * protective_effectiveness +
        s$material_support_weight * material_support +
        s$accessible_recovery_weight * accessible_recovery +
        s$governance_inclusion_weight * governance_inclusion +
        s$transformation_potential_weight * transformation_potential +
        s$exposure_reduction_weight * exposure_reduction -
        s$burden_shift_weight * burden_shift -
        s$implementation_burden_weight * implementation_burden,
      support_gap = pmax(0, 8.0 - material_support),
      recovery_gap = pmax(0, 8.0 - accessible_recovery),
      governance_gap = pmax(0, 8.0 - governance_inclusion),
      abandonment_risk =
        0.32 * support_gap +
        0.24 * recovery_gap +
        0.22 * governance_gap +
        0.14 * burden_shift +
        0.08 * pmax(0, 8.0 - exposure_reduction),
      adjusted_value = support_resilience_value - abandonment_risk,
      scenario = s$scenario,
      diagnostic = case_when(
        abandonment_risk >= 2.4 ~ "high abandonment-risk review needed",
        burden_shift >= 5.5 ~ "burden-shifting review needed",
        material_support < 6.0 ~ "material-support gap",
        accessible_recovery < 6.0 ~ "recovery-access gap",
        governance_inclusion < 6.0 ~ "participation and authority gap",
        TRUE ~ "support-oriented resilience candidate"
      )
    ) %>%
    arrange(desc(adjusted_value)) %>%
    mutate(rank = row_number())
}

rankings <- scenarios %>%
  group_split(scenario) %>%
  map_dfr(~ score_one(strategies, .x[1, ]))

top_summary <- rankings %>%
  filter(rank == 1) %>%
  count(strategy, name = "times_ranked_first") %>%
  arrange(desc(times_ranked_first))

write_csv(rankings, file.path(out_tables, "r_resilience_or_abandonment_strategy_rankings.csv"))
write_csv(top_summary, file.path(out_tables, "r_resilience_or_abandonment_top_rank_summary.csv"))

print(top_summary)
