# Run: Rscript r/ethical_resilience_strategy_comparison.R
# Requires: install.packages("tidyverse")

suppressPackageStartupMessages(library(tidyverse))

args <- commandArgs(trailingOnly = FALSE)
file_arg <- args[grepl("^--file=", args)]
root <- if (length(file_arg) > 0) normalizePath(file.path(dirname(sub("^--file=", "", file_arg[1])), "..")) else getwd()

out_tables <- file.path(root, "outputs", "tables")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(file.path(root, "data", "raw", "ethical_resilience_strategies.csv"), show_col_types = FALSE)
scenarios <- read_csv(file.path(root, "data", "raw", "ethical_resilience_priority_scenarios.csv"), show_col_types = FALSE)

score_one <- function(data, s) {
  data %>%
    mutate(
      ethical_resilience_value =
        s$protection_effectiveness_weight * protection_effectiveness +
        s$equity_weight * equity +
        s$governance_legitimacy_weight * governance_legitimacy +
        s$recognition_weight * recognition +
        s$accountability_weight * accountability -
        s$burden_shift_weight * burden_shift -
        s$implementation_burden_weight * implementation_burden,
      equity_gap = pmax(0, 8.5 - equity),
      governance_gap = pmax(0, 8.5 - governance_legitimacy),
      recognition_gap = pmax(0, 8.5 - recognition),
      adjusted_value =
        ethical_resilience_value -
        0.06 * equity_gap -
        0.06 * governance_gap -
        0.05 * recognition_gap,
      scenario = s$scenario,
      diagnostic = case_when(
        burden_shift >= 5.0 ~ "burden-shifting review needed",
        equity < 7.5 ~ "equity-performance review needed",
        governance_legitimacy < 7.5 ~ "governance-legitimacy review needed",
        recognition < 7.5 ~ "recognition review needed",
        implementation_burden >= 4.0 ~ "implementation-burden review needed",
        TRUE ~ "promising but requires participatory validation"
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

write_csv(rankings, file.path(out_tables, "r_ethical_resilience_strategy_rankings.csv"))
write_csv(top_summary, file.path(out_tables, "r_ethical_resilience_top_rank_summary.csv"))

print(top_summary)
