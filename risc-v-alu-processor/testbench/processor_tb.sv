// processor_tb.sv
// Enhanced Testbench for the Processor Module, Covering Pipelined Operations, Branching, Memory Access, and Interrupt Handling
// Developed on: 11/05/2024
// Updated 12/4/ - 12/5 for extra credit

`timescale 1ns/1ps

module Processor_tb;

    // Testbench Signals
    logic clk;
    logic reset;
    logic interrupt;

    // Instantiate the Processor
    Processor uut (
        .clk(clk),
        .reset(reset),
        .interrupt(interrupt)
    );

    // Clock Generation: 100MHz Clock
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // Toggle clock every 5 ns
    end

    // Initialize VCD for Waveform Viewing
    initial begin
        $dumpfile("processor_tb.vcd");
        $dumpvars(0, Processor_tb);
    end

    // Main Testing Procedure
    initial begin
        // Initialize Inputs
        reset = 1;
        interrupt = 0;

        // Apply Reset
        #10;
        reset = 0;

        // Wait for the processor to initialize
        #10;

        // Load Instructions into Instruction Memory (Assuming InstructionMemory is preloaded or accessible)
        // For simulation purposes, you can modify the InstructionMemory module to accept program data

        // Example Instruction Sequence:
        // 1. ADD x1, x2, x3      // x1 = x2 + x3
        // 2. SUB x4, x1, x5      // x4 = x1 - x5
        // 3. BEQ x4, x0, label   // if (x4 == 0) branch to label
        // 4. JAL x0, jump_addr    // Jump to jump_addr
        // 5. LW x6, 0(x7)         // Load word from memory address in x7 to x6
        // 6. SW x6, 4(x7)         // Store word from x6 to memory address (x7 + 4)
        // 7. JALR x0, x1, 0       // Jump to address in x1

        // For simplicity, assume InstructionMemory is preloaded with these instructions

        // Monitor Registers
        initial begin
            // Monitor specific registers to verify correct execution
            $monitor("Time: %0t | PC: %0d | x1: %0d | x4: %0d | x6: %0d",
                     $time,
                     uut.PC,
                     uut.regfile.registers[1],
                     uut.regfile.registers[4],
                     uut.regfile.registers[6]);
        end

        // Inject Interrupt after some cycles
        initial begin
            #100;
            interrupt = 1;
            #10;
            interrupt = 0;
        end

        // Run the simulation for a sufficient duration
        #200;
        $display("Simulation Completed.");
        $finish;
    end

endmodule