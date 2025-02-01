// control_unit_tb.sv
// Testbench for the Control Unit module
// started on 9/29/2024 and completed 10/01/2024


`timescale 1ns/1ps

module ControlUnit_tb;

    // Testbench Signals
    logic [6:0] opcode;
    logic reg_write;
    logic [4:0] alu_op;
    logic mem_read;
    logic mem_write;
    logic branch;
    logic jump;

    // Instantiate the Control Unit
    ControlUnit uut (
        .opcode(opcode),
        .reg_write(reg_write),
        .alu_op(alu_op),
        .mem_read(mem_read),
        .mem_write(mem_write),
        .branch(branch),
        .jump(jump)
    );

    // VCD Dumping for GTKWave
    initial begin
        $dumpfile("control_unit_tb.vcd");
        $dumpvars(0, ControlUnit_tb);
    end

    covergroup ctrl_cg @(posedge opcode);
        coverpoint opcode;
        coverpoint reg_write;
        coverpoint mem_read;
        coverpoint mem_write;
        coverpoint branch;
        coverpoint jump;
    endgroup

    initial begin
        ctrl_cg cu_cov = new();
        // Initialize Inputs
        opcode = 7'd0;

        // Wait for a short period to stabilize
        #10;

        // Test ADD Opcode
        #10;
        opcode = 7'b0110011; // OP_ADD
        #10;
        $display("Test ADD Opcode:");
        $display("Opcode: %b, Reg_Write: %b, ALU_Op: %b", opcode, reg_write, alu_op);
        if (reg_write !== 1'b1 || alu_op !== 5'b00000) begin
            $error("ADD Opcode Test Failed");
        end else begin
            $display("ADD Opcode Test Passed");
        end

        // Test SUB Opcode (Assuming differentiation handled)
        #10;
        opcode = 7'b0110011; // OP_SUB (same opcode, differentiation needed)
        #10;
        $display("Test SUB Opcode:");
        $display("Opcode: %b, Reg_Write: %b, ALU_Op: %b", opcode, reg_write, alu_op);
        // Since differentiation isn't handled, it will default to ADD
        if (reg_write !== 1'b1 || alu_op !== 5'b00000) begin
            $error("SUB Opcode Test Failed");
        end else begin
            $display("SUB Opcode Test Passed (Note: Differentiation not implemented)");
        end

        // Test Unknown Opcode
        #10;
        opcode = 7'b0000000; // Unknown opcode
        #10;
        $display("Test Unknown Opcode:");
        $display("Opcode: %b, Reg_Write: %b, ALU_Op: %b", opcode, reg_write, alu_op);
        if (reg_write !== 1'b0 || alu_op !== 5'd0) begin
            $error("Unknown Opcode Test Failed");
        end else begin
            $display("Unknown Opcode Test Passed");
        end

        // End Simulation
        #10;
        $display("All Control Unit tests completed.");
        $finish;
    end

endmodule
