// register_file.sv
// This module represents the Register File in a RISC-V processor
// It contains 32 general-purpose registers, each 32 bits wide
// started on 9/10/2024 and completed 9/17/2024

module RegisterFile (
    input  logic        clk,         // Clock signal for synchronous writes
    input  logic        reset,       // Reset signal to initialize registers
    input  logic [4:0]  read_reg1,   // Address of the first register to read
    input  logic [4:0]  read_reg2,   // Address of the second register to read
    input  logic [4:0]  write_reg,   // Address of the register to write to
    input  logic [31:0] write_data,  // Data to write into the register
    input  logic        reg_write,   // Control signal to enable writing
    output logic [31:0] read_data1,  // Data read from the first register
    output logic [31:0] read_data2   // Data read from the second register
);

    parameter REG_COUNT   = 32;
    parameter ASYNC_READ  = 0;
    parameter CHECK_WB    = 0;

    // Declare an array of 32 registers, each 32 bits wide
    logic [31:0] registers [REG_COUNT];

    // Handle asynchronous read operations
    // Register x0 is always zero in RISC-V, so override its value
    assign read_data1 = (read_reg1 != 5'd0) ? registers[read_reg1] : 32'd0;
    assign read_data2 = (read_reg2 != 5'd0) ? registers[read_reg2] : 32'd0;

    // Integrate optional asynchronous read
    always_comb begin
        if (ASYNC_READ) begin
            read_data1 = registers[read_reg1];
            read_data2 = registers[read_reg2];
        end else begin
            // Register x0 is always zero in RISC-V, so override its value
            read_data1 = (read_reg1 != 5'd0) ? registers[read_reg1] : 32'd0;
            read_data2 = (read_reg2 != 5'd0) ? registers[read_reg2] : 32'd0;
        end
    end

    // Handle synchronous write operations
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            // On reset, initialize all registers to zero
            integer i; // Loop variable
            for (i = 0; i < REG_COUNT; i++) begin
                registers[i] <= 32'd0;
            end
        end else if (reg_write && (write_reg != 5'd0)) begin
            // If writing is enabled and not writing to x0, perform the write
            registers[write_reg] <= write_data;
        end
        // Note: Writing to x0 has no effect since it's always zero
    end

    // Optional write-back check
    always_ff @(posedge clk) begin
        if (reg_write) begin
            if (CHECK_WB && (read_reg1 == write_reg || read_reg2 == write_reg)) begin
                // Add debug or verification logic here
            end
        end
    end

endmodule
