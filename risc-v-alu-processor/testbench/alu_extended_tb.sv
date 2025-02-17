// alu_extended_tb.sv
// Testbench for Enhanced ALU Module
// Updated on 2025-02-17 - Timescale clarified to 1ns/1ps resolution
`timescale 1ns / 1ps

module ALU_Extended_tb;

    // Parameters
    parameter DATA_WIDTH = 32;
    parameter OP_WIDTH   = 5;
    parameter NUM_OPS    = 32;
    parameter SIMD_WIDTH = 4;

    // Localparam definitions for ALU operation codes
    localparam ADD  = 5'd0;
    localparam SUB  = 5'd1;
    localparam AND  = 5'd2;
    localparam OR   = 5'd3;
    localparam XOR  = 5'd4;
    localparam SLL  = 5'd5;
    localparam ROL  = 5'd6;
    localparam FADD = 5'd7;
    localparam FDIV = 5'd8;
    // Additional operations can be defined as needed

    // Testbench Signals
    logic clk;
    logic en;
    logic [SIMD_WIDTH*DATA_WIDTH-1:0] operand_a;
    logic [SIMD_WIDTH*DATA_WIDTH-1:0] operand_b;
    logic [SIMD_WIDTH*OP_WIDTH-1:0]   alu_op;
    logic [SIMD_WIDTH*DATA_WIDTH-1:0] result;
    logic [SIMD_WIDTH-1:0]            zero;
    logic [SIMD_WIDTH-1:0]            overflow;
    logic [SIMD_WIDTH-1:0]            carry_out;
    logic [SIMD_WIDTH-1:0]            negative;
    logic [SIMD_WIDTH*DATA_WIDTH-1:0] fp_result;
    logic [SIMD_WIDTH-1:0]            fp_overflow;

    // Instantiate SIMD ALU
    SIMD_ALU_Extended #(
        .DATA_WIDTH(DATA_WIDTH),
        .OP_WIDTH(OP_WIDTH),
        .SIMD_WIDTH(SIMD_WIDTH)
    ) uut (
        .clk(clk),
        .operand_a(operand_a),
        .operand_b(operand_b),
        .alu_op(alu_op),
        .en(en),
        .result(result),
        .zero(zero),
        .overflow(overflow),
        .carry_out(carry_out),
        .negative(negative),
        .fp_result(fp_result),
        .fp_overflow(fp_overflow)
    );

    // Clock Generation
    initial clk = 0;
    always #5 clk = ~clk; // Clock period = 10ns (100MHz)

    // Task to Apply Test Vectors
    task apply_test(
        input [DATA_WIDTH-1:0] a,
        input [DATA_WIDTH-1:0] b,
        input [OP_WIDTH-1:0]   op,
        input [DATA_WIDTH-1:0] expected_result,
        input                  expected_zero,
        input                  expected_overflow,
        input                  expected_carry_out,
        input                  expected_negative,
        input [DATA_WIDTH-1:0] expected_fp_result,
        input                  expected_fp_overflow
    );
        integer i;
        begin
            // Apply test vectors to each SIMD lane with a slight offset
            for (i = 0; i < SIMD_WIDTH; i++) begin
                operand_a[i*DATA_WIDTH +: DATA_WIDTH] = a + i;
                operand_b[i*DATA_WIDTH +: DATA_WIDTH] = b + i;
                alu_op[i*OP_WIDTH +: OP_WIDTH]       = op;
            end
            en = 1;
            @(posedge clk);
            // Assertions for each ALU instance
            for (i = 0; i < SIMD_WIDTH; i++) begin
                // Integer Operations
                assert(result[i*DATA_WIDTH +: DATA_WIDTH] == (expected_result + i))
                    else $error("ALU Instance %0d: Result mismatch for op %b", i, op);
                assert(zero[i] == ((expected_result + i) == 0))
                    else $error("ALU Instance %0d: Zero flag mismatch", i);
                assert(overflow[i] == expected_overflow)
                    else $error("ALU Instance %0d: Overflow flag mismatch", i);
                assert(carry_out[i] == expected_carry_out)
                    else $error("ALU Instance %0d: Carry-out flag mismatch", i);
                assert(negative[i] == ((expected_result + i)[DATA_WIDTH-1]))
                    else $error("ALU Instance %0d: Negative flag mismatch", i);
                // Floating-Point Operations
                assert(fp_result[i*DATA_WIDTH +: DATA_WIDTH] == expected_fp_result)
                    else $error("ALU Instance %0d: Floating-Point Result mismatch", i);
                assert(fp_overflow[i] == expected_fp_overflow)
                    else $error("ALU Instance %0d: Floating-Point Overflow mismatch", i);
            end
            // Clear Inputs
            en = 0;
            operand_a = 0;
            operand_b = 0;
            alu_op = 0;
        end
    endtask

    // Enhanced Coverage Collection for ALU operations
    covergroup alu_ops_cg @(posedge clk);
        coverpoint uut.alu_op {
            bins add_bin  = { ADD };
            bins sub_bin  = { SUB };
            bins and_bin  = { AND };
            bins or_bin   = { OR };
            bins xor_bin  = { XOR };
            bins sll_bin  = { SLL };
            bins rol_bin  = { ROL };
            bins fadd_bin = { FADD };
            bins fdiv_bin = { FDIV };
            // Additional bins can be added as necessary
        }
    endgroup

    // Coverage bins for saturating arithmetic
    covergroup sat_cg @(posedge clk);
        coverpoint uut.saturate {
            bins satOn  = {1'b1};
            bins satOff = {1'b0};
        }
    endgroup

    // Constrained-Random Testing: Set a reproducible seed
    initial begin
        $srandom(32'hDEADBEEF);
    end

    // Random test generation and directed tests
    initial begin
        alu_ops_cg alu_cov = new();
        sat_cg s_cov = new();

        // Initialize Inputs
        en = 0;
        operand_a = 0;
        operand_b = 0;
        alu_op = 0;

        // Wait for global reset
        #10;

        // Directed Test 1: Addition
        apply_test(
            32'd10,             // operand_a
            32'd5,              // operand_b
            ADD,                // alu_op
            32'd15,             // expected_result
            1'b0,               // expected_zero
            1'b0,               // expected_overflow
            1'b0,               // expected_carry_out
            1'b0,               // expected_negative
            32'd15,             // expected_fp_result
            1'b0                // expected_fp_overflow
        );

        // Directed Test 2: Subtraction
        apply_test(
            32'd20,             // operand_a
            32'd30,             // operand_b
            SUB,                // alu_op
            32'd-10,            // expected_result
            1'b0,               // expected_zero
            1'b1,               // expected_overflow (if signed)
            1'b1,               // expected_carry_out
            1'b1,               // expected_negative
            32'd-10,            // expected_fp_result
            1'b0                // expected_fp_overflow
        );

        // Directed Test 3: Logical AND
        apply_test(
            32'hFF00FF00,       // operand_a
            32'h0F0F0F0F,       // operand_b
            AND,                // alu_op
            32'h0F000F00,       // expected_result
            1'b0,               // expected_zero
            1'b0,               // expected_overflow
            1'b0,               // expected_carry_out
            1'b0,               // expected_negative
            32'h0F000F00,       // expected_fp_result
            1'b0                // expected_fp_overflow
        );

        // Directed Test 4: Logical OR
        apply_test(
            32'hFF00FF00,       // operand_a
            32'h0F0F0F0F,       // operand_b
            OR,                 // alu_op
            32'hFF0FFF0F,       // expected_result
            1'b0,               // expected_zero
            1'b0,               // expected_overflow
            1'b0,               // expected_carry_out
            1'b1,               // expected_negative
            32'hFF0FFF0F,       // expected_fp_result
            1'b0                // expected_fp_overflow
        );

        // Directed Test 5: XOR
        apply_test(
            32'hAAAA5555,       // operand_a
            32'h5555AAAA,       // operand_b
            XOR,                // alu_op
            32'hFFFFFFFF,       // expected_result
            1'b0,               // expected_zero
            1'b0,               // expected_overflow
            1'b0,               // expected_carry_out
            1'b1,               // expected_negative
            32'hFFFFFFFF,       // expected_fp_result
            1'b0                // expected_fp_overflow
        );

        // Directed Test 6: Shift Left Logical
        apply_test(
            32'd1,              // operand_a
            32'd4,              // operand_b (shift by 4)
            SLL,                // alu_op
            32'd16,             // expected_result
            1'b0,               // expected_zero
            1'b0,               // expected_overflow
            1'b0,               // expected_carry_out
            1'b0,               // expected_negative
            32'd16,             // expected_fp_result
            1'b0                // expected_fp_overflow
        );

        // Directed Test 7: Rotate Left
        apply_test(
            32'h12345678,       // operand_a
            32'd8,              // operand_b (rotate by 8)
            ROL,                // alu_op
            32'h34567812,       // expected_result
            1'b0,               // expected_zero
            1'b0,               // expected_overflow
            1'b0,               // expected_carry_out
            1'b0,               // expected_negative
            32'h34567812,       // expected_fp_result
            1'b0                // expected_fp_overflow
        );

        // Directed Test 8: Floating-Point Addition
        apply_test(
            32'h40000000,       // operand_a (2.0 in IEEE 754)
            32'h40000000,       // operand_b (2.0 in IEEE 754)
            FADD,               // alu_op
            32'h40000000,       // expected_result (ignored for FPU)
            1'b0,               // expected_zero (ignored for FPU)
            1'b0,               // expected_overflow (FPU)
            1'b0,               // expected_carry_out (ignored for FPU)
            1'b0,               // expected_negative (ignored for FPU)
            32'h40800000,       // expected_fp_result (4.0 in IEEE 754)
            1'b0                // expected_fp_overflow
        );

        // Directed Test 9: Floating-Point Division by Zero
        apply_test(
            32'h40000000,       // operand_a (2.0 in IEEE 754)
            32'h00000000,       // operand_b (0.0 in IEEE 754)
            FDIV,               // alu_op
            32'h40000000,       // expected_result (ignored for FPU)
            1'b0,               // expected_zero (ignored for FPU)
            1'b1,               // expected_overflow (FPU)
            1'b0,               // expected_carry_out (ignored for FPU)
            1'b0,               // expected_negative (ignored for FPU)
            32'h00000000,       // expected_fp_result (undefined, set to 0)
            1'b1                // expected_fp_overflow
        );

        // Directed Test 10: SIMD Addition
        apply_test(
            32'd100,            // operand_a
            32'd200,            // operand_b
            ADD,                // alu_op
            32'd300,            // expected_result
            1'b0,               // expected_zero
            1'b0,               // expected_overflow
            1'b0,               // expected_carry_out
            1'b0,               // expected_negative
            32'd300,            // expected_fp_result
            1'b0                // expected_fp_overflow
        );

        // Constrained-Random Tests: Random test generation with reproducible seed
        repeat(1000) begin
            // Operands are constrained to full 32-bit range for stress testing.
            operand_a = $urandom_range(0, 32'hFFFF_FFFF);
            operand_b = $urandom_range(0, 32'hFFFF_FFFF);
            alu_op    = $urandom_range(0, 31);
            @(posedge clk);
        end

        // Additional random tests to stress saturate logic
        repeat(50) begin
            operand_a = $urandom_range(0, 32'hFFFFFFFF);
            operand_b = $urandom_range(0, 32'hFFFFFFFF);
            alu_op    = $urandom_range(0, 31);
            @(posedge clk);
        end

        // End Simulation
        #20;
        $display("All tests completed.");
        $finish;
    end

    // Simple scoreboard/reference model
    // (Reference model 'ref_result' must be defined or this block removed)
    always_ff @(posedge clk) begin
        // Uncomment and implement the reference model comparison as needed:
        // if (uut.result !== ref_result) begin
        //     $error("Mismatch between DUT result and reference result");
        // end
    end

    // Simple FP scoreboard
    always_ff @(posedge clk) begin
        // Compare fp_result with a reference model if needed
    end

endmodule
