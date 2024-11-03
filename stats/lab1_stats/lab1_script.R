# lab1_script.R
# Author: Jeremiah Ddumba
# Date: 09/20/2023
# Description: Analysis and visualization for Lab 1 of Stats class

# ------------------------------
# Load Necessary Libraries
# ------------------------------
# These libraries help in reading data and creating visualizations
library(readxl)   # For reading Excel files
library(ggplot2)  # For advanced plotting
library(lubridate) # For date manipulation

# ------------------------------
# Set Working Directory
# ------------------------------
# Modify the path below to the location where your Lab1_Stats folder is stored.
# Example for Windows: "C:/Users/YourName/Documents/Fall-2024-Projects/Lab1_Stats"
# Example for macOS/Linux: "/Users/YourName/Documents/Fall-2024-Projects/Lab1_Stats"
setwd("path/to/your/Fall-2024-Projects/lab1_stats")

# ------------------------------
# Section 1: Exploring the Iris Dataset
# ------------------------------

# Load the Iris dataset from Iris.xls
iris_data <- read_excel("data/iris.xls")

# View the first few rows to understand the data structure
head(iris_data)

# Calculate mean and standard deviation for each numerical variable
# This helps us understand the central tendency and variability of the measurements
iris_means <- sapply(iris_data[, 2:5], mean)
iris_sds <- sapply(iris_data[, 2:5], sd)

# Print the calculated means and standard deviations
print("Means of Iris variables:")
print(iris_means)
print("Standard deviations of Iris variables:")
print(iris_sds)

# Create a histogram for Sepal Length using ggplot2 for better aesthetics
ggplot(iris_data, aes(x = Sepal_length)) +
  geom_histogram(binwidth = 0.5, fill = "lightblue", color = "black") +
  theme_minimal() +
  labs(title = "Histogram of Sepal Length",
       x = "Sepal Length (cm)",
       y = "Frequency")

# Save the histogram to the Graphs folder
ggsave("Graphs/Histogram_SepalLength.png")

# ------------------------------
# Section 2: Bar Chart for Spearhead Data
# ------------------------------

# Load Spearhead data from Spearhead.xlsx
spearhead_data <- read_excel("data/spearhead.xlsx")

# View the Spearhead data to confirm it's loaded correctly
print(spearhead_data)

# Create a bar chart showing the number of spearheads found in different rivers using ggplot2
ggplot(spearhead_data, aes(x = River, y = `No. of spearheads`, fill = River)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(title = "Number of Spearheads Found in Different Rivers",
       x = "River",
       y = "Number of Spearheads") +
  theme(legend.position = "none")  # Remove legend as it's redundant

# Save the bar chart to the Graphs folder
ggsave("Graphs/BarChart_Spearheads.png")

# ------------------------------
# Section 3: Pie Chart for Ice Cream Data
# ------------------------------

# Load Ice Cream data from IceCream.xlsx
icecream_data <- read_excel("data/icecream.xlsx")

# View the Ice Cream data to confirm it's loaded correctly
print(icecream_data)

# Calculate percentages for each flavor
icecream_percent <- round(100 * icecream_data$`Number of kids` / sum(icecream_data$`Number of kids`), 1)

# Create labels combining flavor names and their percentages
labels <- paste(icecream_data$Flavor, icecream_percent, "%", sep=" ")

# Assign colors to each slice for better visualization
colors <- c("brown", "yellow", "pink", "lightblue", "grey")

# Create the pie chart using ggplot2
ggplot(icecream_data, aes(x = "", y = `Number of kids`, fill = Flavor)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y", start = 0) +
  theme_void() +  # Removes background, grid, and numeric labels
  labs(title = "Distribution of Ice Cream Flavors Among Children") +
  geom_text(aes(label = labels), position = position_stack(vjust = 0.5)) +
  scale_fill_manual(values = colors)

# Save the pie chart to the Graphs folder
ggsave("Graphs/PieChart_IceCreamDistribution.png")

# ------------------------------
# Section 4: Time Series Plot for US Gas Usage
# ------------------------------

# Load US gas usage data from usgas.xlsx
usgas_data <- read_excel("data/usgas.xlsx")

# View the US Gas Usage data to confirm it's loaded correctly
print(usgas_data)

# Convert the Date column to Date type for accurate plotting
usgas_data$Date <- as.Date(usgas_data$Date, format = "%Y-%m-%d")

# Create a time series plot using ggplot2
ggplot(usgas_data, aes(x = Date, y = Y)) +
  geom_line(color = "blue") +
  theme_minimal() +
  labs(title = "US Monthly Gas Usage (2001-2021)",
       x = "Date",
       y = "Gas Usage (Billions of Cubic Feet)")

# Save the time series plot to the Graphs folder
ggsave("Graphs/TimeSeries_USGasUsage.png")
