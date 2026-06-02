# Run: Rscript r/future_resilience_strategy_portfolios.R
# Requires: install.packages("tidyverse")

suppressPackageStartupMessages(library(tidyverse))

args <- commandArgs(trailingOnly = FALSE)
file_arg <- args[grepl("^--file=", args)]
root <- if (length(file_arg) > 0) normalizePath(file.path(dirname(sub("^--file=", "", file_arg[1])), "..")) else getwd()

out_tables <- file.path(root, "outputs", "tables")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(file.path(root, "data", "raw", "future_resilience_strategies.csv"), show_col_types = FALSE)
scenarios <- read_csv(file.path(root, "data", "raw", "future_resilience_priority_scenarios.csv"), show_col_types = FALSE)

score_one <- function(data, s) {
  data %>%
    mutate(
      resilience_value =
        s$adaptive_capacity_weight * adaptive_capacity +
        s$buffering_capacity_weight * buffering_capacity +
        s$transformability_weight * transformability +
        s$governance_quality_weight * governance_quality +
        s$equity_performance_weight * equity_performance +
        s$digital_resilience_weight * digital_resilience +
        s$climate_readiness_weight * climate_readiness -
        s$systemic_exposure_weight * systemic_exposure -
        s$implementation_burden_weight * implementation_burden,
      governance_gap = pmax(0, 8.5 - governance_quality),
      equity_gap = pmax(0, 8.5 - equity_performance),
      adjusted_value = resilience_value - 0.06 * governance_gap - 0.08 * equity_gap,
      scenario = s$scenario
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

write_csv(rankings, file.path(out_tables, "r_future_resilience_strategy_rankings.csv"))
write_csv(top_summary, file.path(out_tables, "r_future_resilience_top_rank_summary.csv"))

print(top_summary)
