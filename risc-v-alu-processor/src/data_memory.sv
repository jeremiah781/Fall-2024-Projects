`timescale 1ns/1ps

module DataMemory (
    input  logic        clk,
    input  logic [31:0] address,
    input  logic [31:0] write_data,
    input  logic        mem_write,
    input  logic        mem_read,
    output logic [31:0] read_data
);
    // Minimal placeholder: read_data is set to 32'b0
    assign read_data = 32'b0;
endmodule