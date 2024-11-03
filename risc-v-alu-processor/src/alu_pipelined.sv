// alu_pipelined.sv
// This module represents a pipelined version of the ALU to improve performance by dividing operations into stages
// It consists of two pipeline stages: Decode & Partial Compute, and Finalize Result & Set Flags
// started on 10/09/2024 and completed 10/15/2024


module ALU_Pipelined (
    input  logic        clk,         // Clock signal for synchronous operations
    input  logic        reset,       // Reset signal to initialize pipeline registers
    input  logic [31:0] operand_a,   // First operand
    input  logic [31:0] operand_b,   // Second operand
    input  logic [4:0]  alu_op,      // ALU operation code
    output logic [31:0] result,      // Final result after pipeline
    output logic        zero         // Zero flag indicating if the result is zero
);

    // ----- Pipeline Stage 1: Decode and Partial Compute -----
    // These registers hold intermediate values between pipeline stages
    logic [31:0] stage1_result; // Intermediate result from Stage 1
    logic [4:0]  stage1_op;     // Operation code passed to Stage 2

    // Stage 1 processes the ALU operation and computes a partial result
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            // On reset, clear the intermediate pipeline registers
            stage1_result <= 32'd0;
            stage1_op     <= 5'd0;
        end else begin
            // Pass the operation code to the next stage
            stage1_op <= alu_op;

            // Perform the ALU operation based on alu_op
            case (alu_op)
                5'b00000: stage1_result <= operand_a + operand_b;             // ADD
                5'b00001: stage1_result <= operand_a - operand_b;             // SUB
                5'b00010: stage1_result <= operand_a & operand_b;             // AND
                5'b00011: stage1_result <= operand_a | operand_b;             // OR
                5'b00100: stage1_result <= operand_a ^ operand_b;             // XOR
                5'b00101: stage1_result <= ($signed(operand_a) < $signed(operand_b)) ? 32'd1 : 32'd0; // SLT
                5'b00110: stage1_result <= operand_a << operand_b[4:0];       // SLL
                5'b00111: stage1_result <= operand_a >> operand_b[4:0];       // SRL
                5'b01000: stage1_result <= $signed(operand_a) >>> operand_b[4:0]; // SRA
                5'b01001: stage1_result <= ~(operand_a | operand_b);          // NOR
                5'b01010: stage1_result <= ($signed(operand_a) >= $signed(operand_b)) ? 32'd1 : 32'd0; // SGE
                default: stage1_result <= 32'd0; // Default case
            endcase
        end
    end

    // ----- Pipeline Stage 2: Finalize Result and Set Flags -----
    // These registers hold the final output after processing
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            // On reset, clear the final result register
            result <= 32'd0;
        end else begin
            // Pass the intermediate result to the final output
            result <= stage1_result;
        end
    end

    // ----- Zero Flag Assignment -----
    // Determine if the final result is zero
    assign zero = (result == 32'd0) ? 1'b1 : 1'b0;

endmodule
