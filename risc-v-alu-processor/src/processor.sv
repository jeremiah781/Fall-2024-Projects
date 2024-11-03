// processor.sv
// This module represents a simplified RISC-V processor
// It integrates the ALU, Register File, Instruction Memory, and Control Unit to execute instructions
// started on 10/17/2024 and completed 10/25/2024
module Processor (
    input  logic        clk,    // Clock signal
    input  logic        reset   // Reset signal to initialize the processor
);

    // ----- Program Counter (PC) -----
    // The PC holds the address of the current instruction
    logic [31:0] PC;

    // ----- Instruction Memory -----
    // Fetches the instruction based on the current PC value
    logic [31:0] current_instruction;
    InstructionMemory imem (
        .address(PC),
        .instruction(current_instruction)
    );

    // ----- Register File -----
    // Handles reading and writing to the processor's registers.
    logic [4:0] read_reg1, read_reg2, write_reg; // Register addresses
    logic [31:0] read_data1, read_data2, write_data; // Data read from and written to registers
    logic reg_write; // Control signal to enable writing to the register file
    RegisterFile regfile (
        .clk(clk),
        .reset(reset),
        .read_reg1(read_reg1),
        .read_reg2(read_reg2),
        .write_reg(write_reg),
        .write_data(write_data),
        .reg_write(reg_write),
        .read_data1(read_data1),
        .read_data2(read_data2)
    );

    // ----- Control Unit -----
    // Generates control signals based on the opcode of the current instruction
    logic [6:0] opcode;
    logic [4:0] alu_op;
    ControlUnit control (
        .opcode(opcode),
        .reg_write(reg_write),
        .alu_op(alu_op)
    );

    // ----- ALU -----
    // Executes arithmetic and logic operations
    logic [31:0] alu_result;
    logic        alu_zero;
    ALU_Pipelined alu (
        .clk(clk),
        .reset(reset),
        .operand_a(read_data1),
        .operand_b(read_data2),
        .alu_op(alu_op),
        .result(alu_result),
        .zero(alu_zero)
    );

    // ----- Instruction Fields Extraction -----
    // Break down the instruction into its constituent parts for decoding
    logic [6:0] opcode_field;
    logic [4:0] rd;
    logic [4:0] rs1;
    logic [4:0] rs2;
    logic [2:0] funct3;
    logic [6:0] funct7;

    // Extract fields from the fetched instruction
    assign opcode_field = current_instruction[6:0];     // Bits 0-6
    assign rd          = current_instruction[11:7];     // Bits 7-11
    assign funct3      = current_instruction[14:12];    // Bits 12-14
    assign rs1         = current_instruction[19:15];    // Bits 15-19
    assign rs2         = current_instruction[24:20];    // Bits 20-24
    assign funct7      = current_instruction[31:25];    // Bits 25-31

    // Connect the extracted opcode to the Control Unit
    assign opcode = opcode_field;

    // Connect register addresses for reading
    assign read_reg1 = rs1;
    assign read_reg2 = rs2;

    // Connect the write register address and data
    assign write_reg = rd;
    assign write_data = alu_result; // For simplicity, assume ALU result is written back

    // ----- Program Counter Logic -----
    // Updates the PC to point to the next instruction.
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            PC <= 32'd0; // Initialize PC to zero on reset
        end else begin
            PC <= PC + 4; // Move to the next instruction (assuming 4-byte instructions)
        end
    end

endmodule
