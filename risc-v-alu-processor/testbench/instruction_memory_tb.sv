// instruction_memory_tb.sv
// Testbench for the Instruction Memory module
// started on 10/06/2024 and completed 10/09/2024

`timescale 1ns/1ps

module InstructionMemory_tb;

    // Testbench Signals
    logic [31:0] address;
    logic [31:0] instruction;

    // Instantiate the Instruction Memory
    InstructionMemory uut (
        .address(address),
        .instruction(instruction)
    );

    // VCD Dumping for GTKWave
    initial begin
        $dumpfile("instruction_memory_tb.vcd");
        $dumpvars(0, InstructionMemory_tb);
    end

    // Test Procedure
    initial begin
        // Initialize Inputs
        address = 32'd0;

        // Wait for a short period
        #10;

        // Read first instruction
        #10;
        address = 32'd0;
        #10;
        $display("Address: %0d, Instruction: %b", address, instruction);

        // Read second instruction
        #10;
        address = 32'd4;
        #10;
        $display("Address: %0d, Instruction: %b", address, instruction);

        // Read third instruction (should be undefined or default)
        #10;
        address = 32'd8;
        #10;
        $display("Address: %0d, Instruction: %b", address, instruction);

        // Random address tests
        repeat (5) begin
            address = $urandom_range(0, 32'h10);
            #10;
            $display("Random Address: %0d, Instruction: %b", address, instruction);
        end

        // End Simulation
        #10;
        $display("All Instruction Memory tests completed.");
        $finish;
    end

endmodule
