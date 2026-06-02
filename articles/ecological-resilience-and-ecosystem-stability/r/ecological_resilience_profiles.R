suppressPackageStartupMessages({
  library(tidyverse)
})

root <- normalizePath(file.path(dirname(sub("^--file=", "", commandArgs(trailingOnly = FALSE)[grepl("^--file=", commandArgs(trailingOnly = FALSE))][1])), ".."))
if (is.na(root)) root <- getwd()

profiles_path <- file.path(root, "data", "raw", "ecosystem_resilience_profiles.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ecosystems <- read_csv(profiles_path, show_col_types = FALSE)

profiles <- ecosystems %>%
  mutate(
    stability_score = short_run_stability,
    ecological_resilience_profile =
      0.11 * short_run_stability +
      0.13 * biodiversity +
      0.13 * functional_diversity +
      0.13 * response_diversity +
      0.16 * threshold_distance +
      0.14 * basin_width +
      0.12 * regenerative_capacity +
      0.10 * ecological_memory +
      0.08 * connectivity -
      0.06 * disturbance_exposure -
      0.06 * slow_variable_pressure,
    threshold_risk_index = pmax(
      0,
      pmin(
        1,
        0.30 * (1 - threshold_distance) +
          0.25 * (1 - basin_width) +
          0.20 * disturbance_exposure +
          0.18 * slow_variable_pressure -
          0.15 * regenerative_capacity -
          0.12 * response_diversity
      )
    )
  )

write_csv(profiles, file.path(out_tables, "r_ecosystem_resilience_profiles.csv"))
print(profiles %>% select(ecosystem_type, stability_score, ecological_resilience_profile, threshold_risk_index))
