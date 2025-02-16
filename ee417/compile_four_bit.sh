#### 5. Compile the Verilog Files

Use the compile script to compile your Verilog modules and testbenches:

iverilog -o tb_four_bit_comp \
    Four-Bit\ Comparator\ Gate-Level\ Model.v \
    Two-Bit\ Comparator\ Gate-Level\ Model.v \
    Testbench\ for\ Four-Bit\ Comparator.v