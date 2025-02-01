// Two-Bit Comparator Gate-Level Model
// Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Compares two 2-bit inputs and outputs equality, less than, and greater than signals.

// -----------------------------------------------------------------------------
// Module: two_bit_comparator
// Description: Gate-level implementation of a Two-Bit Comparator.
//              Compares two 2-bit numbers (a and b) and outputs:
//              - a_equals_b  : High when a == b
//              - a_less_than_b: High when a < b
//              - a_greater_than_b: High when a > b
//
// Truth Table:
//  a1 a0 | b1 b0 || a_equals_b | a_less_than_b | a_greater_than_b
// ---------------------------------------------------------------
//  0  0 |  0  0 ||      1     |       0       |         0
//  0  0 |  0  1 ||      0     |       1       |         0
//  0  0 |  1  0 ||      0     |       1       |         0
//  0  0 |  1  1 ||      0     |       1       |         0
//  0  1 |  0  0 ||      0     |       0       |         1
//  0  1 |  0  1 ||      1     |       0       |         0
//  0  1 |  1  0 ||      0     |       1       |         0
//  0  1 |  1  1 ||      0     |       1       |         0
//  1  0 |  0  0 ||      0     |       0       |         1
//  1  0 |  0  1 ||      0     |       0       |         1
//  1  0 |  1  0 ||      1     |       0       |         0
//  1  0 |  1  1 ||      0     |       1       |         0
//  1  1 |  0  0 ||      0     |       0       |         1
//  1  1 |  0  1 ||      0     |       0       |         1
//  1  1 |  1  0 ||      0     |       0       |         1
//  1  1 |  1  1 ||      1     |       0       |         0
// -----------------------------------------------------------------------------

module two_bit_comparator(
    input  [1:0] a,
    input  [1:0] b,
    output       a_equals_b,
    output       a_less_than_b,
    output       a_greater_than_b
);

    // Intermediate signals for bit-level equality:
    // eq1 is true when the most significant bits are equal.
    // eq0 is true when the least significant bits are equal.
    wire eq1, eq0;
    
    // Bitwise XNOR for each bit:
    assign eq1 = (a[1] & b[1]) | (~a[1] & ~b[1]);  // a1 XNOR b1
    assign eq0 = (a[0] & b[0]) | (~a[0] & ~b[0]);  // a0 XNOR b0
    
    // a equals b when both corresponding bits are equal.
    assign a_equals_b = eq1 & eq0;
    
    // a is less than b if either:
    // - a[1] is 0 and b[1] is 1, or
    // - the MSBs are equal (eq1) and a[0] is 0 while b[0] is 1.
    assign a_less_than_b = (~a[1] & b[1]) | (eq1 & (~a[0] & b[0]));
    
    // a is greater than b if either:
    // - a[1] is 1 and b[1] is 0, or
    // - the MSBs are equal (eq1) and a[0] is 1 while b[0] is 0.
    assign a_greater_than_b = (a[1] & ~b[1]) | (eq1 & (a[0] & ~b[0]));

endmodule
