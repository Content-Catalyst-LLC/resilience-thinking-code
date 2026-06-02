# Systems thinking and resilience thinking indicators
#
# Run:
#   Rscript r/systems_resilience_indicators.R
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

profiles_path <- file.path(root, "data", "raw", "systems_resilience_profiles.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(profiles_path, show_col_types = FALSE)

profiles <- systems %>%
  mutate(
    systems_thinking_score =
      0.28 * feedback_visibility +
      0.24 * boundary_clarity +
      0.24 * leverage_capacity +
      0.24 * delay_management,
    resilience_thinking_score =
      0.24 * adaptive_capacity +
      0.20 * redundancy +
      0.22 * threshold_distance +
      0.18 * buffer_capacity -
      0.08 * vulnerability_pressure -
      0.08 * disturbance_exposure,
    combined_system_resilience =
      0.50 * systems_thinking_score +
      0.50 * resilience_thinking_score,
    diagnostic = case_when(
      systems_thinking_score < 0.55 & resilience_thinking_score < 0.55 ~
        "Weak structure visibility and weak resilience capacity",
      systems_thinking_score >= 0.65 & resilience_thinking_score >= 0.65 ~
        "Strong structural understanding and resilience capacity",
      systems_thinking_score > resilience_thinking_score ~
        "System structure is visible, but resilience capacity needs strengthening",
      TRUE ~
        "Resilience capacity exists, but system structure needs clearer mapping"
    )
  )

profiles_long <- profiles %>%
  select(system_type, systems_thinking_score, resilience_thinking_score, combined_system_resilience) %>%
  pivot_longer(
    cols = c(systems_thinking_score, resilience_thinking_score, combined_system_resilience),
    names_to = "index",
    values_to = "score"
  )

p <- ggplot(
  profiles_long,
  aes(x = reorder(system_type, score), y = score, fill = index)
) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "Systems Thinking and Resilience Thinking Indicators",
    x = "System type",
    y = "Score",
    fill = "Index"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_systems_resilience_indicators.png"),
  plot = p,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(profiles, file.path(out_tables, "r_systems_resilience_profiles.csv"))
write_csv(profiles_long, file.path(out_tables, "r_systems_resilience_profiles_long.csv"))

print(profiles %>% select(system_type, systems_thinking_score, resilience_thinking_score, combined_system_resilience, diagnostic))
