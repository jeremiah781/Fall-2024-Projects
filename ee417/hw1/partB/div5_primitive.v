// div5_primitive.v
// Divisible by 5 Primitive
// Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Checks if a 4-bit input is divisible by 5 by comparing it against known minterms.
// Note: Clear, modular code is something I picked up at Arm.

module div5_primitive(
    input  [3:0] word,
    output       div_by_5_o
);
    assign div_by_5_o = (~word[3] & ~word[2] & ~word[1] & ~word[0]) | // 0
                        (~word[3] &  word[2] & ~word[1] &  word[0]) | // 5
                        ( word[3] & ~word[2] &  word[1] & ~word[0]) | // 10
                        ( word[3] &  word[2] &  word[1] &  word[0]);   // 15
endmodule