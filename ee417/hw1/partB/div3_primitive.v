// div3_primitive.v
// Divisible by 3 Primitive
// Author: Jeremiah Ddumba
// Date: 2025-01-30
// Description: Checks if a 4-bit input is divisible by 3 by comparing it against known minterms.
// Note: I learned a lot of these basics during my time at Arm.

module div3_primitive(
    input  [3:0] word,
    output       div_by_3_o
);
    assign div_by_3_o = (~word[3] & ~word[2] & ~word[1] & ~word[0]) | // 0
                        (~word[3] & ~word[2] &  word[1] &  word[0]) | // 3
                        (~word[3] &  word[2] &  word[1] & ~word[0]) | // 6
                        ( word[3] & ~word[2] & ~word[1] &  word[0]) | // 9
                        ( word[3] &  word[2] & ~word[1] & ~word[0]) | // 12
                        ( word[3] &  word[2] &  word[1] &  word[0]);   // 15
endmodule