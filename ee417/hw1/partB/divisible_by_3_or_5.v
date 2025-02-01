// divisible_by_3_or_5.v
// Divisible by 3 or 5 Top-Level Module
// Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Instantiates the div3_primitive and div5_primitive to check if a 4-bit input
//              is divisible by 3 or 5. The module outputs two flags accordingly.
// Note: Modular design makes the code reusable and easier to test—a lesson I learned at Arm.

module divisible_by_3_or_5(
    input  [3:0] in_word,
    output       div_by_3_o,
    output       div_by_5_o
);
    // Instantiate the Divisible by 3 primitive.
    div3_primitive div3_inst(
        .word(in_word),
        .div_by_3_o(div_by_3_o)
    );
    
    // Instantiate the Divisible by 5 primitive.
    div5_primitive div5_inst(
        .word(in_word),
        .div_by_5_o(div_by_5_o)
    );
endmodule