# Landscape resilience and disturbance-regime profile workflow
#
# Run:
#   Rscript r/landscape_resilience_profiles.R
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

profiles_path <- file.path(root, "data", "raw", "landscape_resilience_profiles.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

landscapes <- read_csv(profiles_path, show_col_types = FALSE)

profiles <- landscapes %>%
  mutate(
    landscape_resilience_profile =
      0.17 * spatial_heterogeneity +
      0.15 * viable_connectivity +
      0.17 * refugia_capacity +
      0.17 * ecological_memory +
      0.14 * governance_capacity -
      0.11 * disturbance_pressure -
      0.06 * fragmentation -
      0.06 * social_vulnerability,
    disturbance_risk_index =
      0.28 * disturbance_pressure +
      0.20 * fragmentation +
      0.18 * social_vulnerability +
      0.14 * (1 - refugia_capacity) +
      0.10 * (1 - ecological_memory) +
      0.10 * (1 - governance_capacity),
    diagnostic = case_when(
      landscape_resilience_profile >= 0.55 & disturbance_risk_index < 0.58 ~
        "Stronger landscape-resilience profile",
      disturbance_risk_index >= 0.68 ~
        "High disturbance-regime risk",
      refugia_capacity < 0.50 | ecological_memory < 0.50 ~
        "Refugia or ecological-memory concern",
      TRUE ~
        "Mixed landscape-resilience profile requiring monitoring"
    )
  )

profiles_long <- profiles %>%
  select(
    landscape_type,
    spatial_heterogeneity,
    viable_connectivity,
    refugia_capacity,
    ecological_memory,
    disturbance_pressure,
    fragmentation,
    governance_capacity,
    social_vulnerability,
    landscape_resilience_profile,
    disturbance_risk_index
  ) %>%
  pivot_longer(
    cols = -landscape_type,
    names_to = "dimension",
    values_to = "value"
  )

p <- ggplot(
  profiles_long,
  aes(x = dimension, y = value, fill = landscape_type)
) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "Landscape Resilience and Disturbance-Regime Dimensions",
    x = "Dimension",
    y = "Value",
    fill = "Landscape Type"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_landscape_resilience_dimensions.png"),
  plot = p,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(profiles, file.path(out_tables, "r_landscape_resilience_profiles.csv"))
write_csv(profiles_long, file.path(out_tables, "r_landscape_resilience_profiles_long.csv"))

print(profiles %>% select(landscape_type, landscape_resilience_profile, disturbance_risk_index, diagnostic))
