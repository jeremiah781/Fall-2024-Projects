# Makefile

# Variables
DATA_DIR = data/imdb
DATASET = imdb
SETUP_SCRIPT = scripts/setup.py
LOAD_SCRIPT = scripts/load_dataset.py

# Targets
all: setup load

setup: $(DATA_DIR)/ready

$(DATA_DIR)/ready: $(DATA_DIR)
	@echo "Downloading and saving the $(DATASET) dataset..."
	python $(SETUP_SCRIPT)
	@touch $(DATA_DIR)/ready

$(DATA_DIR):
	@mkdir -p $(DATA_DIR)

load: $(DATA_DIR)/ready
	@echo "Loading and inspecting the dataset..."
	python $(LOAD_SCRIPT)

clean:
	@echo "Cleaning up data directory..."
	rm -rf $(DATA_DIR)
	@echo "Cleaned."

.PHONY: all setup load clean
