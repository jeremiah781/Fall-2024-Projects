// Two-Bit Comparator Gate-Level Model
// Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Compares two 2-bit inputs and outputs equality, less than, and greater than signals.

module two_bit_comparator (
    input [1:0] a,      // 2-bit input a
    input [1:0] b,      // 2-bit input b
    output a_equals_b,   // Output high if a equals b
    output a_less_than_b,// Output high if a < b
    output a_greater_than_b // Output high if a > b
);

// Intermediate Signals
wire a1, a0, b1, b0;
wire eq1, eq0;
wire not_a1, not_b1, not_b0;

// Assign input bits to intermediate wires
assign a1 = a[1];
assign a0 = a[0];
assign b1 = b[1];
assign b0 = b[0];

// Equality using XNOR gates
assign eq1 = ~(a1 ^ b1);
assign eq0 = ~(a0 ^ b0);
assign a_equals_b = eq1 & eq0;

// Less Than
assign not_a1 = ~a1;
assign not_b1 = ~b1;
assign a_less_than_b = (not_a1 & b1) | (not_a1 & not_b1 & b0);

// Greater Than
assign not_b0 = ~b0;
assign a_greater_than_b = (a1 & not_b1) | (a0 & not_b0);

endmodule