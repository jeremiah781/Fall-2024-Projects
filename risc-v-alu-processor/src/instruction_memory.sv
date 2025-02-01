// instruction_memory.sv
// This module represents the Instruction Memory in a RISC-V processor
// It stores a sequence of instructions that the processor will execute
// started on 10/02/2024 and completed 10/03/2024

module InstructionMemory (
    input  logic [31:0] address,      // Address input to fetch the instruction
    output logic [31:0] instruction,  // Output instruction fetched from memory
    output logic valid,               // Indicates instruction output is valid
    input  logic stall_in             // Allows stalling the pipeline if needed
);

    // Declare an array to simulate memory, with 256 words (1KB if each word is 4 bytes)
    logic [31:0] mem [0:255];

    // Initialize the instruction memory with some predefined instructions
    initial begin
        // Example instructions (these are RISC-V machine codes)
        // Instruction encoding should follow the RISC-V specification
        // Here, we manually insert a few instructions for demonstration

        // ADD x1, x0, x1 => x1 = x0 + x1 (effectively copies x1 to itself)
        mem[0] = 32'b00000000000100000000000010110011;

        // ADD x3, x0, x2 => x3 = x0 + x2 (copies x2 to x3)
        mem[1] = 32'b00000000001000000000000110110011;

        // You can add more instructions as needed for testing
        // For example, SUB, AND, OR, etc.
    end

    // Fetch the instruction based on the address input
    // Assuming word-aligned addresses, so we ignore the two least significant bits
    assign instruction = mem[address[31:2]];

    always_ff @(posedge clk) begin
        if (reset) begin
            valid <= 1'b0;
        end else if (!stall_in) begin
            valid <= 1'b1;
        end else begin
            valid <= 1'b0;
        end
    end

endmodule
