; Final Project
; Ryan Buck
; Advent of Code, Day 7, 2024
; Bridge Repair - Part 2
; https://adventofcode.com/2024/day/7#part2

includelib shlwapi.lib

extrn ExitProcess : proc
extrn CreateFileA : proc
extrn ReadFile: proc
extrn CloseHandle: proc
extrn MessageBoxA : proc
extrn StrToInt64ExA : proc

.data
calibrationResult QWORD 0

currentLineStartIndex QWORD 0
currentLineLength QWORD 0
currentTestValue QWORD 0
currentOperandStartIndex QWORD 0
convertedInt QWORD 0

; File I/O
inputFile BYTE "input.txt",0
inputFD QWORD ?
numBytesRead QWORD ?
buffer BYTE 256 DUP(0)
bufferLen EQU ($ - buffer)
bufferNewDataIndex QWORD 0 ; where new data should start being written (past previous unprocessed data)
isFileReadingDone BYTE 0
carriageReturn BYTE 13

conversionBuffer BYTE 80 DUP(0)

outputWindowTitle BYTE "Calibration Result",0

.code
_main PROC
	sub rsp, 10h ; reserve for return and rbp
	sub rsp, 18h ; reserve for parameters
	sub rsp, 20h ; reserve shadow space

	call _openInputFile
	mov inputFD, rax

	process_equations:
		; Read from input and put into buffer
		mov rbx, bufferNewDataIndex
		mov ecx, bufferLen ; automatically zero extended
		sub rcx, rbx
		call _readInputFile
		mov isFileReadingDone, al

		; Parse line from buffer
		mov currentLineStartIndex, 0
		parse_lines:
			; Find line length
			mov rcx, currentLineStartIndex
			call _findLineLength
			cmp rax, -1
			je out_of_bytes
			mov currentLineLength, rax
			
			; Set end of line to space rather than carriage return (will make parsing easier later)
			lea rbx, [buffer]
			mov rcx, currentLineStartIndex
			add rcx, rax
			mov BYTE PTR [rbx + rcx], ' '

			; Find test value
			mov rcx, currentLineStartIndex
			mov rdx, rax ; line length
			call _findTestValue
			mov currentTestValue, rax

			; Check all operand combinations
			mov rcx, 0
			mov rdx, currentOperandStartIndex
			mov r8, currentLineStartIndex
			add r8, currentLineLength
			sub r8, rdx ; length of operands
			inc r8 ; include space at the end
			call _checkOperandCombinations
			cmp rax, 1
			jne no_combination

			; If an operand combination exists that produces the test value, add test value to calibration result
			mov rax, currentTestValue
			add calibrationResult, rax

			; Move to next line
			no_combination:
			mov rcx, currentLineLength
			mov rax, currentLineStartIndex
			add rax, rcx
			add rax, 2 ; skip null terminator and newline
			cmp rax, 256
			jle dont_clamp
			mov rax, 256 ; clamp so max value is 256
			dont_clamp:
			mov currentLineStartIndex, rax
			jmp parse_lines
		
		out_of_bytes:
			; Copy end of buffer to beginning
			mov rdx, currentLineStartIndex
			lea rsi, [buffer]
			lea rsi, [rsi + rdx]
			lea rdi, [buffer]
			mov ecx, bufferLen ; automatically zero extended
			sub rcx, rdx
			mov bufferNewDataIndex, rcx
			cld
			rep movsb

			; Fill buffer with zeros
			xor rax, rax
			mov al, 0
			mov rdx, bufferNewDataIndex
			lea rdi, [buffer]
			lea rdi, [rdi + rdx]
			mov ecx, bufferLen ; automatically zero extended
			sub rcx, rdx
			cld
			rep stosb

		; If there is still more left in the file, keep processing
		mov al, isFileReadingDone
		cmp al, 0
		je process_equations

	mov rcx, inputFD
	call CloseHandle

	mov rcx, calibrationResult
	lea rdx, conversionBuffer
	call _intToString

	; Show message box
	mov rcx, 0 ; no owner
	lea rdx, conversionBuffer ; calibration result
	lea r8, outputWindowTitle
	mov r9, 0 ; ok button
	call MessageBoxA

xor rcx, rcx
call ExitProcess
_main ENDP

; Convert a positive 64 bit integer to a string
; Arguments:
;	Positive integer
;	Write location
; Returns:
;	Length of int string
_intToString PROC
	push rbp
	push rbx
	push rdi
	mov rbp, rsp
	sub rsp, 20h

	mov rax, rcx ; int to convert
	mov rcx, 0 ; digit count
	mov rbx, 10 ; divisor
	mov rdi, rdx
	convert_digit:
		cqo
		div rbx

		add dl, 48 ; convert to character code
		push dx ; push digit
		inc rcx

		cmp rax, 0
		je done_converting
		jmp convert_digit

	done_converting:
		mov rdx, 0 ; buffer index
	write_digits:
		pop bx
		dec rcx
		
		mov BYTE PTR [rdi + rdx], bl
		inc rdx

		cmp rcx, 0
		jne write_digits

	mov BYTE PTR [rdi + rdx], 0 ; null terminate

	mov rax, rdx ; return length of int string

	mov rsp, rbp
	pop rdi
	pop rbx
	pop rbp
	ret
_intToString ENDP

; Check all operand combinations to see if any produce the test value
; Arguments:
;	Current total
;	Start index of remaining operands
;	Length of remaining operands
; Returns:
;	1 if a combination produces the test value, 0 otherwise
_checkOperandCombinations PROC
	push rbp
	push rbx
	push r12
	push r13
	push r14
	push rdi
	mov rbp, rsp
	sub rsp, 20h

	mov r12, rcx ; save current total

	; base condition
	cmp r8, 0
	je out_of_operands

	; there are operands left
	; find space
	xor rax, rax
	mov al, ' ' ; character to find
	lea rdi, [buffer]
	lea rdi, [rdi + rdx] ; start address of operands
	mov rbx, r8
	mov rcx, r8 ; counter value, original value also saved in rbx
	cld
	repnz scasb
	
	inc rcx
	sub rbx, rcx ; length of operand

	; convert operand from string to int
	mov r13, r8
	mov r14, rdx
	lea rcx, [buffer]
	lea rcx, [rcx + rdx] ; start of operand string
	push rcx
	mov BYTE PTR [rcx + rbx], 0 ; null terminate at space
	mov rdx, 0 ; default flags
	lea r8, convertedInt
	call StrToInt64ExA
	mov rax, convertedInt
	pop rcx
	mov BYTE PTR [rcx + rbx], ' ' ; reverse null terminate at space
	mov rdx, r14
	mov r8, r13

	; adjust operands start and length
	add rdx, rbx
	inc rdx ; skip space
	sub r8, rbx
	dec r8 ; skip space

	; check addition
	push rax
	push r8
	push rdx
	mov rcx, r12
	add rcx, rax
	call _checkOperandCombinations
	mov r13, rax
	pop rdx
	pop r8
	pop rax
	cmp r13, 1
	je combination_found

	; check multiplication
	push rax
	push r8
	push rdx
	mov rcx, r12
	imul rcx, rax
	call _checkOperandCombinations
	mov r13, rax
	pop rdx
	pop r8
	pop rax
	cmp r13, 1
	je combination_found

	; check concatenation
	push rax
	push r8
	push rdx
	push r8
	push rdx
	mov rcx, r12
	mov rdx, rax
	call _concatenateInts
	pop rdx
	pop r8
	mov rcx, rax
	call _checkOperandCombinations
	mov r13, rax
	pop rdx
	pop r8
	pop rax
	cmp r13, 1
	je combination_found

	jmp no_combination_found

	; check if combination produced the test value
	out_of_operands:
		mov rax, currentTestValue
		cmp rax, rcx
		jne no_combination_found

		; found a combination
		combination_found:
		mov rax, 1
		jmp operand_combination_done

	no_combination_found:
		mov rax, 0

	operand_combination_done:
	mov rsp, rbp
	pop rdi
	pop r14
	pop r13
	pop r12
	pop rbx
	pop rbp
	ret
_checkOperandCombinations ENDP

; Concatenate two positive integers
; Arguments:
;	First int
;	Second int
; Returns:
;	Concatenated int
_concatenateInts PROC
	push rbp
	push rbx
	push rdi
	push r12
	mov rbp, rsp
	sub rsp, 28h

	mov r12, rdx ; second int

	; first int already in rcx
	lea rdx, conversionBuffer
	call _intToString
	
	mov rcx, r12
	lea rdx, conversionBuffer
	add rdx, rax ; end of first int
	call _intToString

	; convert concatenated string back to int
	lea rcx, conversionBuffer
	mov rdx, 0 ; default flags
	lea r8, convertedInt
	call StrToInt64ExA
	mov rax, convertedInt

	mov rsp, rbp
	pop r12
	pop rdi
	pop rbx
	pop rbp
	ret
_concatenateInts ENDP

; Find the test value of a calibration equation in the buffer
; Arguments:
;	Start index of the equation
;	Length of the equation
; Returns:
;	The test value
_findTestValue PROC
	push rbp
	push rbx
	push r12
	push rdi
	mov rbp, rsp
	sub rsp, 28h

	mov r12, rcx ; save start index

	; find the colon
	xor rax, rax
	mov al, ':' ; character to find
	lea rdi, [buffer]
	lea rdi, [rdi + r12] ; start address of equation
	mov rbx, rdx
	mov rcx, rdx ; counter value, original value also saved in rbx
	cld
	repnz scasb

	; calculate number of indices to colon
	inc rcx
	sub rbx, rcx
	
	; convert test value to integer
	lea rcx, [buffer]
	lea rcx, [rcx + r12] ; start of test value string
	mov BYTE PTR [rcx + rbx], 0 ; null terminate at colon
	mov rdx, 0 ; default flags
	lea r8, convertedInt
	call StrToInt64ExA
	mov rax, convertedInt

	; Save operand start index
	add rbx, r12
	add rbx, 2 ; skip colon and space
	mov currentOperandStartIndex, rbx

	mov rsp, rbp
	pop rdi
	pop r12
	pop rbx
	pop rbp
	ret
_findTestValue ENDP

; Find the length of a line in the buffer
; Arguments:
;	Line start index
; Returns:
;	The length of the line (-1 if line ending not found)
_findLineLength PROC
	push rbp
	push rbx
	push rdx
	push rdi
	mov rbp, rsp
	sub rsp, 20h

	xor rax, rax
	mov al, carriageReturn ; character to find
	lea rdi, [buffer]
	lea rdi, [rdi + rcx] ; start address of line
	mov ebx, bufferLen ; automatically zero extended
	sub rbx, rcx
	mov rcx, rbx ; counter value (original value also saved in rbx)
	cld
	repnz scasb

	; return number of indices scanned until newline was found, or -1 if not found
	jz newline_found
	mov rax, -1
	jmp no_newline

	newline_found:
		inc rcx
		sub rbx, rcx
		mov rax, rbx
	no_newline:

	mov rsp, rbp
	pop rdi
	pop rdx
	pop rbx
	pop rbp
	ret
_findLineLength ENDP

; Read a chunk from the input file
; Arguments:
;	Number of bytes to read
; Returns:
;	1 if done reading, 0 if more to read
_readInputFile PROC
	push rbp
	push rbx
	push r12
	mov rbp, rsp
	sub rsp, 28h

	mov r12, rcx ; save num bytes to read

	mov rcx, inputFD ; input file
	lea rdx, buffer
	mov rbx, bufferNewDataIndex
	lea rdx, [rdx + rbx] ; buffer address (after previous unprocessed data)
	mov r8, r12 ; num bytes to read
	lea r9, numBytesRead ; num bytes that were read
	mov QWORD PTR [rsp + 20h], 0 ; no overlap
	call ReadFile

	; Return 1 if done reading, 0 if theres still more to read
	cmp r12, numBytesRead
	jne done_reading
	mov rax, 0
	jmp still_reading
	
	done_reading:
		mov rax, 1
		; add carriage return to end of buffer to help with parsing later
		lea rdx, buffer
		mov r9, bufferNewDataIndex
		add r9, numBytesRead
		mov bl, carriageReturn
		mov BYTE PTR [rdx + r9], bl
	still_reading:

	mov rsp, rbp
	pop r12
	pop rbx
	pop rbp
	ret
_readInputFile ENDP

; Open the input file
; Arguments: None
; Returns:
;	Input file descriptor
_openInputFile PROC
	push rbp
	mov rbp, rsp
	sub rsp, 30h

	lea rcx, inputFile ; file name
	mov rdx, 80000000h ; open with read access
	mov r8, 0 ; no share
	mov r9, 0 ; no security
	mov QWORD PTR [rsp + 20h], 3 ; open existing file
	mov QWORD PTR [rsp + 28h], 80h ; normal file attributes
	mov QWORD PTR [rsp + 30h], 0 ; no template
	call CreateFileA

	mov rsp, rbp
	pop rbp
	ret
_openInputFile ENDP

END