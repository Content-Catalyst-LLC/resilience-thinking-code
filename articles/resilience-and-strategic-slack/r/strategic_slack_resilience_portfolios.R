# Strategic slack portfolio scoring workflow.
# Run: Rscript r/strategic_slack_resilience_portfolios.R
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

portfolios_path <- file.path(root, "data", "raw", "strategic_slack_portfolios.csv")
scenarios_path <- file.path(root, "data", "raw", "strategic_slack_scenarios.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

portfolios <- read_csv(portfolios_path, show_col_types = FALSE)
scenarios <- read_csv(scenarios_path, show_col_types = FALSE)

score_portfolios <- function(data, scenario_row) {
  data %>%
    mutate(
      slack_resilience_value =
        scenario_row$financial_slack_weight * financial_slack +
        scenario_row$workforce_slack_weight * workforce_slack +
        scenario_row$operational_slack_weight * operational_slack +
        scenario_row$knowledge_slack_weight * knowledge_slack +
        scenario_row$network_slack_weight * network_slack +
        scenario_row$governance_slack_weight * governance_slack +
        scenario_row$ethical_safeguards_weight * ethical_safeguards -
        scenario_row$ethical_burden_weight * ethical_burden -
        scenario_row$implementation_burden_weight * implementation_burden,
      workforce_gap = pmax(0, 8.2 - workforce_slack),
      knowledge_gap = pmax(0, 8.2 - knowledge_slack),
      governance_gap = pmax(0, 8.2 - governance_slack),
      adjusted_value =
        slack_resilience_value -
        0.07 * workforce_gap -
        0.06 * knowledge_gap -
        0.06 * governance_gap,
      scenario = scenario_row$scenario
    ) %>%
    arrange(desc(adjusted_value)) %>%
    mutate(rank = row_number())
}

ranked_results <- scenarios %>%
  group_split(scenario) %>%
  map_dfr(~ score_portfolios(portfolios, .x[1, ]))

top_rank_summary <- ranked_results %>%
  filter(rank == 1) %>%
  count(portfolio, name = "times_ranked_first") %>%
  arrange(desc(times_ranked_first))

profiles <- portfolios %>%
  mutate(
    slack_resilience_value =
      0.13 * financial_slack +
      0.14 * workforce_slack +
      0.13 * operational_slack +
      0.13 * knowledge_slack +
      0.13 * network_slack +
      0.14 * governance_slack +
      0.13 * ethical_safeguards -
      0.04 * ethical_burden -
      0.03 * implementation_burden,
    workforce_gap = pmax(0, 8.2 - workforce_slack),
    knowledge_gap = pmax(0, 8.2 - knowledge_slack),
    governance_gap = pmax(0, 8.2 - governance_slack),
    adjusted_value =
      slack_resilience_value -
      0.07 * workforce_gap -
      0.06 * knowledge_gap -
      0.06 * governance_gap
  )

p1 <- ggplot(ranked_results, aes(x = portfolio, y = adjusted_value, group = scenario)) +
  geom_point(size = 3) +
  geom_line(aes(color = scenario), linewidth = 1) +
  coord_flip() +
  labs(
    title = "Strategic Slack Portfolio Value Across Priority Scenarios",
    x = "Slack Portfolio",
    y = "Adjusted Slack Resilience Value",
    color = "Scenario"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_strategic_slack_portfolio_rankings.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(ranked_results, file.path(out_tables, "r_strategic_slack_portfolio_rankings.csv"))
write_csv(top_rank_summary, file.path(out_tables, "r_strategic_slack_top_rank_summary.csv"))
write_csv(profiles, file.path(out_tables, "r_strategic_slack_portfolio_profiles.csv"))

print(top_rank_summary)
