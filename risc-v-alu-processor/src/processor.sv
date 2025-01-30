`timescale 1ns/1ps

// processor.sv
// Enhanced RISC-V Processor Module with Branching, Pipelining, Memory Integration, Interrupts, and Power Optimizations
// Developed on: 11/05/2024
// Updated 12/4/ - 12/5 for extra credit


module Processor (
    input  logic        clk,        // Clock signal
    input  logic        reset,      // Reset signal to initialize the processor
    input  logic        interrupt,  // Interrupt signal

    // Debug signals for monitoring pipeline operation
    output logic pipeline_stall_dbg,
    output logic pipeline_flush_dbg
);

    // Add these wire declarations at the top
    wire        ID_EX_reg_write_w, ID_EX_mem_read_w, ID_EX_mem_write_w;
    wire        ID_EX_branch_w, ID_EX_jump_w;
    wire [4:0]  ID_EX_alu_op_w;
    wire        stall_w;

    // Declare the stall signal as logic instead of wire to allow procedural assignments
    logic stall; // Changed from wire to logic

    // ----- Program Counter (PC) -----
    // The PC holds the address of the next instruction to fetch.
    logic [31:0] PC;
    logic [31:0] next_PC;

    // ----- Pipeline Registers -----
    // IF/ID Pipeline Register: Holds information between Instruction Fetch and Instruction Decode stages.
    logic [31:0] IF_ID_instruction, IF_ID_PC;

    // ID/EX Pipeline Register: Holds information between Instruction Decode and Execute stages.
    logic [6:0]  ID_EX_opcode;
    logic [4:0]  ID_EX_rd, ID_EX_rs1, ID_EX_rs2;
    logic [2:0]  ID_EX_funct3;
    logic [6:0]  ID_EX_funct7;
    logic [31:0] ID_EX_read_data1, ID_EX_read_data2;
    logic [31:0] ID_EX_immediate;
    logic        ID_EX_reg_write, ID_EX_mem_read, ID_EX_mem_write;
    logic        ID_EX_branch, ID_EX_jump;
    logic [4:0]  ID_EX_alu_op;
    logic [31:0] ID_EX_PC;

    // EX/MEM Pipeline Register: Holds information between Execute and Memory stages.
    logic [31:0] EX_MEM_alu_result, EX_MEM_write_data;
    logic [4:0]  EX_MEM_rd;
    logic        EX_MEM_reg_write, EX_MEM_mem_read, EX_MEM_mem_write;
    logic        EX_MEM_branch, EX_MEM_jump, EX_MEM_zero;

    // MEM/WB Pipeline Register: Holds information between Memory and Write-Back stages.
    logic [31:0] MEM_WB_mem_data;
    logic [31:0] MEM_WB_alu_result;
    logic [4:0]  MEM_WB_rd;
    logic        MEM_WB_reg_write;

    // ----- Instruction Memory -----
    // Fetches the instruction based on the current PC value.
    logic [31:0] current_instruction;
    InstructionMemory imem (
        .address(PC),
        .instruction(current_instruction)
    );

    // ----- Data Memory -----
    // Handles load (LW) and store (SW) operations by reading from and writing to memory.
    logic [31:0] mem_read_data;
    DataMemory dmem (
        .clk(clk),
        .address(EX_MEM_alu_result), // Address computed by ALU
        .write_data(EX_MEM_write_data), // Data to be written (for SW)
        .mem_write(EX_MEM_mem_write), // Control signal for write
        .mem_read(EX_MEM_mem_read),   // Control signal for read
        .read_data(mem_read_data)     // Data read from memory (for LW)
    );

    // ----- Register File -----
    // Manages the processor's general-purpose registers, allowing data to be read from and written to them.
    logic [31:0] write_data;
    logic [31:0] read_data1, read_data2;
    RegisterFile regfile (
        .clk(clk),
        .reset(reset),
        .read_reg1(IF_ID_instruction[19:15]), // rs1 field from IF/ID stage
        .read_reg2(IF_ID_instruction[24:20]), // rs2 field from IF/ID stage
        .write_reg(MEM_WB_rd),                // Destination register from MEM/WB stage
        .write_data(write_data),               // Data to write to the register
        .reg_write(MEM_WB_reg_write),         // Control signal to enable write
        .read_data1(read_data1),               // Data read from rs1
        .read_data2(read_data2)                // Data read from rs2
    );

    // ----- Control Unit -----
    // Generates control signals based on the opcode of the instruction in the ID/EX stage.
    ControlUnit control (
        .opcode(ID_EX_opcode),
        .reg_write(ID_EX_reg_write_w),
        .mem_read(ID_EX_mem_read_w),
        .mem_write(ID_EX_mem_write_w),
        .branch(ID_EX_branch_w),
        .jump(ID_EX_jump_w),
        .alu_op(ID_EX_alu_op_w)
    );

    // ----- ALU -----
    // Executes arithmetic and logic operations as specified by the ALU operation code.
    logic [31:0] alu_result;
    logic        alu_zero;
    ALU_Extended alu (
        .clk(clk),
        .en(1'b1),
        .operand_a(ID_EX_read_data1),    // Operand A from Register File
        .operand_b(ID_EX_immediate),     // Operand B (could be immediate or register data)
        .alu_op(ID_EX_alu_op),           // Operation code from Control Unit
        .result(alu_result),             // Result of the ALU operation
        .zero(alu_zero),                 // Zero flag indicating if result is zero
        .overflow(),                      // Overflow flag (optional)
        .carry_out(),                     // Carry-out flag (optional)
        .negative(),                      // Negative flag (optional)
        .fp_result(),                     // Floating-Point result (if applicable)
        .fp_overflow()                    // Floating-Point overflow flag (if applicable)
    );

    // ----- Branch Comparator -----
    // Determines if a branch should be taken based on the branch condition and ALU zero flag.
    logic branch_taken;
    assign branch_taken = (ID_EX_branch && alu_zero);

    // ----- Next PC Logic -----
    // Determines the next value of the Program Counter based on branching and jumping.
    always @* begin
        if (ID_EX_jump) begin
            next_PC = ID_EX_immediate; // Unconditional jump: set PC to immediate address
        end else if (branch_taken) begin
            next_PC = ID_EX_PC + ID_EX_immediate; // Conditional branch: set PC relative to current
        end else begin
            next_PC = PC + 4; // Sequential execution: increment PC by 4
        end
    end

    // ----- Hazard Detection Unit -----
    // Detects data hazards that require stalling the pipeline to prevent incorrect data usage.
    HazardDetectionUnit hazard (
        .ID_EX_mem_read(ID_EX_mem_read), // Indicates if the previous instruction is a load
        .ID_EX_rd(ID_EX_rd),             // Destination register of the previous instruction
        .IF_ID_rs1(IF_ID_instruction[19:15]), // Source register 1 of the current instruction
        .IF_ID_rs2(IF_ID_instruction[24:20]), // Source register 2 of the current instruction
        .stall(stall_w)                      // Output stall signal
    );

    // ----- Pipeline Control -----
    // Determines whether to flush the pipeline based on stalling or interrupt signals.
    logic flush;
    assign flush = stall || interrupt;

    // Assign debug signals
    assign pipeline_stall_dbg = stall;
    assign pipeline_flush_dbg  = flush;

    // ----- Pipeline Registers Update -----
    // **IF Stage:** Fetch the next instruction and update PC.
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            PC <= 32'd0; // Initialize PC to zero on reset
        end else if (!stall) begin
            PC <= next_PC; // Update PC to next_PC if not stalling
        end
    end

    // **IF/ID Register:** Pass fetched instruction and PC to the next stage.
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            IF_ID_instruction <= 32'd0;
            IF_ID_PC <= 32'd0;
        end else if (!stall) begin
            IF_ID_instruction <= current_instruction; // Instruction fetched from Instruction Memory
            IF_ID_PC <= PC;                           // Current PC value
        end
    end

    // **ID/EX Register:** Decode instruction and prepare data for execution.
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            ID_EX_opcode     <= 7'd0;
            ID_EX_rd         <= 5'd0;
            ID_EX_rs1        <= 5'd0;
            ID_EX_rs2        <= 5'd0;
            ID_EX_funct3     <= 3'd0;
            ID_EX_funct7     <= 7'd0;
            ID_EX_read_data1 <= 32'd0;
            ID_EX_read_data2 <= 32'd0;
            ID_EX_immediate  <= 32'd0;
            ID_EX_reg_write  <= 1'b0;
            ID_EX_mem_read   <= 1'b0;
            ID_EX_mem_write  <= 1'b0;
            ID_EX_branch     <= 1'b0;
            ID_EX_jump       <= 1'b0;
            ID_EX_alu_op     <= 5'd0;
            ID_EX_PC         <= 32'd0;
        end else if (flush) begin
            ID_EX_opcode     <= 7'd0;
            ID_EX_rd         <= 5'd0;
            ID_EX_rs1        <= 5'd0;
            ID_EX_rs2        <= 5'd0;
            ID_EX_funct3     <= 3'd0;
            ID_EX_funct7     <= 7'd0;
            ID_EX_read_data1 <= 32'd0;
            ID_EX_read_data2 <= 32'd0;
            ID_EX_immediate  <= 32'd0;
            ID_EX_reg_write  <= 1'b0;
            ID_EX_mem_read   <= 1'b0;
            ID_EX_mem_write  <= 1'b0;
            ID_EX_branch     <= 1'b0;
            ID_EX_jump       <= 1'b0;
            ID_EX_alu_op     <= 5'd0;
            ID_EX_PC         <= 32'd0;
        end else begin
            // Extract fields from the instruction
            ID_EX_opcode     <= IF_ID_instruction[6:0];   // Opcode field
            ID_EX_rd         <= IF_ID_instruction[11:7];  // Destination register
            ID_EX_rs1        <= IF_ID_instruction[19:15]; // Source register 1
            ID_EX_rs2        <= IF_ID_instruction[24:20]; // Source register 2
            ID_EX_funct3     <= IF_ID_instruction[14:12]; // Function field 3
            ID_EX_funct7     <= IF_ID_instruction[31:25]; // Function field 7
            ID_EX_read_data1 <= read_data1;                // Data from source register 1
            ID_EX_read_data2 <= read_data2;                // Data from source register 2
            ID_EX_immediate  <= sign_extend(IF_ID_instruction); // Sign-extended immediate value
            ID_EX_PC         <= IF_ID_PC;                  // Current PC value

            // Control signals are generated combinationally by the Control Unit based on ID_EX.opcode
            // These signals are already connected via the Control Unit instantiation above
        end
    end

    // Enhanced hazard detection for consecutive read/write to same register
    logic multi_cycle_in_progress;
    always @* begin
        stall_internal = stall_w;
        if (ID_EX_rd == IF_ID_instruction[19:15] && ID_EX_reg_write) begin
            // Additional logic to handle or bypass hazard
        end
        if (ID_EX_rd == IF_ID_instruction[19:15] && ID_EX_reg_write && multi_cycle_in_progress) begin
            stall_internal = 1'b1;
        end
    end

    // **EX/MEM Register:** Pass ALU results and control signals to the Memory stage.
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            EX_MEM_alu_result <= 32'd0;
            EX_MEM_write_data <= 32'd0;
            EX_MEM_rd         <= 5'd0;
            EX_MEM_reg_write  <= 1'b0;
            EX_MEM_mem_read   <= 1'b0;
            EX_MEM_mem_write  <= 1'b0;
            EX_MEM_branch     <= 1'b0;
            EX_MEM_jump       <= 1'b0;
            EX_MEM_zero       <= 1'b0;
        end else begin
            EX_MEM_alu_result <= alu_result;        // Result from the ALU
            EX_MEM_write_data <= ID_EX_read_data2; // Data to write to memory (for SW)
            EX_MEM_rd         <= ID_EX_rd;         // Destination register
            EX_MEM_reg_write  <= ID_EX_reg_write;  // Control signal for register write
            EX_MEM_mem_read   <= ID_EX_mem_read;   // Control signal for memory read
            EX_MEM_mem_write  <= ID_EX_mem_write;  // Control signal for memory write
            EX_MEM_branch     <= ID_EX_branch;     // Branch control signal
            EX_MEM_jump       <= ID_EX_jump;       // Jump control signal
            EX_MEM_zero       <= alu_zero;         // Zero flag from ALU (for branch decisions)
        end
    end

    // **MEM/WB Register:** Pass data from Memory or ALU to the Write-Back stage.
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            MEM_WB_mem_data   <= 32'd0;
            MEM_WB_alu_result <= 32'd0;
            MEM_WB_rd         <= 5'd0;
            MEM_WB_reg_write  <= 1'b0;
        end else begin
            MEM_WB_mem_data   <= mem_read_data;    // Data read from Data Memory (for LW)
            MEM_WB_alu_result <= EX_MEM_alu_result; // ALU result (for arithmetic operations)
            MEM_WB_rd         <= EX_MEM_rd;        // Destination register
            MEM_WB_reg_write  <= EX_MEM_reg_write; // Control signal for register write
        end
    end

    // ----- Write-Back Stage -----
    // Determines the data to write back to the Register File based on memory read signals.
    assign write_data = EX_MEM_mem_read ? MEM_WB_mem_data : MEM_WB_alu_result;

    // ----- Instruction Fields Extraction for Immediate -----
    // Function to sign-extend immediate values based on instruction type.
    function [31:0] sign_extend(input [31:0] instr);
        case (instr[6:0])
            // I-Type Instructions (e.g., ADDI, ORI, LW, JALR)
            7'b0010011, // ADDI, ORI, etc.
            7'b0000011, // LW
            7'b1100111: // JALR
                sign_extend = {{20{instr[31]}}, instr[31:20]};
            // S-Type Instructions (e.g., SW)
            7'b0100011:
                sign_extend = {{20{instr[31]}}, instr[31:25], instr[11:7]};
            // B-Type Instructions (e.g., BEQ, BNE)
            7'b1100011:
                sign_extend = {{19{instr[31]}}, instr[31], instr[7], instr[30:25], instr[11:8], 1'b0};
            // U-Type Instructions (e.g., LUI, AUIPC)
            7'b0110111,
            7'b0010111:
                sign_extend = {instr[31:12], 12'd0};
            // J-Type Instructions (e.g., JAL)
            7'b1101111:
                sign_extend = {{12{instr[31]}}, instr[19:12], instr[20], instr[30:21], 1'b0};
            default:
                sign_extend = 32'd0; // Default to zero for undefined types
        endcase
    endfunction

    // ----- Interrupt Handling -----
    // Simple interrupt handler that flushes the pipeline and jumps to an interrupt vector.
    // Note: This is a basic implementation; more complex systems may require prioritized interrupts and multiple vectors.
    logic [31:0] interrupt_vector = 32'h0000_1000; // Example interrupt vector address

    parameter PRIORITY_LEVELS = 4;
    logic [PRIORITY_LEVELS-1:0] interrupt_queue;
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            interrupt_queue <= '0;
            // Initialize as needed on reset
        end else if (interrupt) begin
            // Flush all pipeline registers by resetting them
            IF_ID_instruction <= 32'd0;
            IF_ID_PC <= 32'd0;
            ID_EX_opcode     <= 7'd0;
            ID_EX_rd         <= 5'd0;
            ID_EX_rs1        <= 5'd0;
            ID_EX_rs2        <= 5'd0;
            ID_EX_funct3     <= 3'd0;
            ID_EX_funct7     <= 7'd0;
            ID_EX_read_data1 <= 32'd0;
            ID_EX_read_data2 <= 32'd0;
            ID_EX_immediate  <= 32'd0;
            ID_EX_reg_write  <= 1'b0;
            ID_EX_mem_read   <= 1'b0;
            ID_EX_mem_write  <= 1'b0;
            ID_EX_branch     <= 1'b0;
            ID_EX_jump       <= 1'b0;
            ID_EX_alu_op     <= 5'd0;
            ID_EX_PC         <= 32'd0;
            EX_MEM_alu_result <= 32'd0;
            EX_MEM_write_data <= 32'd0;
            EX_MEM_rd         <= 5'd0;
            EX_MEM_reg_write  <= 1'b0;
            EX_MEM_mem_read   <= 1'b0;
            EX_MEM_mem_write  <= 1'b0;
            EX_MEM_branch     <= 1'b0;
            EX_MEM_jump       <= 1'b0;
            EX_MEM_zero       <= 1'b0;
            MEM_WB_mem_data   <= 32'd0;
            MEM_WB_alu_result <= 32'd0;
            MEM_WB_rd         <= 5'd0;
            MEM_WB_reg_write  <= 1'b0;
            // Redirect PC to the interrupt vector address
            PC <= interrupt_vector;
            // Enqueue interrupt in the lowest available priority slot
        end
    end

    // ----- Power and Performance Optimization -----
    // Example Placeholder for Clock Gating: Disable certain modules when not in use to save power.
    // Actual implementation would require identifying clock-enable signals for each module and controlling them based on activity.
    // For simplicity, this example assumes ALU is always enabled.
    // Implement clock gating based on module activity as per specific design requirements.

    // Then assign those wires to the actual registers
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            // ...existing reset logic...
        end else begin
            ID_EX_reg_write <= ID_EX_reg_write_w;
            ID_EX_mem_read  <= ID_EX_mem_read_w;
            ID_EX_mem_write <= ID_EX_mem_write_w;
            ID_EX_branch    <= ID_EX_branch_w;
            ID_EX_jump      <= ID_EX_jump_w;
            ID_EX_alu_op    <= ID_EX_alu_op_w;
        end
    end

    // Fix for unresolved stall wire
    logic stall_internal;
    assign stall = stall_internal;

    // Fix for hazard detection assignment
    always @* begin
        stall_internal = stall_w;
        if (ID_EX_rd == IF_ID_instruction[19:15] && ID_EX_reg_write && multi_cycle_in_progress) begin
            stall_internal = 1'b1;
        end
    end

endmodule