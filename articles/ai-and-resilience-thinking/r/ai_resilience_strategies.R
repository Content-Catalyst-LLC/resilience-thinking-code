# AI resilience strategy scoring workflow.
# Run: Rscript r/ai_resilience_strategies.R
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

strategies_path <- file.path(root, "data", "raw", "ai_resilience_strategies.csv")
scenarios_path <- file.path(root, "data", "raw", "ai_resilience_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read_csv(strategies_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_strategies <- function(data, scenario_row) {
  data %>%
    mutate(
      ai_resilience_value =
        scenario_row$monitoring_value_weight * monitoring_value +
        scenario_row$forecasting_value_weight * forecasting_value +
        scenario_row$scenario_value_weight * scenario_value +
        scenario_row$decision_support_weight * decision_support +
        scenario_row$governance_quality_weight * governance_quality +
        scenario_row$equity_safeguards_weight * equity_safeguards +
        scenario_row$human_oversight_weight * human_oversight +
        scenario_row$local_knowledge_weight * local_knowledge +
        scenario_row$security_resilience_weight * security_resilience -
        scenario_row$ai_risk_weight * ai_risk -
        scenario_row$implementation_burden_weight * implementation_burden,
      governance_gap = pmax(0, 8.5 - governance_quality),
      equity_gap = pmax(0, 8.5 - equity_safeguards),
      human_gap = pmax(0, 8.5 - human_oversight),
      local_gap = pmax(0, 8.2 - local_knowledge),
      adjusted_value =
        ai_resilience_value -
        0.07 * governance_gap -
        0.08 * equity_gap -
        0.08 * human_gap -
        0.06 * local_gap,
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
    ai_resilience_value =
      0.11 * monitoring_value +
      0.10 * forecasting_value +
      0.11 * scenario_value +
      0.11 * decision_support +
      0.12 * governance_quality +
      0.12 * equity_safeguards +
      0.12 * human_oversight +
      0.10 * local_knowledge +
      0.10 * security_resilience -
      0.05 * ai_risk -
      0.04 * implementation_burden
  )

p1 <- ggplot(ranked_results, aes(x = strategy, y = adjusted_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "AI Resilience Strategy Value Across Priority Scenarios",
    x = "AI Resilience Strategy",
    y = "Adjusted AI Resilience Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_ai_resilience_strategy_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_ai_resilience_strategy_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_ai_resilience_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_ai_resilience_strategy_profiles.csv"))

print(top_rank_summary)
