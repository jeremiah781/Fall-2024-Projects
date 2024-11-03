// control_unit.sv
// This module generates control signals based on the instruction's opcode
// It determines how the ALU should operate for each instruction
// started on 9/27/2024 and completed 9/30/2024

module ControlUnit (
    input  logic [6:0] opcode,       // Opcode field from the instruction
    output logic       reg_write,    // Control signal to enable writing to the register file
    output logic [4:0] alu_op        // ALU operation code to control the ALU's behavior
    // Additional control signals can be added here as needed
);

    // Define opcodes for the supported instructions using an enumeration for clarity
    typedef enum logic [6:0] {
        OP_ADD  = 7'b0110011, // R-type ADD instruction
        OP_SUB  = 7'b0110011, // R-type SUB instruction (distinguished by funct7)
        // Add more opcodes for different instruction types (e.g., AND, OR, etc.)
    } opcode_t;

    // Use combinational logic to generate control signals based on the opcode
    always_comb begin
        // Initialize control signals to default values
        reg_write = 1'b0;    // Disable register writing by default
        alu_op    = 5'd0;    // Default ALU operation (e.g., ADD)

        // Decode the opcode to set control signals accordingly
        case (opcode)
            OP_ADD: begin
                // For ADD and SUB, differentiation is needed based on funct7
                // Here, we assume that differentiation is handled elsewhere or simplified
                reg_write = 1'b1;        // Enable writing to the register file
                alu_op    = 5'b00000;    // Set ALU to perform addition
            end

            // Add more cases for other opcodes, setting reg_write and alu_op as needed
            // For example:
            // OP_SUB: begin
            //     reg_write = 1'b1;
            //     alu_op    = 5'b00001; // SUB operation
            // end

            default: begin
                // For unrecognized opcodes, keep control signals at default values
                reg_write = 1'b0;
                alu_op    = 5'd0;
            end
        endcase
    end

endmodule
