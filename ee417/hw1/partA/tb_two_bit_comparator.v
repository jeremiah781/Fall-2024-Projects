// Testbench for Two-Bit Comparator
// Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Simulates the Two-Bit Comparator module with various input combinations.

`timescale 1ns/1ps
module tb_two_bit_comparator;
    reg [1:0] a;
    reg [1:0] b;
    wire eq, lt, gt;
    
    // Instantiate the Two-Bit Comparator
    two_bit_comparator uut (
        .a(a),
        .b(b),
        .a_equals_b(eq),
        .a_less_than_b(lt),
        .a_greater_than_b(gt)
    );
    
    integer i, j;
    
    initial begin
        // Set up the dump file and dump variables for waveform viewing
        $dumpfile("dump.vcd");
        $dumpvars(0, tb_two_bit_comparator);
        
        $display("Time |  a   b   | eq lt gt");
        for (i = 0; i < 4; i = i + 1) begin
            for (j = 0; j < 4; j = j + 1) begin
                a = i;
                b = j;
                #10;  // Wait for signals to propagate
                $display("%4t | %b %b |  %b  %b  %b", $time, a, b, eq, lt, gt);
            end
        end
        $finish;
    end
endmodule