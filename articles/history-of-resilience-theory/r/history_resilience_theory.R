# Historical expansion of resilience theory
#
# Run:
#   Rscript r/history_resilience_theory.R
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

data_path <- file.path(root, "data", "raw", "resilience_theory_historical_phases.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

history <- read_csv(data_path, show_col_types = FALSE) %>%
  mutate(
    influence_score =
      0.35 * conceptual_scope +
      0.25 * governance_relevance +
      0.25 * system_complexity +
      0.15 * justice_relevance
  )

history_long <- history %>%
  pivot_longer(
    cols = c(conceptual_scope, governance_relevance, system_complexity, justice_relevance),
    names_to = "dimension",
    values_to = "value"
  )

p1 <- ggplot(history_long, aes(x = start_year, y = value, color = dimension)) +
  geom_line(linewidth = 1.1) +
  geom_point(size = 2.4) +
  labs(
    title = "Stylized Historical Expansion of Resilience Theory",
    x = "Year",
    y = "Relative emphasis",
    color = "Dimension"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  file.path(out_figures, "r_historical_expansion_dimensions.png"),
  p1,
  width = 10,
  height = 6,
  dpi = 160
)

p2 <- ggplot(history, aes(x = reorder(period, influence_score), y = influence_score)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Stylized Influence Score Across Historical Phases",
    x = "Historical phase",
    y = "Influence score"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  file.path(out_figures, "r_historical_phase_influence_scores.png"),
  p2,
  width = 10,
  height = 7,
  dpi = 160
)

write_csv(history, file.path(out_tables, "r_history_phase_scores.csv"))
write_csv(history_long, file.path(out_tables, "r_history_phase_scores_long.csv"))

print(history %>% select(period, start_year, influence_score))
