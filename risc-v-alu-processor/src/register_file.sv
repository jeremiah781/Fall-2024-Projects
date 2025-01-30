`timescale 1ns/1ps

// register_file.sv
// This module represents the Register File in a RISC-V processor
// It contains 32 general-purpose registers, each 32 bits wide
// started on 9/10/2024 and completed 9/17/2024

module RegisterFile (
    input  logic        clk,         // Clock signal for synchronous writes
    input  logic        reset,       // Reset signal to initialize registers
    input  logic [4:0]  read_reg1,   // Address of the first register to read
    input  logic [4:0]  read_reg2,   // Address of the second register to read
    input  logic [4:0]  write_reg,   // Address of the register to write to
    input  logic [31:0] write_data,  // Data to write into the register
    input  logic        reg_write,   // Control signal to enable writing
    output logic [31:0] read_data1,  // Data read from the first register
    output logic [31:0] read_data2   // Data read from the second register
);

    parameter REG_COUNT   = 32;
    parameter ASYNC_READ  = 0;
    parameter CHECK_WB    = 0;

    // Simple 32x32 register array
    logic [31:0] registers [0:31];

    // Handle synchronous write operations
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            // Initialize all registers to 0
            for (int i = 0; i < 32; i++) begin
                registers[i] <= 32'd0;
            end
        end else if (reg_write && write_reg != 5'd0) begin
            registers[write_reg] <= write_data;
        end
    end

    // Combinational read
    assign read_data1 = (read_reg1 == 5'd0) ? 32'd0 : registers[read_reg1];
    assign read_data2 = (read_reg2 == 5'd0) ? 32'd0 : registers[read_reg2];

endmodule
