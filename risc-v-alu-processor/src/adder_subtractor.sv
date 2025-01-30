`timescale 1ns/1ps

module AdderSubtractor #(
    parameter DATA_WIDTH = 32
)(
    input  logic [DATA_WIDTH-1:0] in_a,
    input  logic [DATA_WIDTH-1:0] in_b,
    input  logic                  op_sub,
    output logic [DATA_WIDTH-1:0] result,
    output logic                  carry_out,
    output logic                  overflow
);
    // Minimal placeholder
    assign result    = in_a + (op_sub ? ~in_b + 1'b1 : in_b);
    assign carry_out = 1'b0;
    assign overflow  = 1'b0;
endmodule