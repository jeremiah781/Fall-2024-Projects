// alu_extended.sv
// the reason this file is extended is I addded a few more operations, comments and expanded the project for extra credit (10/26/2024)
// This module represents an Arithmetic Logic Unit (ALU) for a 32-bit RISC-V processor
// It performs various arithmetic and logic operations based on the provided operation code
// started on 10/18/2024 and completed 10/29/2024
//TODO:
//FIXME:

module ALU (
    input  logic        clk,         // Clock signal (useful for synchronous operations)
    input  logic [31:0] operand_a,   // First operand (32 bits)
    input  logic [31:0] operand_b,   // Second operand (32 bits)
    input  logic [4:0]  alu_op,      // ALU operation code (5 bits to support more operations)
    output logic [31:0] result,      // Result of the ALU operation (32 bits)
    output logic        zero         // Zero flag (indicates if the result is zero)
);

    // Define the various operations our ALU can perform using an enumeration for clarity
    typedef enum logic [4:0] {
        ADD  = 5'b00000,  // Addition
        SUB  = 5'b00001,  // Subtraction
        AND  = 5'b00010,  // Bitwise AND
        OR   = 5'b00011,  // Bitwise OR
        XOR  = 5'b00100,  // Bitwise XOR
        SLT  = 5'b00101,  // Set on Less Than (signed comparison)
        SLL  = 5'b00110,  // Shift Left Logical
        SRL  = 5'b00111,  // Shift Right Logical
        SRA  = 5'b01000,  // Shift Right Arithmetic
        NOR  = 5'b01001,  // Bitwise NOR
        SGE  = 5'b01010   // Set on Greater or Equal (signed comparison)
        // this is expanded from my orignal ALU only had; ADD, SUB, AND, OR, XOR, AND SLT
    } alu_operation_t;

    // Always block to determine the ALU's result based on the operation code
    always_comb begin
        // Start by assuming the result is zero; this helps in avoiding latchesß
        result = 32'd0;

        // Use a case statement to handle different ALU operations.
        case (alu_op)
            ADD:  result = operand_a + operand_b; // Perform addition
            SUB:  result = operand_a - operand_b; // Perform subtraction
            AND:  result = operand_a & operand_b; // Perform bitwise AND
            OR:   result = operand_a | operand_b; // Perform bitwise OR
            XOR:  result = operand_a ^ operand_b; // Perform bitwise XOR
            SLT:  // Set result to 1 if operand_a is less than operand_b (signed), else 0
                result = ($signed(operand_a) < $signed(operand_b)) ? 32'd1 : 32'd0;
            SLL:  // Shift operand_a left by the number of positions specified in the lower 5 bits of operand_b
                result = operand_a << operand_b[4:0];
            SRL:  // Shift operand_a right logically by the number of positions specified in the lower 5 bits of operand_b
                result = operand_a >> operand_b[4:0];
            SRA:  // Shift operand_a right arithmetically (maintaining the sign) by the number of positions specified in the lower 5 bits of operand_b
                result = $signed(operand_a) >>> operand_b[4:0];
            NOR:  // Perform bitwise NOR on operand_a and operand_b
                result = ~(operand_a | operand_b);
            SGE:  // Set result to 1 if operand_a is greater than or equal to operand_b (signed), else 0
                result = ($signed(operand_a) >= $signed(operand_b)) ? 32'd1 : 32'd0;
            default: 
                result = 32'd0; // Default case sets result to zero
        endcase
    end

    // Assign the zero flag based on whether the result is zero
    assign zero = (result == 32'd0) ? 1'b1 : 1'b0;

endmodule

