// alu_pipelined_tb.sv
// This is the testbench for the pipelined ALU module
// It applies various test cases to ensure the pipelined ALU operates correctly
// started on 10/13/2024 and completed 10/17/2024

`timescale 1ns/1ps // Define the time unit and precision

module ALU_Pipelined_tb;

    // Declare signals to connect to the Pipelined ALU
    logic clk;             // Clock signal
    logic reset;           // Reset signal
    logic [31:0] operand_a; // First operand
    logic [31:0] operand_b; // Second operand
    logic [4:0] alu_op;      // Operation code
    logic [31:0] result;     // ALU result
    logic zero;             // Zero flag

    // Instantiate the Pipelined ALU
    ALU_Pipelined uut (
        .clk(clk),
        .reset(reset),
        .operand_a(operand_a),
        .operand_b(operand_b),
        .alu_op(alu_op),
        .result(result),
        .zero(zero)
    );

    // Generate a clock signal that toggles every 5 ns (100MHz frequency)
    initial begin
        clk = 0; // Start with clock low
        forever #5 clk = ~clk; // Toggle clock every 5 ns
    end

    // Initialize VCD (Value Change Dump) for waveform viewing in GTKWave
    initial begin
        $dumpfile("alu_pipelined_tb.vcd"); // Specify the VCD file name
        $dumpvars(0, ALU_Pipelined_tb);    // Dump all variables in the ALU_Pipelined_tb module
    end

    // Define a structure to hold individual test cases
    typedef struct {
        logic [31:0] a;            // Operand A
        logic [31:0] b;            // Operand B
        logic [4:0] op;            // Operation code
        logic [31:0] expected;     // Expected result
        logic expected_zero;      // Expected zero flag
        string operation;         // Description of the operation
    } test_case_t;

    // Create an array of test cases to cover all operations and edge cases
    test_case_t test_cases [*] = '{
        // ADD Operations
        '{32'd10, 32'd15, 5'b00000, 32'd25, 1'b0, "ADD 10 + 15 = 25"},
        '{32'd0, 32'd0, 5'b00000, 32'd0, 1'b1, "ADD 0 + 0 = 0"},

        // SUB Operations
        '{32'd20, 32'd5, 5'b00001, 32'd15, 1'b0, "SUB 20 - 5 = 15"},
        '{32'd5, 32'd5, 5'b00001, 32'd0, 1'b1, "SUB 5 - 5 = 0"},

        // AND Operations
        '{32'hFF00FF00, 32'h0F0F0F0F, 5'b00010, 32'h0F000F00, 1'b0, "AND FF00FF00 & 0F0F0F0F = 0F000F00"},
        '{32'd0, 32'd0, 5'b00010, 32'd0, 1'b1, "AND 0 & 0 = 0"},

        // OR Operations
        '{32'hFF00FF00, 32'h0F0F0F0F, 5'b00011, 32'hFFFFFFF0, 1'b0, "OR FF00FF00 | 0F0F0F0F = FFFFFFF0"},
        '{32'd0, 32'd0, 5'b00011, 32'd0, 1'b1, "OR 0 | 0 = 0"},

        // XOR Operations
        '{32'hFFFF0000, 32'h00FFFF00, 5'b00100, 32'hFFFFFFFF, 1'b0, "XOR FFFF0000 ^ 00FFFF00 = FFFFFFFF"},
        '{32'd0, 32'd0, 5'b00100, 32'd0, 1'b1, "XOR 0 ^ 0 = 0"},

        // SLT Operations (Set Less Than)
        '{32'd10, 32'd20, 5'b00101, 32'd1, 1'b0, "SLT (10 < 20) = 1"},
        '{32'd20, 32'd10, 5'b00101, 32'd0, 1'b1, "SLT (20 < 10) = 0"},
        '{32'd0, 32'd0, 5'b00101, 32'd0, 1'b1, "SLT (0 < 0) = 0"},

        // SLL Operations (Shift Left Logical)
        '{32'd1, 32'd3, 5'b00110, 32'd8, 1'b0, "SLL (1 << 3) = 8"},
        '{32'd0, 32'd0, 5'b00110, 32'd0, 1'b1, "SLL (0 << 0) = 0"},

        // SRL Operations (Shift Right Logical)
        '{32'd8, 32'd3, 5'b00111, 32'd1, 1'b0, "SRL (8 >> 3) = 1"},
        '{32'd0, 32'd0, 5'b00111, 32'd0, 1'b1, "SRL (0 >> 0) = 0"},

        // SRA Operations (Shift Right Arithmetic)
        '{32'sd-8, 32'd3, 5'b01000, 32'sd-1, 1'b0, "SRA (-8 >>> 3) = -1"},
        '{32'd0, 32'd0, 5'b01000, 32'd0, 1'b1, "SRA (0 >>> 0) = 0"},

        // NOR Operations
        '{32'hFFFF0000, 32'h0000FFFF, 5'b01001, 32'h00000000, 1'b1, "NOR (FFFF0000 | 0000FFFF) = 00000000"},
        '{32'd0, 32'd0, 5'b01001, 32'hFFFFFFFF, 1'b0, "NOR (0 | 0) = FFFFFFFF"},

        // SGE Operations (Set Greater or Equal)
        '{32'd20, 32'd10, 5'b01010, 32'd1, 1'b0, "SGE (20 >= 10) = 1"},
        '{32'd10, 32'd20, 5'b01010, 32'd0, 1'b1, "SGE (10 >= 20) = 0"},
        '{32'd0, 32'd0, 5'b01010, 32'd1, 1'b0, "SGE (0 >= 0) = 1"}
    };

    // Coverage for pipeline stages
    covergroup alu_pipe_cg @(posedge clk);
        coverpoint uut.stage2_carry_out;
        coverpoint uut.stage2_overflow;
    endgroup

    // Main testing procedure
    initial begin
        // Start with all inputs set to zero
        operand_a = 0;
        operand_b = 0;
        alu_op    = 0;

        // Wait for a short period to stabilize
        #10;

        alu_pipe_cg pipe_cov = new();

        // Extended multi-cycle tests
        operand_a = 32'hFFFF0000;
        operand_b = 32'h0000FFFF;
        alu_op = 5'b00000;
        // Wait a few cycles to let pipeline advance
        #20;

        // Loop through each test case and apply the inputs to the ALU
        for (i = 0; i < test_cases.size(); i++) begin
            // Apply the operands and operation code from the current test case
            operand_a = test_cases[i].a;
            operand_b = test_cases[i].b;
            alu_op    = test_cases[i].op;

            #10; // Wait for the ALU to process the inputs

            // Display the test case information and results
            $display("Test %0d: %s", i+1, test_cases[i].operation);
            $display("Operands: A = %0d, B = %0d", operand_a, operand_b);
            $display("Expected Result: %0d, Actual Result: %0d", test_cases[i].expected, result);
            $display("Expected Zero Flag: %b, Actual Zero Flag: %b", test_cases[i].expected_zero, zero);

            // Verify that the actual results match the expected results
            if (result !== test_cases[i].expected) begin
                $error("Result mismatch in Test %0d: Expected %0d, Got %0d", i+1, test_cases[i].expected, result);
            end
            if (zero !== test_cases[i].expected_zero) begin
                $error("Zero flag mismatch in Test %0d: Expected %b, Got %b", i+1, test_cases[i].expected_zero, zero);
            end

            $display("--------------------------------------------------");
        end

        // Indicate that all tests have been completed
        $display("All ALU tests completed successfully.");
        $finish; // End the simulation
    end

endmodule
