// control_unit.sv
// This module generates control signals based on the instruction's opcode
// It determines how the ALU should operate for each instruction
// started on 9/27/2024 and completed 9/30/2024

module ControlUnit (
    input  logic [6:0] opcode,       // Opcode field from the instruction
    output logic       reg_write,    // Control signal to enable writing to the register file
    output logic       mem_read,     // Control signal for memory read
    output logic       mem_write,    // Control signal for memory write
    output logic       branch,       // Control signal indicating branch instruction
    output logic       jump,         // Control signal indicating jump instruction
    output logic [4:0] alu_op        // ALU operation code to control the ALU's behavior
);

    // Define opcodes for the supported instructions using an enumeration for clarity
    typedef enum logic [6:0] {
        OP_ADD   = 7'b0110011, // R-type ADD
        OP_LW    = 7'b0000011, // Load Word
        OP_SW    = 7'b0100011, // Store Word
        OP_BEQ   = 7'b1100011, // Branch if Equal
        OP_JAL   = 7'b1101111  // Jump and Link
        // Add more opcodes for different instruction types (e.g., AND, OR, etc.)
    } opcode_t;

    // Use combinational logic to generate control signals based on the opcode
    always_comb begin
        // Initialize control signals to default values
        reg_write  = 1'b0;    // Disable register writing by default
        mem_read   = 1'b0;    // Disable memory read by default
        mem_write  = 1'b0;    // Disable memory write by default
        branch     = 1'b0;    // Disable branch by default
        jump       = 1'b0;    // Disable jump by default
        alu_op     = 5'd0;    // Default ALU operation (e.g., ADD)

        // Decode the opcode to set control signals accordingly
        case (opcode)
            OP_ADD: begin
                // For ADD and SUB, differentiation is needed based on funct7
                // Here, we assume that differentiation is handled elsewhere or simplified
                reg_write = 1'b1;        // Enable writing to the register file
                alu_op    = 5'b00000;    // Set ALU to perform addition
            end
            OP_LW: begin
                reg_write = 1'b1;
                mem_read  = 1'b1;
                alu_op    = 5'b00000; // Use ADD to compute address
            end
            OP_SW: begin
                mem_write = 1'b1;
                alu_op    = 5'b00000; // Use ADD to compute address
            end
            OP_BEQ: begin
                branch  = 1'b1;
                alu_op  = 5'b00001; // ALU subtract for compare
            end
            OP_JAL: begin
                jump    = 1'b1;
                reg_write = 1'b1;   // Usually link to register
                // alu_op can remain 0 or set to special if needed
            end
            default: begin
                // For unrecognized opcodes, keep control signals at default values
                reg_write = 1'b0;
                mem_read  = 1'b0;
                mem_write = 1'b0;
                branch    = 1'b0;
                jump      = 1'b0;
                alu_op    = 5'd0;
            end
        endcase
    end

endmodule
