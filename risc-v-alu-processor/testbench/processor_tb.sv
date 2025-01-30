`timescale 1ns/1ps

module Processor_tb;
    // Testbench Signals
    logic clk;
    logic reset;
    logic interrupt;
    logic [31:0] regfile_ref [31:0];  // Reference model registers

    // Debug signals
    logic pipeline_stall_dbg;
    logic pipeline_flush_dbg;

    // Instantiate the Processor
    Processor uut (
        .clk(clk),
        .reset(reset),
        .interrupt(interrupt),
        .pipeline_stall_dbg(pipeline_stall_dbg),
        .pipeline_flush_dbg(pipeline_flush_dbg)
    );

    // Clock Generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    // Test stimulus and monitoring
    initial begin
        // Initialize signals
        reset = 1;
        interrupt = 0;
        
        // Initialize reference model
        for (int i = 0; i < 32; i++) begin
            regfile_ref[i] = 32'h0;
        end

        // Setup waveform dumping
        $dumpfile("processor_tb.vcd");
        $dumpvars(0, Processor_tb);

        // Apply reset
        #10 reset = 0;

        // Wait for processor initialization
        #10;

        // Monitor message
        $display("Time: %0t - Starting processor execution", $time);

        // Begin monitoring key signals
        $monitor("Time: %0t | PC: %0h | Stall: %b | Flush: %b",
                 $time, uut.PC, pipeline_stall_dbg, pipeline_flush_dbg);

        // Test sequence
        repeat(5) @(posedge clk);  // Wait 5 clock cycles

        // Inject interrupt
        interrupt = 1;
        #10 interrupt = 0;

        // Continue execution
        repeat(15) @(posedge clk);

        // Check results
        check_results();

        // End simulation
        #100;
        $display("Simulation Completed at time %0t", $time);
        $finish;
    end

    // Task to check results
    task check_results;
        begin
            // Add specific result checking logic here
            if (uut.PC === 32'h0) begin
                $display("ERROR: PC should not be zero at this point");
            end
            // Add more checks as needed
        end
    endtask

    // Simple result checking at each clock edge
    always @(posedge clk) begin
        if (!reset && uut.regfile.reg_write) begin
            // Update reference model when write occurs
            regfile_ref[uut.regfile.write_reg] <= uut.regfile.write_data;
            
            // Log register writes
            $display("Time: %0t - Register x%0d written with value %0h",
                    $time, uut.regfile.write_reg, uut.regfile.write_data);
        end
    end

endmodule