`timescale 1ns/1ps

module FloatingPointUnit #(
    parameter DATA_WIDTH = 32
)(
    input  logic [DATA_WIDTH-1:0] a,          // Changed from in_a
    input  logic [DATA_WIDTH-1:0] b,          // Changed from in_b
    input  logic [1:0]            operation,  // Must be 2 bits
    output logic [DATA_WIDTH-1:0] fp_result,  // Changed from result
    output logic                  fp_overflow // Changed from overflow
);
    assign fp_result = 32'b0;
    assign fp_overflow = 1'b0;
endmodule