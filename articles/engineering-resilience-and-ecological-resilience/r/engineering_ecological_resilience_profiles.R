# Engineering and ecological resilience profiles
#
# Run:
#   Rscript r/engineering_ecological_resilience_profiles.R
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

systems_path <- file.path(root, "data", "raw", "engineering_ecological_resilience_systems.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(systems_path, show_col_types = FALSE)

profiles <- systems %>%
  mutate(
    engineering_resilience =
      0.28 * return_speed +
      0.24 * reliability +
      0.18 * repair_capacity +
      0.15 * backup_capacity +
      0.15 * service_continuity,
    ecological_resilience =
      0.20 * threshold_distance +
      0.18 * basin_width +
      0.18 * adaptive_capacity +
      0.15 * functional_diversity +
      0.13 * redundancy +
      0.10 * modularity -
      0.08 * disturbance_exposure -
      0.08 * regime_shift_sensitivity,
    resilience_gap = ecological_resilience - engineering_resilience,
    interpretation = case_when(
      resilience_gap < -0.18 ~ "Strong engineering return but weaker threshold persistence",
      resilience_gap > 0.18 ~ "Stronger ecological adaptive capacity than operational return",
      TRUE ~ "More balanced engineering/ecological profile"
    )
  )

profiles_long <- profiles %>%
  select(system_type, engineering_resilience, ecological_resilience) %>%
  pivot_longer(
    cols = c(engineering_resilience, ecological_resilience),
    names_to = "resilience_type",
    values_to = "score"
  )

p <- ggplot(
  profiles_long,
  aes(x = reorder(system_type, score), y = score, fill = resilience_type)
) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "Engineering vs Ecological Resilience Profiles",
    x = "System type",
    y = "Score",
    fill = "Resilience type"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  filename = file.path(out_figures, "r_engineering_ecological_profiles.png"),
  plot = p,
  width = 10,
  height = 6,
  dpi = 160
)

write_csv(profiles, file.path(out_tables, "r_engineering_ecological_profiles.csv"))

print(profiles %>% select(system_type, engineering_resilience, ecological_resilience, resilience_gap, interpretation))
