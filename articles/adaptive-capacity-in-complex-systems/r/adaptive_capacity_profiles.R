# Adaptive capacity profile workflow
#
# Run:
#   Rscript r/adaptive_capacity_profiles.R
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

profiles_path <- file.path(root, "data", "raw", "adaptive_capacity_profiles.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(profiles_path, show_col_types = FALSE)

profiles <- systems %>%
  mutate(
    adaptive_capacity =
      0.18 * learning +
      0.18 * flexibility +
      0.17 * diversity +
      0.17 * governance_capacity +
      0.14 * slack +
      0.16 * trust_legitimacy -
      0.12 * rigidity,
    adaptive_vulnerability =
      0.34 * exposure +
      0.24 * rigidity +
      0.16 * (1 - slack) +
      0.14 * (1 - trust_legitimacy) +
      0.12 * (1 - governance_capacity),
    response_space_baseline = adaptive_capacity - adaptive_vulnerability,
    diagnostic = case_when(
      adaptive_capacity >= 0.58 & adaptive_vulnerability < 0.55 ~
        "Stronger adaptive-capacity profile",
      adaptive_vulnerability >= 0.66 ~
        "High adaptive-vulnerability concern",
      rigidity >= 0.62 ~
        "Rigidity and lock-in concern",
      TRUE ~
        "Mixed adaptive-capacity profile requiring monitoring"
    )
  )

profiles_long <- profiles %>%
  select(
    system_type,
    learning,
    flexibility,
    diversity,
    governance_capacity,
    slack,
    trust_legitimacy,
    rigidity,
    exposure,
    adaptive_capacity,
    adaptive_vulnerability,
    response_space_baseline
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
    title = "Adaptive-Capacity Dimensions Across System Types",
    x = "Dimension",
    y = "Value",
    fill = "System Type"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_adaptive_capacity_dimensions.png"),
  plot = p,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(profiles, file.path(out_tables, "r_adaptive_capacity_profiles.csv"))
write_csv(profiles_long, file.path(out_tables, "r_adaptive_capacity_profiles_long.csv"))

print(profiles %>% select(system_type, adaptive_capacity, adaptive_vulnerability, response_space_baseline, diagnostic))
