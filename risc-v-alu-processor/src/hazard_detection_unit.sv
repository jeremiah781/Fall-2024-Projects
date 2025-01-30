`timescale 1ns/1ps
module HazardDetectionUnit (
    input  logic        ID_EX_mem_read,
    input  logic [4:0]  ID_EX_rd,
    input  logic [4:0]  IF_ID_rs1,
    input  logic [4:0]  IF_ID_rs2,
    output logic        stall
);
    // Minimal placeholder: stall always deasserted
    assign stall = 1'b0;
endmodule