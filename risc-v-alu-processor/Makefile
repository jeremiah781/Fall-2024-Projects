# Makefile
# Automates compilation, simulation, and waveform viewing for the RISC-V processor project
# started on 10/29/2024 and completed 11/02/2024; edited 11/15/2024

# ----- Tool Definitions -----
IVERILOG = iverilog    # Verilog/SystemVerilog compiler
VVP      = vvp         # Simulation engine
GTKWAVE  = gtkwave     # Waveform viewer

# Uncomment the line below to enable debug flags:
DEBUG_FLAGS = -g

# Optional coverage flags (if your tools support them)
COVERAGE_FLAGS = -fprofile-arcs -ftest-coverage

# ----- Source and Testbench Files -----
SRC = \
	src/hazard_detection_unit.sv \
	src/data_memory.sv \
	src/adder_subtractor.sv \
	src/logic_unit.sv \
	src/shift_unit.sv \
	src/floating_point_unit.sv \
	src/alu_extended.sv \
	src/alu_pipelined.sv \
	src/control_unit.sv \
	src/register_file.sv \
	src/instruction_memory.sv \
	src/processor.sv

TB_ALU = testbench/alu_extended_tb.sv
TB_PROC = testbench/processor_tb.sv

# ----- Output Files -----
SIMV_ALU = waveforms/alu_extended_tb.vvp
VCD_ALU = waveforms/alu_extended_tb.vcd

SIMV_PROC = waveforms/processor_tb.vvp
VCD_PROC = waveforms/processor_tb.vcd

# ----- Default Target -----
all: simulate_view_proc

# ----- Directory Preparation -----
prepare_dirs:
	mkdir -p waveforms

# ----- Compilation Targets -----
# Compile the ALU testbench
compile_alu: prepare_dirs
	$(IVERILOG) -g2012 -Wall -Werror -o $(SIMV_ALU) $(SRC) $(TB_ALU)

# Compile the Processor testbench
compile_proc: prepare_dirs
	$(IVERILOG) -g2012 -Wall -Werror -o $(SIMV_PROC) $(SRC) $(TB_PROC)

# ----- Simulation Targets -----
# Run the ALU simulation and generate VCD
simulate_alu: compile_alu
	$(VVP) $(SIMV_ALU) -vcd=$(VCD_ALU) || echo "ALU Simulation Failed"

# Run the Processor simulation and generate VCD
simulate_proc: compile_proc
	$(VVP) $(SIMV_PROC) -vcd=$(VCD_PROC) || echo "Processor Simulation Failed"

# ----- View Waveform Targets -----
# Open the ALU waveform in GTKWave
view_alu:
	@if [ -f $(VCD_ALU) ]; then \
		$(GTKWAVE) $(VCD_ALU) & \
	else \
		echo "VCD_ALU file not found. Please run simulate_alu first."; \
	fi

# Open the Processor waveform in GTKWave
view_proc:
	@if [ -f $(VCD_PROC) ]; then \
		$(GTKWAVE) $(VCD_PROC) & \
	else \
		echo "VCD_PROC file not found. Please run simulate_proc first."; \
	fi

# ----- Combined Simulation and View -----
# Simulate and view ALU testbench
simulate_view_alu: simulate_alu view_alu

# Simulate and view Processor testbench
simulate_view_proc: simulate_proc view_proc

# ----- Clean Up Target -----
# Remove generated simulation files and waveforms directory
clean:
	rm -f $(SIMV_ALU) $(SIMV_PROC) $(VCD_ALU) $(VCD_PROC)
	rm -rf waveforms/

# ----- Help Target -----
help:
	@echo "Available targets:"
	@echo "  all                - Build and simulate the default processor testbench"
	@echo "  compile_alu        - Compile ALU testbench"
	@echo "  compile_proc       - Compile Processor testbench"
	@echo "  simulate_alu       - Run ALU simulation"
	@echo "  simulate_proc      - Run Processor simulation"
	@echo "  view_alu           - View ALU VCD in GTKWave"
	@echo "  view_proc          - View Processor VCD in GTKWave"
	@echo "  coverage           - Example coverage target (tool-dependent)"
	@echo "  clean              - Remove generated files"
	@echo "Use 'make -jN' for parallel builds (N is number of threads)."

# ----- Coverage Target -----
coverage:
	# Example coverage workflow (adjust for your coverage tools)
	$(IVERILOG) $(DEBUG_FLAGS) $(COVERAGE_FLAGS) -o coverage.vvp $(SRC) $(TB_ALU)
	$(VVP) coverage.vvp
	@echo "Coverage data collected (tool-dependent)."

# ----- Phony Targets -----
.PHONY: all compile_alu compile_proc simulate_alu simulate_proc view_alu view_proc simulate_view_alu simulate_view_proc clean prepare_dirs help coverage