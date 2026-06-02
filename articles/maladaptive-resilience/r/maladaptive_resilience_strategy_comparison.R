# Run: Rscript r/maladaptive_resilience_strategy_comparison.R
# Requires: install.packages("tidyverse")

suppressPackageStartupMessages(library(tidyverse))

args <- commandArgs(trailingOnly = FALSE)
file_arg <- args[grepl("^--file=", args)]
root <- if (length(file_arg) > 0) normalizePath(file.path(dirname(sub("^--file=", "", file_arg[1])), "..")) else getwd()

out_tables <- file.path(root, "outputs", "tables")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(file.path(root, "data", "raw", "maladaptive_resilience_strategies.csv"), show_col_types = FALSE)
scenarios <- read_csv(file.path(root, "data", "raw", "maladaptive_priority_scenarios.csv"), show_col_types = FALSE)

score_one <- function(data, s) {
  data %>%
    mutate(
      adaptive_resilience_value =
        s$persistence_capacity_weight * persistence_capacity +
        s$harm_reduction_weight * harm_reduction +
        s$lock_in_reduction_weight * lock_in_reduction +
        s$equity_weight * equity +
        s$transformation_capacity_weight * transformation_capacity +
        s$ecological_integrity_weight * ecological_integrity -
        s$burden_shift_weight * burden_shift -
        s$implementation_burden_weight * implementation_burden,
      maladaptive_risk =
        0.28 * pmax(0, 8.0 - harm_reduction) +
        0.24 * pmax(0, 8.0 - lock_in_reduction) +
        0.20 * pmax(0, 8.0 - transformation_capacity) +
        0.16 * burden_shift +
        0.12 * pmax(0, 8.0 - equity),
      adjusted_value = adaptive_resilience_value - maladaptive_risk,
      scenario = s$scenario,
      diagnostic = case_when(
        maladaptive_risk >= 3.0 ~ "high maladaptive-resilience risk",
        burden_shift >= 5.5 ~ "burden-shifting review needed",
        harm_reduction < 6.0 ~ "harm-reduction gap",
        lock_in_reduction < 6.0 ~ "lock-in reduction gap",
        transformation_capacity < 6.0 ~ "transformation gap",
        TRUE ~ "adaptive resilience candidate"
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

write_csv(rankings, file.path(out_tables, "r_maladaptive_resilience_strategy_rankings.csv"))
write_csv(top_summary, file.path(out_tables, "r_maladaptive_resilience_top_rank_summary.csv"))

print(top_summary)
