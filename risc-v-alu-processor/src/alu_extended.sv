// alu_extended.sv
// Enhanced ALU Module with Additional Operations, Hierarchical Design, Parameterization, Flag Extensions, Synchronous Elements, FPU Integration, and SIMD Support
// Developed on: 10/26/2024
// Updated on 12/3 - 12/4/2-24
module ALU_Extended #(
    parameter DATA_WIDTH = 32,
    parameter OP_WIDTH = 5,
    parameter NUM_OPS = 32,
    parameter SIMD_WIDTH = 4 // Number of parallel ALUs for SIMD
) (
    input  logic                 clk,         // Clock signal for synchronous operations
    input  logic [DATA_WIDTH-1:0] operand_a,  // First operand
    input  logic [DATA_WIDTH-1:0] operand_b,  // Second operand
    input  logic [OP_WIDTH-1:0]    alu_op,     // ALU operation code
    input  logic                   en,         // Enable signal
    output logic [DATA_WIDTH-1:0]  result,     // ALU operation result
    output logic                    zero,       // Zero flag
    output logic                    overflow,   // Overflow flag
    output logic                    carry_out,  // Carry-out flag
    output logic                    negative,   // Negative flag
    // Floating-Point Outputs
    output logic [DATA_WIDTH-1:0]  fp_result,  // Floating-Point operation result
    output logic                    fp_overflow // Floating-Point overflow flag
);
    // Enumeration of ALU operations
    typedef enum logic [4:0] {
        // Basic Arithmetic
        ADD  = 5'b00000,
        SUB  = 5'b00001,
        MUL  = 5'b01011,
        DIV  = 5'b01100,
        MOD  = 5'b01101,

        // Logical Operations
        AND  = 5'b00010,
        OR   = 5'b00011,
        XOR  = 5'b00100,
        XNOR = 5'b01110,
        NOR  = 5'b01001,

        // Shift Operations
        SLL  = 5'b00110,
        SRL  = 5'b00111,
        SRA  = 5'b01000,
        ROL  = 5'b01111, // Rotate Left
        ROR  = 5'b10000, // Rotate Right

        // Bit Manipulation
        BCLR = 5'b10001, // Bit Clear
        BSET = 5'b10010, // Bit Set
        BTGL = 5'b10011, // Bit Toggle

        // Floating-Point Operations
        FADD = 5'b10100,
        FSUB = 5'b10101,
        FMUL = 5'b10110,
        FDIV = 5'b10111

        // ... Add more operations as needed
    } alu_operation_t;

    // Internal signals for sub-module outputs
    logic [DATA_WIDTH-1:0] add_sub_result;
    logic                  subtract;
    logic                  carry_out_internal;
    logic                  overflow_internal;

    logic [DATA_WIDTH-1:0] logic_result;
    logic [2:0]             logic_op;

    logic [DATA_WIDTH-1:0] shift_result;
    logic                  shift_arith;
    logic                  shift_dir;

    // Floating-Point Internal Signals
    logic [DATA_WIDTH-1:0] fpu_result_internal;
    logic                  fpu_overflow_internal;

    // Instantiate Adder/Subtractor
    AdderSubtractor #(
        .DATA_WIDTH(DATA_WIDTH)
    ) adder_subtractor_inst (
        .a(operand_a),
        .b(operand_b),
        .subtract(subtract),
        .sum(add_sub_result),
        .carry_out(carry_out_internal),
        .overflow(overflow_internal)
    );

    // Instantiate Logic Unit
    LogicUnit #(
        .DATA_WIDTH(DATA_WIDTH)
    ) logic_unit_inst (
        .a(operand_a),
        .b(operand_b),
        .operation(logic_op),
        .result(logic_result)
    );

    // Instantiate Shift Unit
    ShiftUnit #(
        .DATA_WIDTH(DATA_WIDTH)
    ) shift_unit_inst (
        .a(operand_a),
        .shift_amount(operand_b[4:0]),
        .arith(shift_arith),
        .direction(shift_dir),
        .shifted(shift_result)
    );

    // Instantiate Floating-Point Unit
    FloatingPointUnit #(
        .DATA_WIDTH(DATA_WIDTH)
    ) fpu_inst (
        .a(operand_a),
        .b(operand_b),
        .operation(alu_op[2:0]), // Assuming lower 3 bits for FPU operations
        .result(fpu_result_internal),
        .overflow(fpu_overflow_internal)
    );

    // Operation Decoding and Sub-Module Control Signals
    always_comb begin
        // Default Control Signals
        subtract = 1'b0;
        logic_op = 3'b000;
        shift_arith = 1'b0;
        shift_dir = 1'b0;
        
        case (alu_op)
            ADD: begin
                subtract = 1'b0;
            end
            SUB: begin
                subtract = 1'b1;
            end
            AND, OR, XOR, NOR, XNOR: begin
                logic_op = alu_op[2:0];
            end
            SLL, SRL, SRA, ROL, ROR: begin
                shift_dir = (alu_op == SLL || alu_op == ROL) ? 1'b0 : 1'b1;
                shift_arith = (alu_op == SRA) ? 1'b1 : 1'b0;
            end
            default: begin
                // No operation
            end
        endcase
    end

    // Determine which sub-module's result to use based on alu_op
    logic [DATA_WIDTH-1:0] mux_result;
    logic selected_float_op;

    assign selected_float_op = (alu_op == FADD) || (alu_op == FSUB) || (alu_op == FMUL) || (alu_op == FDIV);

    always_comb begin
        if (selected_float_op) begin
            mux_result = fpu_result_internal;
        end else begin
            case (alu_op)
                ADD, SUB, MUL, DIV, MOD: mux_result = add_sub_result;
                AND, OR, XOR, NOR, XNOR: mux_result = logic_result;
                SLL, SRL, SRA, ROL, ROR: mux_result = shift_result;
                BCLR, BSET, BTGL: begin
                    case (alu_op)
                        BCLR: mux_result = operand_a & ~operand_b;
                        BSET: mux_result = operand_a | operand_b;
                        BTGL: mux_result = operand_a ^ operand_b;
                        default: mux_result = {DATA_WIDTH{1'b0}};
                    endcase
                end
                default: mux_result = {DATA_WIDTH{1'b0}};
            endcase
        end
    end

    // Synchronous Register for Result and Flags
    always_ff @(posedge clk) begin
        if (en) begin
            result     <= mux_result;
            zero       <= (mux_result == {DATA_WIDTH{1'b0}}) ? 1'b1 : 1'b0;
            overflow   <= selected_float_op ? fpu_overflow_internal : overflow_internal;
            carry_out  <= carry_out_internal;
            negative   <= mux_result[DATA_WIDTH-1];
            fp_result  <= fpu_result_internal;
            fp_overflow <= fpu_overflow_internal;
        end
    end

endmodule