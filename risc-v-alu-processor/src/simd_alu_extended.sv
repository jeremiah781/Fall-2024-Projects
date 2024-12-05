// simd_alu_extended.sv
// SIMD-Enabled ALU Module
// Made on 12/3 - 12/4
module SIMD_ALU_Extended #(
    parameter DATA_WIDTH = 32,
    parameter OP_WIDTH = 5,
    parameter NUM_OPS = 32,
    parameter SIMD_WIDTH = 4 // Number of parallel ALUs
) (
    input  logic                   clk,          // Clock signal
    input  logic [SIMD_WIDTH*DATA_WIDTH-1:0] operand_a, // SIMD First operands
    input  logic [SIMD_WIDTH*DATA_WIDTH-1:0] operand_b, // SIMD Second operands
    input  logic [SIMD_WIDTH*OP_WIDTH-1:0]    alu_op,    // SIMD ALU operation codes
    input  logic                   en,           // Enable signal
    output logic [SIMD_WIDTH*DATA_WIDTH-1:0]  result,    // SIMD ALU results
    output logic [SIMD_WIDTH-1:0]             zero,      // SIMD Zero flags
    output logic [SIMD_WIDTH-1:0]             overflow,  // SIMD Overflow flags
    output logic [SIMD_WIDTH-1:0]             carry_out, // SIMD Carry-out flags
    output logic [SIMD_WIDTH-1:0]             negative,  // SIMD Negative flags
    output logic [SIMD_WIDTH*DATA_WIDTH-1:0]  fp_result, // SIMD Floating-Point results
    output logic [SIMD_WIDTH-1:0]             fp_overflow // SIMD Floating-Point overflow flags
);
    genvar i;
    generate
        for (i = 0; i < SIMD_WIDTH; i++) begin : simd_alus
            ALU_Extended #(
                .DATA_WIDTH(DATA_WIDTH),
                .OP_WIDTH(OP_WIDTH)
            ) alu_inst (
                .clk(clk),
                .operand_a(operand_a[i*DATA_WIDTH +: DATA_WIDTH]),
                .operand_b(operand_b[i*DATA_WIDTH +: DATA_WIDTH]),
                .alu_op(alu_op[i*OP_WIDTH +: OP_WIDTH]),
                .en(en),
                .result(result[i*DATA_WIDTH +: DATA_WIDTH]),
                .zero(zero[i]),
                .overflow(overflow[i]),
                .carry_out(carry_out[i]),
                .negative(negative[i]),
                .fp_result(fp_result[i*DATA_WIDTH +: DATA_WIDTH]),
                .fp_overflow(fp_overflow[i])
            );
        end
    endgenerate
endmodule