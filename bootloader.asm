; 110 Baud = bit time 1152
; We will use 1200 baud = bit time 106


UPDDT	EQU	036Eh	; A register to data display
DELAY   EQU     05F1h   ; Counts down 16-bit DE register pair
WAIT	EQU	53	; Half Bit
IBTIM	EQU	106	; Whole Bit

	ORG 2000h


START:	LXI SP,2080h   ; Initialize stack pointer
	LXI H, 2800h	; We will use HL for pointer
			; Furthermore we will limit rw to the
			; 28xxh address space by only reading on byte
			; of address and one of data

LOOP:	CALL CI		; Get address byte
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
	LXI B, 8	; Count 8 bits
CI10:	LXI D, IBTIM	; Wait 1 bit
	CALL DELAY
	RIM		; Read SID
	RAL		; Shift into carry flag
	MOV A,B		; Move B to A
	RAR		; Roate 1 bit
	MOV B,A		; Move A to B
	DCR C		; Decrement bit count
	JNZ CI10	; Still more bits to get
	MOV A,B		; Move byte to A
	RET


