// tb_divisible_by_3_or_5.v
// Testbench for Divisible by 3 or 5 Module
// Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Tests the divisible_by_3_or_5 module by sweeping through all 4-bit values
//              and printing whether each value is divisible by 3 and/or 5.

`timescale 1ns/1ps
module tb_divisible_by_3_or_5;
    reg [3:0] in_word;
    wire div_by_3_o, div_by_5_o;
    
    // Instantiate the top-level module.
    divisible_by_3_or_5 uut (
        .in_word(in_word),
        .div_by_3_o(div_by_3_o),
        .div_by_5_o(div_by_5_o)
    );
    
    integer i;
    
    // Dump waveform data for RTL analysis
    initial begin
        $dumpfile("tb_divisible_by_3_or_5.vcd");
        $dumpvars(0, tb_divisible_by_3_or_5);
    end
    
    initial begin
        $display("Time | in_word | div_by_3 | div_by_5");
        for(i = 0; i < 16; i = i + 1) begin
            in_word = i;
            #5;
            $display("%4t | %b | %b | %b", $time, in_word, div_by_3_o, div_by_5_o);
        end
        $finish;
    end
endmodule