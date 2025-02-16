// Testbench for Four-Bit Comparator
//Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Simulates the Four-Bit Comparator module with various input combinations.

`timescale 1ns/1ps
module tb_four_bit_comparator;
    reg [3:0] a;
    reg [3:0] b;
    wire eq, lt, gt;
    
    // Instantiate the Four-Bit Comparator
    four_bit_comparator uut (
        .a(a),
        .b(b),
        .a_equals_b(eq),
        .a_less_than_b(lt),
        .a_greater_than_b(gt)
    );
    
    integer i, j;
    
    initial begin
        $display("Time |   a    b   | eq lt gt");
        for (i = 0; i < 16; i = i + 1) begin
            for (j = 0; j < 16; j = j + 1) begin
                a = i;
                b = j;
                #5;
                $display("%4t | %b %b |  %b  %b  %b", $time, a, b, eq, lt, gt);
            end
        end
        $finish;
    end
endmodule
