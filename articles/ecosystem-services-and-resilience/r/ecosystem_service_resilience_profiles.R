# Ecosystem-service resilience profile workflow
#
# Run:
#   Rscript r/ecosystem_service_resilience_profiles.R
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

profiles_path <- file.path(root, "data", "raw", "ecosystem_service_profiles.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

services <- read_csv(profiles_path, show_col_types = FALSE)

profiles <- services %>%
  mutate(
    service_resilience_profile =
      0.10 * current_service_flow +
      0.17 * ecological_condition +
      0.15 * functional_diversity +
      0.14 * functional_redundancy +
      0.15 * threshold_distance +
      0.12 * governance_capacity +
      0.09 * access_equity +
      0.12 * ecological_memory -
      0.12 * disturbance_exposure,
    service_resilience_gap = service_resilience_profile - current_service_flow,
    service_threshold_risk_index = pmax(
      0,
      pmin(
        1,
        0.26 * (1 - threshold_distance) +
          0.22 * disturbance_exposure +
          0.16 * (1 - functional_redundancy) +
          0.14 * (1 - functional_diversity) +
          0.12 * (1 - governance_capacity) +
          0.10 * (1 - ecological_memory) -
          0.08 * access_equity
      )
    ),
    diagnostic = case_when(
      current_service_flow >= 0.70 & service_resilience_profile < 0.55 ~
        "High current flow but weak resilience profile",
      service_resilience_profile >= 0.60 & threshold_distance >= 0.55 ~
        "Stronger service-resilience profile",
      access_equity < 0.50 ~
        "Equity and access concern",
      TRUE ~
        "Mixed service-resilience profile requiring monitoring"
    )
  )

profiles_long <- profiles %>%
  select(
    service,
    current_service_flow,
    ecological_condition,
    functional_diversity,
    functional_redundancy,
    threshold_distance,
    governance_capacity,
    disturbance_exposure,
    access_equity,
    ecological_memory,
    service_resilience_profile,
    service_threshold_risk_index
  ) %>%
  pivot_longer(
    cols = -service,
    names_to = "dimension",
    values_to = "value"
  )

p <- ggplot(
  profiles_long,
  aes(x = dimension, y = value, fill = service)
) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "Ecosystem-Service Resilience Dimensions",
    x = "Dimension",
    y = "Value",
    fill = "Service"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_ecosystem_service_resilience_dimensions.png"),
  plot = p,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(profiles, file.path(out_tables, "r_ecosystem_service_resilience_profiles.csv"))
write_csv(profiles_long, file.path(out_tables, "r_ecosystem_service_resilience_profiles_long.csv"))

print(profiles %>% select(service, current_service_flow, service_resilience_profile, service_threshold_risk_index, diagnostic))
