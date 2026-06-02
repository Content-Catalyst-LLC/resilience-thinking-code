# Risk governance and resilience indicators
#
# Run:
#   Rscript r/risk_governance_resilience_indicators.R
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

profiles_path <- file.path(root, "data", "raw", "risk_governance_resilience_profiles.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(profiles_path, show_col_types = FALSE)

profiles <- systems %>%
  mutate(
    risk_pressure =
      hazard_intensity * exposure * vulnerability * (1 - 0.55 * adaptive_capacity),
    governance_capacity =
      0.18 * trust +
      0.17 * participation_quality +
      0.17 * knowledge_integration +
      0.18 * coordination_quality +
      0.15 * transparency +
      0.15 * accountability,
    resilience_capacity =
      0.26 * buffer_capacity +
      0.28 * adaptive_capacity +
      0.22 * learning_capacity +
      0.24 * governance_capacity,
    resilience_margin =
      buffer_capacity +
      adaptive_capacity +
      learning_capacity +
      governance_capacity -
      risk_pressure -
      vulnerability,
    diagnostic = case_when(
      resilience_margin < 1.05 ~ "High governance-resilience concern",
      resilience_margin < 1.45 ~ "Moderate governance-resilience concern",
      TRUE ~ "Stronger governance-resilience position"
    )
  )

profiles_long <- profiles %>%
  select(system_type, risk_pressure, governance_capacity, resilience_capacity, resilience_margin) %>%
  pivot_longer(
    cols = c(risk_pressure, governance_capacity, resilience_capacity, resilience_margin),
    names_to = "indicator",
    values_to = "value"
  )

p <- ggplot(
  profiles_long,
  aes(x = reorder(system_type, value), y = value, fill = indicator)
) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "Risk Governance and Resilience Indicators",
    x = "System type",
    y = "Indicator value",
    fill = "Indicator"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_risk_governance_resilience_indicators.png"),
  plot = p,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(profiles, file.path(out_tables, "r_risk_governance_profiles.csv"))
write_csv(profiles_long, file.path(out_tables, "r_risk_governance_profiles_long.csv"))

print(profiles %>% select(system_type, risk_pressure, governance_capacity, resilience_margin, diagnostic))
