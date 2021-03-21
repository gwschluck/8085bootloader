; 110 Baud = bit time 1152
; We will use 1200 baud = bit time 106
; This bootloader useis 16-bit addressing`
; It expects 16 bits of address followed by 8 bits of data


UPDDT	EQU	036Eh	; A register to data display
DELAY   EQU     05F1h   ; Counts down 16-bit DE register pair
WAIT	EQU	53	; Half Bit
IBTIM	EQU	106	; Whole Bit
SSP	EQU	LI+8	; Stack initiatized as 8 past last instruction

	ORG 2000h


START:	LXI SP,SSP   ; Initialize stack pointer

LOOP:	CALL CI		; Get high order address byte
	MOV H,A		; Put in high order address byte of pointer
	CALL CI		; Get low order address byte
	MOV L,A		; Put in low order address byte of pointer
	CALL CI		; Get data byte
	MOV M,A
	JMP LOOP	; Loop
CI:	RIM		; Read SID
	RAL		; Shift to carry flag
	JNC CI		; Wait for idle input line
CI05:	RIM		; READ SID
	RAL		; Shift to carry flag
	JC CI05		; Wait for start bit
	LXI D, WAIT	; Delay half bit
	CALL DELAY	
	MVI C, 8  	; Count 8 bits, no need to initiatize B
CI10:	MVI E, IBTIM	; Wait 1 bit - 8 bits - fits into E only
	CALL DELAY
	RIM		; Read SID
	RAL		; Shift into carry flag
	MOV A,B		; Move B to A
	RAR		; Roate 1 bit
	MOV B,A		; Move A to B
	DCR C		; Decrement bit count
	JNZ CI10	; Still more bits to get
	MOV A,B		; Move byte to A
LI:	RET


