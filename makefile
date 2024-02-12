# Define variables for file names
PYTHON_SCRIPT = GatorLibraryManagement.py
INPUT_FILE = inputs.txt
OUTPUT_FILE = inputs_output_file.txt

# Default target
all: run

# Target to run the Python script
run:
    @echo "Running Gator Library Management System..."
    python $(PYTHON_SCRIPT) $(INPUT_FILE)

# Target to clean up the output file
clean:
@echo "Cleaning up..."
rm -f $(OUTPUT_FILE)

.PHONY: all run clean