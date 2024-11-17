                          ; (Microprocessors and Embedded Systems, CMPEN 472)
                          ; ===== 6502 Assembly Checksum Program =====

         .org $0600; Program starting address

START:
                          ; ----- Preload Memory Locations $00 through $1F -----
         LDX   #$00       ; Initialize X register to 0

PRELOAD_LOOP:
         STX   $00,X      ; Store X at memory location $00 + X
         INX              ; Increment X
         CPX   #$20       ; Compare X with $20 (32 in decimal)
         BNE   PRELOAD_LOOP ; If X != $20, repeat the loop

                          ; ----- Initialize Checksum Variables -----
         LDA   #$00
         STA   CHECKSUM_LO ; Set CHECKSUM_LO to 0
         STA   CHECKSUM_HI ; Set CHECKSUM_HI to 0

                          ; ----- Calculate Checksum -----
         LDX   #$00       ; Reset X register to 0

SUM_LOOP:
         CLC              ; Clear carry flag before addition
         LDA   CHECKSUM_LO ; Load current CHECKSUM_LO
         ADC   $00,X      ; Add value at memory location $00 + X
         STA   CHECKSUM_LO ; Store result back to CHECKSUM_LO

         LDA   CHECKSUM_HI ; Load current CHECKSUM_HI
         ADC   #$00       ; Add carry from previous addition
         STA   CHECKSUM_HI ; Store result back to CHECKSUM_HI

         INX              ; Increment X
         CPX   #$20       ; Compare X with $20
         BNE   SUM_LOOP   ; If X != $20, repeat the loop

                          ; ----- Store Checksum in Locations $20 (HI) and $21 (LO) -----
         LDA   CHECKSUM_HI ; Load high byte of checksum
         STA   $20        ; Store at memory location $20
         LDA   CHECKSUM_LO ; Load low byte of checksum
         STA   $21        ; Store at memory location $21

                          ; ----- End of Program -----
BRK;     Break - endof program

                          ; ----- Variable Definitions -----
CHECKSUM_LO =     $FE        ; Zero-page address for checksum low byte
CHECKSUM_HI =     $FF        ; Zero-page address for checksum high byte

                          ; ----- Reset Vector -----
         .org $FFFC; Reset vector location
         .word START; Set reset vector to START label
