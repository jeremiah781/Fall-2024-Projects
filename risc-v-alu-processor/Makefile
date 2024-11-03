# Makefile
# Automates compilation, simulation, and waveform viewing for the RISC-V processor project
# started on 10/29/2024 and completed 11/02/2024

# ----- Tool Definitions -----
IVERILOG = iverilog    # Verilog/SystemVerilog compiler
VVP      = vvp         # Simulation engine
GTKWAVE  = gtkwave     # Waveform viewer

# ----- Source and Testbench Files -----
SRC = \
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

# ----- Compilation Targets -----
# Compile the ALU testbench
compile_alu:
	$(IVERILOG) -g2012 -o $(SIMV_ALU) $(SRC) $(TB_ALU)

# Compile the Processor testbench
compile_proc:
	$(IVERILOG) -g2012 -o $(SIMV_PROC) $(SRC) $(TB_PROC)

# ----- Simulation Targets -----
# Run the ALU simulation and generate VCD
simulate_alu: compile_alu
	$(VVP) $(SIMV_ALU) -vcd=$(VCD_ALU)

# Run the Processor simulation and generate VCD
simulate_proc: compile_proc
	$(VVP) $(SIMV_PROC) -vcd=$(VCD_PROC)

# ----- View Waveform Targets -----
# Open the ALU waveform in GTKWave
view_alu:
	$(GTKWAVE) $(VCD_ALU) &

# Open the Processor waveform in GTKWave
view_proc:
	$(GTKWAVE) $(VCD_PROC) &

# ----- Combined Simulation and View -----
# Simulate and view ALU testbench
simulate_view_alu: simulate_alu view_alu

# Simulate and view Processor testbench
simulate_view_proc: simulate_proc view_proc

# ----- Clean Up Target -----
# Remove generated simulation files
clean:
	rm -f $(SIMV_ALU) $(SIMV_PROC) $(VCD_ALU) $(VCD_PROC)

# ----- Phony Targets -----
.PHONY: all compile_alu compile_proc simulate_alu simulate_proc view_alu view_proc simulate_view_alu simulate_view_proc clean
