                          ; 6502 Assembly Multiplication Program
                          ; (Microprocessors and Embedded Systems, CMPEN 472)

                          ; ----- Zero-Page Variable Definitions -----
         .ORG $0000; Zero-page starts at $0000

OPER_A:  .DB 0; Operand A input at $0000
OPER_B:  .DB 0; Operand B input at $0001
MULTI:   .DB 0; Operand A for multiplication at $0002
MULTI_CNT: .DB 0; Operand B (counter) at $0003
PROD_LO: .DB 0; Low byte of Product at $0004
PROD_HI: .DB 0; High byte of Product at $0005

                          ; ----- Program Code -----
         .ORG $8000; Starting address of the program in memory

START:
                          ; Initialize Product to 0
         LDA   #$00
         STA   PROD_LO    ; Low byte of Product
         STA   PROD_HI    ; High byte of Product

                          ; Load Operands into Zero-Page
         LDA   OPER_A
         STA   MULTI
         LDA   OPER_B
         STA   MULTI_CNT

                          ; Check if Multiplier is Zero
         LDA   MULTI_CNT
         BEQ   MUL_DONE

MUL_LOOP:
                          ; Add Multiplicand to Product
         CLC
         LDA   PROD_LO
         ADC   MULTI
         STA   PROD_LO

                          ; Handle Carry to High Byte
         LDA   PROD_HI
         ADC   #$00
         STA   PROD_HI

                          ; Decrement Loop Counter
         LDA   MULTI_CNT
         SEC
         SBC   #$01
         STA   MULTI_CNT

                          ; Check if Counter is Zero
         BNE   MUL_LOOP

MUL_DONE:
                          ; End of Program


                          ; ----- Reset Vector -----
         .ORG $FFFC; Reset/Interrupt Vector
         .DW START; Set Reset Vector to start of program
