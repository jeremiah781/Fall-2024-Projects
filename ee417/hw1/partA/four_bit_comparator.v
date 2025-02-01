// Four-Bit Comparator Design (with Two-Bit Comparator included)
// Author: Jeremiah Ddumba
// Date: 2025-01-30

`timescale 1ns/1ps

// Two-Bit Comparator Module
module two_bit_comparator (
    input  [1:0] a,
    input  [1:0] b,
    output       a_equals_b,
    output       a_less_than_b,
    output       a_greater_than_b
);
    // Behavioral implementation using relational operators.
    assign a_equals_b      = (a == b);
    assign a_less_than_b   = (a < b);
    assign a_greater_than_b = (a > b);
endmodule

// Four-Bit Comparator Module
module four_bit_comparator(
    input  [3:0] a,
    input  [3:0] b,
    output       a_equals_b,
    output       a_less_than_b,
    output       a_greater_than_b
);

    // Wires for results from the MSB comparator (bits [3:2])
    wire ms_eq, ms_lt, ms_gt;
    
    two_bit_comparator comp_high (
        .a(a[3:2]),
        .b(b[3:2]),
        .a_equals_b(ms_eq),
        .a_less_than_b(ms_lt),
        .a_greater_than_b(ms_gt)
    );
    
    // Wires for results from the LSB comparator (bits [1:0])
    wire ls_eq, ls_lt, ls_gt;
    
    two_bit_comparator comp_low (
        .a(a[1:0]),
        .b(b[1:0]),
        .a_equals_b(ls_eq),
        .a_less_than_b(ls_lt),
        .a_greater_than_b(ls_gt)
    );
    
    // Combine the results:
    // a equals b if both the MSB and LSB comparators report equality.
    assign a_equals_b = ms_eq & ls_eq;
    
    // a is less than b if:
    // - the MSB comparator indicates a < b, or
    // - the MSBs are equal and the LSB comparator indicates a < b.
    assign a_less_than_b = ms_lt | (ms_eq & ls_lt);
    
    // a is greater than b if:
    // - the MSB comparator indicates a > b, or
    // - the MSBs are equal and the LSB comparator indicates a > b.
    assign a_greater_than_b = ms_gt | (ms_eq & ls_gt);

endmodule