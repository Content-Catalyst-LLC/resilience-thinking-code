# Predictive resilience profile workflow in R
#
# Run:
#   Rscript r/predictive_resilience_profiles.R
#
# Requires:
#   install.packages(c("tidyverse"))

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

input_path <- file.path(root, "data", "processed", "synthetic_resilience_training_data.csv")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

if (!file.exists(input_path)) {
  stop("Run python/predictive_resilience_model_standard.py first to create synthetic training data.")
}

df <- read_csv(input_path, show_col_types = FALSE)

profiles <- df %>%
  mutate(
    concept_balance =
      resilience_score - 0.5 * stability_score - 0.5 * robustness_score,
    risk_band = case_when(
      resilience_failure_risk == 1 & risk_pressure >= 0.60 ~ "high risk pressure failure",
      resilience_failure_risk == 1 ~ "predicted failure",
      TRUE ~ "viable in synthetic simulation"
    )
  )

summary <- profiles %>%
  group_by(system_type, risk_band) %>%
  summarize(
    observations = n(),
    mean_stability = mean(stability_score),
    mean_robustness = mean(robustness_score),
    mean_resilience = mean(resilience_score),
    mean_risk_pressure = mean(risk_pressure),
    .groups = "drop"
  )

write_csv(summary, file.path(out_tables, "r_predictive_profile_summary.csv"))

plot_data <- profiles %>%
  sample_n(min(800, nrow(.))) %>%
  select(system_type, stability_score, robustness_score, resilience_score, resilience_failure_risk) %>%
  pivot_longer(
    cols = c(stability_score, robustness_score, resilience_score),
    names_to = "concept",
    values_to = "score"
  )

p <- ggplot(plot_data, aes(x = concept, y = score, fill = factor(resilience_failure_risk))) +
  geom_boxplot(alpha = 0.75) +
  facet_wrap(~ system_type) +
  labs(
    title = "Synthetic Predictive Profiles by System Type",
    x = "Concept score",
    y = "Score",
    fill = "Failure risk"
  ) +
  theme_minimal(base_size = 11)

ggsave(
  filename = file.path(out_figures, "r_predictive_profile_boxplots.png"),
  plot = p,
  width = 11,
  height = 7,
  dpi = 160
)

print(summary)
