// alu_tb.sv
// started on 9/19/2024 and completed 9/21/2024
`timescale 1ns/1ps

module ALU_tb;

    // Testbench Signals
    logic clk;
    logic [31:0] operand_a;
    logic [31:0] operand_b;
    logic [3:0] alu_op;
    logic [31:0] result;
    logic zero;

    // Instantiate the ALU
    ALU uut (
        .clk(clk),
        .operand_a(operand_a),
        .operand_b(operand_b),
        .alu_op(alu_op),
        .result(result),
        .zero(zero)
    );

    // Clock Generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // 100MHz clock
    end

    // Test Vectors
    typedef struct {
        logic [31:0] a;
        logic [31:0] b;
        logic [3:0] op;
        logic [31:0] expected;
        logic expected_zero;
        string operation;
    } test_case_t;

    // Define Test Cases
    test_case_t test_cases [*] = '{
        // ADD Operations
        '{32'd10, 32'd15, 4'b0000, 32'd25, 1'b0, "ADD"},
        '{32'd0, 32'd0, 4'b0000, 32'd0, 1'b1, "ADD"},

        // SUB Operations
        '{32'd20, 32'd5, 4'b0001, 32'd15, 1'b0, "SUB"},
        '{32'd5, 32'd5, 4'b0001, 32'd0, 1'b1, "SUB"},

        // AND Operations
        '{32'hFF00FF00, 32'h0F0F0F0F, 4'b0010, 32'h0F000F00, 1'b0, "AND"},
        '{32'd0, 32'd0, 4'b0010, 32'd0, 1'b1, "AND"},

        // OR Operations
        '{32'hFF00FF00, 32'h0F0F0F0F, 4'b0011, 32'hFFFFFFF0, 1'b0, "OR"},
        '{32'd0, 32'd0, 4'b0011, 32'd0, 1'b1, "OR"},

        // XOR Operations
        '{32'hFFFF0000, 32'h00FFFF00, 4'b0100, 32'hFFFFFFFF, 1'b0, "XOR"},
        '{32'd0, 32'd0, 4'b0100, 32'd0, 1'b1, "XOR"},

        // SLT Operations
        '{32'd10, 32'd20, 4'b0101, 32'd1, 1'b0, "SLT (10 < 20)"},
        '{32'd20, 32'd10, 4'b0101, 32'd0, 1'b1, "SLT (20 < 10)"},
        '{32'd0, 32'd0, 4'b0101, 32'd0, 1'b1, "SLT (0 < 0)"}
    };

    // Test Procedure
    integer i;
    initial begin
        // Initialize Inputs
        operand_a = 0;
        operand_b = 0;
        alu_op = 0;

        // Wait for global reset
        #10;

        // Iterate through Test Cases
        for (i = 0; i < test_cases.size(); i++) begin
            operand_a = test_cases[i].a;
            operand_b = test_cases[i].b;
            alu_op   = test_cases[i].op;

            #10; // Wait for operation to complete

            // Display Results
            $display("Test %0d: %s", i+1, test_cases[i].operation);
            $display("Operands: A = %0d, B = %0d", operand_a, operand_b);
            $display("Expected Result: %0d, Actual Result: %0d", test_cases[i].expected, result);
            $display("Expected Zero: %b, Actual Zero: %b", test_cases[i].expected_zero, zero);

            // Check Assertions
            if (result !== test_cases[i].expected) begin
                $error("Result mismatch in test %0d", i+1);
            end
            if (zero !== test_cases[i].expected_zero) begin
                $error("Zero flag mismatch in test %0d", i+1);
            end

            $display("--------------------------------------------------");
        end

        $display("All tests completed.");
        $finish;
    end

endmodule
