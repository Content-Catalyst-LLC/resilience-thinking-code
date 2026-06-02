# Functional diversity and redundancy profile workflow
#
# Run:
#   Rscript r/functional_diversity_redundancy_profiles.R
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

profiles_path <- file.path(root, "data", "raw", "ecological_function_profiles.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

functions <- read_csv(profiles_path, show_col_types = FALSE)

profiles <- functions %>%
  mutate(
    functional_resilience_profile =
      0.12 * species_richness +
      0.19 * functional_diversity +
      0.17 * functional_redundancy +
      0.20 * response_diversity +
      0.13 * connectivity +
      0.16 * ecological_memory -
      0.12 * disturbance_exposure,
    function_threshold_risk_index = pmax(
      0,
      pmin(
        1,
        0.24 * (1 - response_diversity) +
          0.22 * (1 - functional_redundancy) +
          0.18 * disturbance_exposure +
          0.14 * (1 - connectivity) +
          0.12 * (1 - ecological_memory) +
          0.10 * (1 - functional_diversity)
      )
    ),
    diagnostic = case_when(
      functional_resilience_profile >= 0.58 & response_diversity >= 0.55 ~
        "Stronger function-resilience profile",
      functional_redundancy < 0.50 | response_diversity < 0.50 ~
        "Redundancy or response-diversity concern",
      disturbance_exposure >= 0.70 ~
        "High disturbance exposure",
      TRUE ~
        "Mixed profile requiring monitoring"
    )
  )

profiles_long <- profiles %>%
  select(
    ecosystem_function,
    species_richness,
    functional_diversity,
    functional_redundancy,
    response_diversity,
    connectivity,
    ecological_memory,
    disturbance_exposure,
    functional_resilience_profile,
    function_threshold_risk_index
  ) %>%
  pivot_longer(
    cols = -ecosystem_function,
    names_to = "dimension",
    values_to = "value"
  )

p <- ggplot(
  profiles_long,
  aes(x = dimension, y = value, fill = ecosystem_function)
) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "Biodiversity Dimensions Supporting Ecological Function",
    x = "Dimension",
    y = "Value",
    fill = "Function"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_functional_diversity_redundancy_dimensions.png"),
  plot = p,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(profiles, file.path(out_tables, "r_functional_diversity_redundancy_profiles.csv"))
write_csv(profiles_long, file.path(out_tables, "r_functional_diversity_redundancy_long.csv"))

print(profiles %>% select(ecosystem_function, functional_resilience_profile, function_threshold_risk_index, diagnostic))
