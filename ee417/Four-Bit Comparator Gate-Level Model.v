// Four-Bit Comparator Gate-Level Model
//Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Compares two 4-bit inputs using two two-bit comparator modules and outputs equality, less than, and greater than signals.

module four_bit_comparator (
    input [3:0] a,          // 4-bit input a
    input [3:0] b,          // 4-bit input b
    output a_equals_b,      // Output high if a equals b
    output a_less_than_b,   // Output high if a < b
    output a_greater_than_b // Output high if a > b
);

// Wires for higher and lower two-bit comparisons
wire eq_high, lt_high, gt_high;
wire eq_low, lt_low, gt_low;

// Instantiate two two-bit comparators
two_bit_comparator cmp_high (
    .a(a[3:2]),
    .b(b[3:2]),
    .a_equals_b(eq_high),
    .a_less_than_b(lt_high),
    .a_greater_than_b(gt_high)
);

two_bit_comparator cmp_low (
    .a(a[1:0]),
    .b(b[1:0]),
    .a_equals_b(eq_low),
    .a_less_than_b(lt_low),
    .a_greater_than_b(gt_low)
);

// Combine the outputs based on hierarchical comparison
assign a_equals_b = eq_high & eq_low;
assign a_less_than_b = lt_high | (eq_high & lt_low);
assign a_greater_than_b = gt_high | (eq_high & gt_low);

endmodule