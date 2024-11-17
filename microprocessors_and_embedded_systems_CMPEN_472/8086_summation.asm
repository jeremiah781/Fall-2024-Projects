                            ; (Microprocessors and Embedded Systems, CMPEN 472)
                          ; ===== 8086 Assembly Summation Program =====
                          ; Adds up all values of the numbers less than or equal to an integer.

.MODEL SMALL; Define memory model
.STACK 100h; Define stack size

         .DATA; Data segment
         NUMBERDW 0x 0020       ; The target number for summation (replace 0x0020 with your ID digits)
         SUM   DW 0       ; Variable to store the result

         .CODE; Code segment
START:
         MOV   AX, @DATA  ; Initialize Data Segment
         MOV   DS, AX

                          ; Initialize Registers
         MOV   CX, NUMBER ; Load CX with the target number
         MOV   BX, CX     ; Initialize loop counter in BX (optional, can use CX directly)
         MOV   AX, 0      ; Clear AX to accumulate the sum

SUM_LOOP:
         ADD   AX, CX     ; Add current value of CX to AX
         DEC   CX         ; Decrement CX
         JNZ   SUM_LOOP   ; Repeat loop if CX is not zero

                          ; Store the result
         MOV   DI, OFFSET SUM ; Load DI with the offset address of SUM
         MOV[DI] , AX       ; Store the sum in SUM

                          ; Terminate Program
         MOV   AH, 4Ch    ; DOS function to terminate program
         INT   21h        ; Call DOS interrupt

ENDSTART                                      ; End of program and specify the entry point
