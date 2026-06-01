# Resilience profiles and vulnerability flags
#
# Run:
#   Rscript r/resilience_profiles.R
#
# Requires:
#   install.packages("tidyverse")

suppressPackageStartupMessages({
  library(tidyverse)
})

root <- normalizePath(file.path(dirname(commandArgs(trailingOnly = FALSE)[grep("--file=", commandArgs(trailingOnly = FALSE))][1]), ".."))
if (is.na(root)) root <- getwd()

data_path <- file.path(root, "data", "raw", "synthetic_resilience_systems.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_path, show_col_types = FALSE)

profiles <- systems %>%
  mutate(
    resilience_profile =
      0.24 * adaptive_capacity +
      0.20 * threshold_distance +
      0.18 * learning_capacity +
      0.14 * modularity +
      0.14 * redundancy -
      0.05 * exposure -
      0.05 * sensitivity,
    risk_pressure = 0.55 * exposure + 0.45 * sensitivity,
    viability_margin = resilience_profile + threshold_distance - risk_pressure,
    vulnerability_flag = case_when(
      viability_margin < 0.15 ~ "high threshold risk",
      viability_margin < 0.30 ~ "moderate threshold risk",
      TRUE ~ "lower threshold risk"
    )
  )

profiles_long <- profiles %>%
  select(
    system_type,
    adaptive_capacity,
    threshold_distance,
    learning_capacity,
    modularity,
    redundancy,
    exposure,
    sensitivity
  ) %>%
  pivot_longer(
    cols = -system_type,
    names_to = "dimension",
    values_to = "value"
  )

write_csv(profiles, file.path(out_tables, "resilience_profiles_r.csv"))
write_csv(profiles_long, file.path(out_tables, "resilience_profiles_long_r.csv"))

dimension_plot <- ggplot(
  profiles_long,
  aes(x = reorder(dimension, value), y = value, fill = system_type)
) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "Resilience Dimensions Across Synthetic System Types",
    x = "Dimension",
    y = "Value",
    fill = "System type"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  file.path(out_figures, "resilience_dimensions_r.png"),
  dimension_plot,
  width = 10,
  height = 6,
  dpi = 160
)

print(profiles %>% select(system_type, resilience_profile, risk_pressure, viability_margin, vulnerability_flag))
