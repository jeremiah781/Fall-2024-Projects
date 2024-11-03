// processor_tb.sv
// Enhanced testbench for the Processor module, covering sequential operations and multiple register interactions
// started on 10/23/2024 and completed 10/29/2024

`timescale 1ns/1ps // Define the time unit and precision

module Processor_tb;

    // Testbench Signals
    logic clk;
    logic reset;

    // Instantiate the Processor
    Processor uut (
        .clk(clk),
        .reset(reset)
    );

    // Generate a clock signal that toggles every 5 ns (100MHz frequency)
    initial begin
        clk = 0; // Start with clock low
        forever #5 clk = ~clk; // Toggle clock every 5 ns
    end

    // Initialize VCD (Value Change Dump) for waveform viewing in GTKWave
    initial begin
        $dumpfile("processor_tb.vcd"); // Specify the VCD file name
        $dumpvars(0, Processor_tb);     // Dump all variables in the Processor_tb module
    end

    // Main testing procedure
    initial begin
        // Start with reset active
        reset = 1;

        // Hold reset for 10 ns to ensure all components initialize correctly
        #10;
        reset = 0; // Deactivate reset

        // Let the processor run for enough cycles to execute all instructions
        #200;

        // Indicate that the simulation is complete
        $display("Simulation Completed.");
        $finish; // End the simulation
    end

    // Monitor specific registers to verify correct execution
    // For example, monitor registers x1, x2, x3, x5, x7, x9, x11, x13, x15 to see the results of sequential instructions
    initial begin
        // The $monitor statement continuously prints the values whenever they change
        $monitor("Time: %0t | x1: %0d | x2: %0d | x3: %0d | x5: %0d | x7: %0d | x9: %0d | x11: %0d | x13: %0d | x15: %0d",
                 $time,
                 uut.regfile.registers[1],
                 uut.regfile.registers[2],
                 uut.regfile.registers[3],
                 uut.regfile.registers[5],
                 uut.regfile.registers[7],
                 uut.regfile.registers[9],
                 uut.regfile.registers[11],
                 uut.regfile.registers[13],
                 uut.regfile.registers[15]);
    end

endmodule
