// alu.sv
// started on 9/15/2024 and completed 9/19/2024
module ALU (
    input  logic        clk,
    input  logic [31:0] operand_a,
    input  logic [31:0] operand_b,
    input  logic [3:0]  alu_op,      // Operation code
    output logic [31:0] result,
    output logic        zero
);

    // ALU Operation Codes
    typedef enum logic [3:0] {
        ADD  = 4'b0000,
        SUB  = 4'b0001,
        AND  = 4'b0010,
        OR   = 4'b0011,
        XOR  = 4'b0100,
        SLT  = 4'b0101
    } alu_operation_t;

    always_comb begin
        case (alu_op)
            ADD:  result = operand_a + operand_b;
            SUB:  result = operand_a - operand_b;
            AND:  result = operand_a & operand_b;
            OR:   result = operand_a | operand_b;
            XOR:  result = operand_a ^ operand_b;
            SLT:  result = ($signed(operand_a) < $signed(operand_b)) ? 32'd1 : 32'd0;
            default: result = 32'd0;
        endcase
    end

    // Zero flag
    assign zero = (result == 32'd0) ? 1'b1 : 1'b0;

endmodule
