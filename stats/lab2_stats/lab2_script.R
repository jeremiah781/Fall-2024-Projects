# lab2_script.R
# Author: Jeremiah Ddumba
# Date: 11/05/2023
# Description: Stats Analysis and Regression for Lab 2 of Stats class 200 using R

# ------------------------------
# Load Necessary Libraries
# ------------------------------
# These libraries help in reading data, performing statistical calculations, and creating visualizations
library(readxl)     # For reading Excel files
library(ggplot2)    # For advanced plotting
library(dplyr)      # For data manipulation
library(tidyr)      # For data tidying
library(ggpubr)     # For enhanced ggplot2 visualizations

# ------------------------------
# Set Working Directory
# ------------------------------
# Modify the path below to the location where your lab2_stats folder is stored
# Example for Windows: "C:/Users/YourName/Documents/stats/lab2_stats"
# Example for macOS/Linux: "/Users/YourName/Documents/stats/lab2_stats"
setwd("path/to/your/stats/lab2_stats")

# ------------------------------
# Load the Iris Dataset
# ------------------------------

# Read the Iris dataset from iris.xls
iris_data <- read_excel("data/iris.xls")

# View the first few rows to confirm it's loaded correctly
head(iris_data)

# ------------------------------
# Section 1: Measures of Central Tendency
# ------------------------------

# Calculate means for Sepal Length, Sepal Width, Petal Length, and Petal Width
# Using the mean() function
mean_sepal_length <- mean(iris_data$Sepal_Length)
mean_sepal_width  <- mean(iris_data$Sepal_Width)
mean_petal_length <- mean(iris_data$Petal_Length)
mean_petal_width  <- mean(iris_data$Petal_Width)

# Print the means
print("Mean Values:")
print(paste("Sepal Length:", round(mean_sepal_length, 2)))
print(paste("Sepal Width:", round(mean_sepal_width, 2)))
print(paste("Petal Length:", round(mean_petal_length, 2)))
print(paste("Petal Width:", round(mean_petal_width, 2)))

# Compare means by species
# Using dplyr to group data by Species_Name and calculate means
mean_by_species <- iris_data %>%
  group_by(Species_Name) %>%
  summarise(
    Mean_Sepal_Length = mean(Sepal_Length),
    Mean_Sepal_Width  = mean(Sepal_Width),
    Mean_Petal_Length = mean(Petal_Length),
    Mean_Petal_Width  = mean(Petal_Width)
  )

# Print the means by species
print("Mean Values by Species:")
print(mean_by_species)

# ------------------------------
# Section 2: Measures of Spread
# ------------------------------

# Calculate standard deviations for each variable
sd_sepal_length <- sd(iris_data$Sepal_Length)
sd_sepal_width  <- sd(iris_data$Sepal_Width)
sd_petal_length <- sd(iris_data$Petal_Length)
sd_petal_width  <- sd(iris_data$Petal_Width)

# Print the standard deviations
print("Standard Deviations:")
print(paste("Sepal Length:", round(sd_sepal_length, 2)))
print(paste("Sepal Width:", round(sd_sepal_width, 2)))
print(paste("Petal Length:", round(sd_petal_length, 2)))
print(paste("Petal Width:", round(sd_petal_width, 2)))

# Compare standard deviations by species
sd_by_species <- iris_data %>%
  group_by(Species_Name) %>%
  summarise(
    SD_Sepal_Length = sd(Sepal_Length),
    SD_Sepal_Width  = sd(Sepal_Width),
    SD_Petal_Length = sd(Petal_Length),
    SD_Petal_Width  = sd(Petal_Width)
  )

# Print the standard deviations by species
print("Standard Deviations by Species:")
print(sd_by_species)

# Calculate the coefficient of variation (CV) for each variable
# CV = (Standard Deviation / Mean) * 100
cv_sepal_length <- (sd_sepal_length / mean_sepal_length) * 100
cv_sepal_width  <- (sd_sepal_width / mean_sepal_width) * 100
cv_petal_length <- (sd_petal_length / mean_petal_length) * 100
cv_petal_width  <- (sd_petal_width / mean_petal_width) * 100

# Print the coefficients of variation
print("Coefficient of Variation (%):")
print(paste("Sepal Length:", round(cv_sepal_length, 2)))
print(paste("Sepal Width:", round(cv_sepal_width, 2)))
print(paste("Petal Length:", round(cv_petal_length, 2)))
print(paste("Petal Width:", round(cv_petal_width, 2)))

# ------------------------------
# Section 3: 5-Number Summary and Boxplots
# ------------------------------

# Overall summary using summary()
overall_summary <- summary(iris_data[, c("Sepal_Length", "Sepal_Width", "Petal_Length", "Petal_Width")])
print("Overall 5-Number Summary:")
print(overall_summary)

# Species-specific summaries
species_summary <- iris_data %>%
  group_by(Species_Name) %>%
  summarise(
    Min_Sepal_Length = min(Sepal_Length),
    Q1_Sepal_Length  = quantile(Sepal_Length, 0.25),
    Median_Sepal_Length = median(Sepal_Length),
    Mean_Sepal_Length = mean(Sepal_Length),
    Q3_Sepal_Length  = quantile(Sepal_Length, 0.75),
    Max_Sepal_Length = max(Sepal_Length),
    
    Min_Sepal_Width = min(Sepal_Width),
    Q1_Sepal_Width  = quantile(Sepal_Width, 0.25),
    Median_Sepal_Width = median(Sepal_Width),
    Mean_Sepal_Width = mean(Sepal_Width),
    Q3_Sepal_Width  = quantile(Sepal_Width, 0.75),
    Max_Sepal_Width = max(Sepal_Width),
    
    Min_Petal_Length = min(Petal_Length),
    Q1_Petal_Length  = quantile(Petal_Length, 0.25),
    Median_Petal_Length = median(Petal_Length),
    Mean_Petal_Length = mean(Petal_Length),
    Q3_Petal_Length  = quantile(Petal_Length, 0.75),
    Max_Petal_Length = max(Petal_Length),
    
    Min_Petal_Width = min(Petal_Width),
    Q1_Petal_Width  = quantile(Petal_Width, 0.25),
    Median_Petal_Width = median(Petal_Width),
    Mean_Petal_Width = mean(Petal_Width),
    Q3_Petal_Width  = quantile(Petal_Width, 0.75),
    Max_Petal_Width = max(Petal_Width)
  )

print("5-Number Summary by Species:")
print(species_summary)

# Create boxplots for each variable by species

# Sepal Length Boxplot
boxplot_sepal_length <- ggplot(iris_data, aes(x = Species_Name, y = Sepal_Length, fill = Species_Name)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Boxplot of Sepal Length by Species",
       x = "Species",
       y = "Sepal Length (cm)") +
  theme(legend.position = "none")

# Save the boxplot
ggsave("graphs/boxplot_sepal_length.png", plot = boxplot_sepal_length)

# Sepal Width Boxplot
boxplot_sepal_width <- ggplot(iris_data, aes(x = Species_Name, y = Sepal_Width, fill = Species_Name)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Boxplot of Sepal Width by Species",
       x = "Species",
       y = "Sepal Width (cm)") +
  theme(legend.position = "none")

# Save the boxplot
ggsave("graphs/boxplot_sepal_width.png", plot = boxplot_sepal_width)

# Petal Length Boxplot
boxplot_petal_length <- ggplot(iris_data, aes(x = Species_Name, y = Petal_Length, fill = Species_Name)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Boxplot of Petal Length by Species",
       x = "Species",
       y = "Petal Length (cm)") +
  theme(legend.position = "none")

# Save the boxplot
ggsave("graphs/boxplot_petal_length.png", plot = boxplot_petal_length)

# Petal Width Boxplot
boxplot_petal_width <- ggplot(iris_data, aes(x = Species_Name, y = Petal_Width, fill = Species_Name)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Boxplot of Petal Width by Species",
       x = "Species",
       y = "Petal Width (cm)") +
  theme(legend.position = "none")

# Save the boxplot
ggsave("graphs/boxplot_petal_width.png", plot = boxplot_petal_width)
