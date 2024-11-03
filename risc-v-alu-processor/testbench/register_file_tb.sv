// register_file_tb.sv
// Testbench for the Register File module
// started on 9/13/2024 and completed 9/17/2024

`timescale 1ns/1ps

module RegisterFile_tb;

    // Testbench Signals
    logic clk;
    logic reset;
    logic [4:0] read_reg1, read_reg2, write_reg;
    logic [31:0] write_data;
    logic reg_write;
    logic [31:0] read_data1, read_data2;

    // Instantiate the Register File
    RegisterFile uut (
        .clk(clk),
        .reset(reset),
        .read_reg1(read_reg1),
        .read_reg2(read_reg2),
        .write_reg(write_reg),
        .write_data(write_data),
        .reg_write(reg_write),
        .read_data1(read_data1),
        .read_data2(read_data2)
    );

    // Clock Generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // Toggle clock every 5 ns
    end

    // VCD Dumping for GTKWave
    initial begin
        $dumpfile("register_file_tb.vcd");
        $dumpvars(0, RegisterFile_tb);
    end

    // Test Procedure
    initial begin
        // Initialize Inputs
        reset = 1;
        read_reg1 = 5'd0;
        read_reg2 = 5'd0;
        write_reg = 5'd0;
        write_data = 32'd0;
        reg_write = 0;

        // Apply Reset
        #10;
        reset = 0;

        // Write to register x1
        #10;
        write_reg = 5'd1;
        write_data = 32'd100;
        reg_write = 1;

        // Disable writing
        #10;
        reg_write = 0;

        // Read from register x1
        #10;
        read_reg1 = 5'd1;
        read_reg2 = 5'd0;

        // Write to register x2
        #10;
        write_reg = 5'd2;
        write_data = 32'd200;
        reg_write = 1;

        // Disable writing
        #10;
        reg_write = 0;

        // Read from register x2
        #10;
        read_reg1 = 5'd2;
        read_reg2 = 5'd1;

        // Attempt to write to x0 (should have no effect)
        #10;
        write_reg = 5'd0;
        write_data = 32'd999;
        reg_write = 1;

        // Disable writing
        #10;
        reg_write = 0;

        // Read from register x0
        #10;
        read_reg1 = 5'd0;
        read_reg2 = 5'd0;

        // End Simulation
        #10;
        $display("All Register File tests completed.");
        $finish;
    end

endmodule
