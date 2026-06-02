# Social-ecological systems profile workflow
#
# Run:
#   Rscript r/social_ecological_system_profiles.R
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

profiles_path <- file.path(root, "data", "raw", "social_ecological_system_profiles.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ses_systems <- read_csv(profiles_path, show_col_types = FALSE)

profiles <- ses_systems %>%
  mutate(
    ses_resilience_profile =
      0.18 * ecological_condition +
      0.16 * governance_quality +
      0.12 * livelihood_diversity +
      0.12 * infrastructure_support +
      0.13 * knowledge_integration +
      0.11 * social_trust +
      0.10 * adaptive_capacity -
      0.09 * market_pressure -
      0.07 * climate_exposure -
      0.02 * resource_dependency,
    coupled_vulnerability =
      0.26 * market_pressure +
      0.25 * climate_exposure +
      0.18 * resource_dependency +
      0.15 * (1 - governance_quality) +
      0.10 * (1 - livelihood_diversity) +
      0.06 * (1 - social_trust),
    diagnostic = case_when(
      ses_resilience_profile >= 0.52 & coupled_vulnerability < 0.55 ~
        "Stronger SES resilience profile",
      coupled_vulnerability >= 0.66 ~
        "High coupled vulnerability",
      governance_quality < 0.58 ~
        "Governance capacity concern",
      TRUE ~
        "Mixed SES resilience profile"
    )
  )

profiles_long <- profiles %>%
  select(
    system_type,
    ecological_condition,
    governance_quality,
    livelihood_diversity,
    infrastructure_support,
    knowledge_integration,
    social_trust,
    market_pressure,
    climate_exposure,
    ses_resilience_profile,
    coupled_vulnerability
  ) %>%
  pivot_longer(
    cols = -system_type,
    names_to = "dimension",
    values_to = "value"
  )

p <- ggplot(
  profiles_long,
  aes(x = dimension, y = value, fill = system_type)
) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "Social-Ecological System Dimensions",
    x = "Dimension",
    y = "Value",
    fill = "System Type"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_social_ecological_system_dimensions.png"),
  plot = p,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(profiles, file.path(out_tables, "r_social_ecological_system_profiles.csv"))
write_csv(profiles_long, file.path(out_tables, "r_social_ecological_system_profiles_long.csv"))

print(profiles %>% select(system_type, ses_resilience_profile, coupled_vulnerability, diagnostic))
