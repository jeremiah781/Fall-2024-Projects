// Testbench for Two-Bit Comparator
//Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Simulates the Two-Bit Comparator module with various input combinations.

`timescale 1ns / 1ps

module tb_two_bit_comparator;

// Inputs
reg [1:0] a;
reg [1:0] b;

// Outputs
wire a_equals_b;
wire a_less_than_b;
wire a_greater_than_b;

// Instantiate the Two-Bit Comparator
two_bit_comparator uut (
    .a(a),
    .b(b),
    .a_equals_b(a_equals_b),
    .a_less_than_b(a_less_than_b),
    .a_greater_than_b(a_greater_than_b)
);

initial begin
    // Display header
    $display("a1 a0 | b1 b0 | eq | lt | gt");
    $display("----------------------------");
    
    // Test all possible combinations
    a = 2'b00; b = 2'b00; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b00; b = 2'b01; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b00; b = 2'b10; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b00; b = 2'b11; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b01; b = 2'b00; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b01; b = 2'b01; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b01; b = 2'b10; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b01; b = 2'b11; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b10; b = 2'b00; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b10; b = 2'b01; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b10; b = 2'b10; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b10; b = 2'b11; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b11; b = 2'b00; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b11; b = 2'b01; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b11; b = 2'b10; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    a = 2'b11; b = 2'b11; #10;
    $display("%b  %b | %b  %b | %b  | %b  | %b", a[1], a[0], b[1], b[0], a_equals_b, a_less_than_b, a_greater_than_b);
    
    $stop; // End simulation
end

endmodule