# This test works on all source files *.v from src folder. Hierarchy is: project.v -> CPU_Core.v -> all other src .v files
# Those files need to be added to VERILOG_SOURCES in makefile
# TOPLEVEL is tb.v. tb.v is wrapper over project.v.

import cocotb, logging, operator
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadOnly, Timer


Register_values={0b000: 0,
                 0b001: 0,
                 0b010: 0,
                 0b011: 0,
                 0b100: 0,
                 0b101: 0,
                 0b110: 0,
                 0b111: 0
                 }

D_Mem_locations={0b0000: 0, 
                0b0001: 0, 
                0b0010: 0, 
                0b0011: 0,
                0b0100: 0, 
                0b0101: 0, 
                0b0110: 0, 
                0b0111: 0,
                0b1000: 0, 
                0b1001: 0, 
                0b1010: 0, 
                0b1011: 0,
                0b1100: 0, 
                0b1101: 0, 
                0b1110: 0, 
                0b1111: 0}

program={0: 0b0010_000_0_00000010, # LI r0, #2
         1: 0b0010_001_0_00000011, # LI r1, #3
         2: 0b0000_010_000_001_000, # ADD r2, r0, r1
         3: 0b0000_011_000_001_001, # SUB r3, r0, r1
         4: 0b0000_100_000_001_010, # AND r4, r0, r1
         5: 0b0000_100_000_001_011, # OR r4, r0, r1
         6: 0b0000_100_000_001_100, # XOR r4, r0, r1
         7: 0b0000_100_001_000_101, # SLL r4, r1, r0
         8: 0b0000_100_001_000_110, # SLR r4, r1, r0
         9: 0b0001_100_000_000111, # ADDI r4, r0, #7
         10: 0b1000_100_000_000010, # ANDI r4, r0, #2
         11: 0b1001_100_000_000100, # ORI r4, r0, #4
         12: 0b1010_100_000_000011, # XORI r4, r0, #3
         13: 0b1011_100_000_000001, # SLL r4, r0, #1
         14: 0b0001_100_000_000010, # SLR r4, r0, #2
         15: 0b0100_000_000_001_000, # SW r1, (r0 + #0) -- store number 3 from r1 into memloc 2 from r0 + #0 
         16: 0b0100_000_000_001_001, # SW r1, (r0 + #1) -- store number 3 from r1 into memloc 2 from r0 + #1 
         17: 0b0011_110_000_000000, # LW r6, (r0 + #0) -- load number 3 from r0 value memloc #2 + #0 into r6 
         18: 0b0011_111_000_000001, # LW r6, (r0 + #1) -- load number 3 from r0 value memloc #2 + #1 into r7 
         19: 0b0101_000_110_111_010, # BEQ r6, r7, #2 -- jump +2 to 21
         20: 0b0111_001_001_010_010, # BLT r6, r7, #10 -- jump +10 forward to 30 = halt
         21: 0b0110_111_000_001_111, # BNE r0, r1, #-1 -- jump -1 back to 20

         
         30: 0b1111_000_000_000_000, # NOP halt       
         }

R_opcode=0b0000
funct3_values={0b000: operator.add,
               0b001: operator.sub,
               0b010: operator.and_,
               0b011: operator.or_, 
               0b100: operator.xor,
               0b101: operator.lshift, 
               0b110: operator.rshift
               }


I_opcodes={0b0001: operator.add, 
           0b1000: operator.and_, 
           0b1001: operator.or_, 
           0b1010: operator.xor, 
           0b1011: operator.lshift, 
           0b1100: operator.rshift}

lw_opcode=0b0011
sw_opcode=0b0100


B_opcodes={0b0101: operator.eq, 
           0b0110: operator.ne, 
           0b0111: operator.lt}

LI_opcode=0b0010

NOP_opcode=0b1111
@cocotb.test()
async def End_To_End_test(dut):
    logger= logging.getLogger("cocotb")
    logger.info("Starting End-to-end test")
    c=Clock(dut.clk, 10, "ns")
    cocotb.start_soon(c.start())
    halt=0
    # INITIAL RESET 
    dut.rst_n.value=0
    await Timer(1,"ns")
    dut.rst_n.value=1
    await Timer(1,"ns")

    #PC=dut.uo_out.value.to_unsigned()
    PC=0
    while not halt:
        Instruction=program.get(PC)
        Instr_str=f"{Instruction:016b}"
        
        upper_byte = Instr_str[0:8]
        lower_byte  = Instr_str[8:16]
        
        dut.ui_in.value=int(upper_byte,2)
        dut.uio_in.value=int(lower_byte,2)

        # extract generic structures
        opcode = int(Instr_str[0:4], 2)
        rd     = int(Instr_str[4:7], 2)
        rs1    = int(Instr_str[7:10], 2)
        rs2    = int(Instr_str[10:13], 2)
        funct3 = int(Instr_str[13:16], 2)

        #extract imm8 for LI 
        imm8_raw = int(Instr_str[8:16], 2)
        imm8 = imm8_raw if imm8_raw < 128 else imm8_raw - 256
        
        # extract imm6 for I-type
        imm6_I_raw=int(Instr_str[10:16], 2)
        imm6_I = imm6_I_raw if imm6_I_raw < 32 else imm6_I_raw - 64

        # extract imm6 for SW/B format
        imm_gornji = int(Instr_str[4:7], 2)
        imm_donji = int(Instr_str[13:16], 2)
        imm6_SB_raw = (imm_gornji << 3) | imm_donji
        imm6_SB = imm6_SB_raw if imm6_SB_raw < 32 else imm6_SB_raw - 64

        # Initialization for expected values 
        expected_value = 0
        is_branch_inst = False
        branch_taken = False
        writeback_enabled = False
        mem_write_enabled = False
        
        if opcode == LI_opcode:
            expected_value = imm8 & 0xFF
            writeback_enabled = True
            
        elif opcode == R_opcode:
            val1 = Register_values.get(rs1, 0) & 0xFF
            val2 = Register_values.get(rs2, 0) & 0xFF
            if funct3 == 0b101 or funct3 == 0b110: # logic shifts
                val2 = val2 % 8
            op_func = funct3_values.get(funct3)
            expected_value = op_func(val1, val2) & 0xFF
            writeback_enabled = True
            
        elif opcode in I_opcodes.keys():
            val1 = Register_values.get(rs1, 0) & 0xFF
            if opcode == 0b1011 or opcode == 0b1100: # I-Type logic shifts
                imm6_I = imm6_I % 8
            op_func = I_opcodes.get(opcode)
            expected_value = op_func(val1, imm6_I) & 0xFF
            writeback_enabled = True
            
        elif opcode == lw_opcode:
            base = Register_values.get(rs1, 0) & 0xFF
            mem_addr = ((base + imm6_I) & 0xFF) & 0xF
            expected_value = D_Mem_locations.get(mem_addr, 0) & 0xFF
            writeback_enabled = True
            
        elif opcode == sw_opcode:
            base = Register_values.get(rs1, 0) & 0xFF
            val2 = Register_values.get(rs2, 0) & 0xFF
            mem_addr = ((base + imm6_SB) & 0xFF) & 0xF
            expected_value = 0 # result MUX for SW propagates 0 
            mem_write_enabled = True
            mem_write_val = val2
            
        elif opcode in B_opcodes.keys():
            val1 = Register_values.get(rs1, 0)
            val2 = Register_values.get(rs2, 0)
            op_func = B_opcodes.get(opcode)
            # Relational comparison for signed values
            if op_func(val1, val2):
                branch_taken = True
            
            # ALU calculates SUB for checking 
            sirovi_sub = (val1 - val2) & 0xFF
            expected_value = sirovi_sub if sirovi_sub < 128 else sirovi_sub - 256
            is_branch_inst = True
            
        elif opcode == NOP_opcode:
            
            halt=1
            continue

        # Transform expected CPU_out into signed form for comparison with .to_signed()
        if not is_branch_inst:
            expected_value = expected_value if expected_value < 128 else expected_value - 256
        
        logger.warning(f"PC je {PC}")

        await Timer(2, "ns") # async propagation through ALU/MUX
        
        # 2 stage cycle: 1st stage output is operation result, 2nd stage output is new pc adress

        #go from previous 2nd to 1st stage
        await RisingEdge(dut.clk)
        await ReadOnly()

        assert dut.uo_out.value.to_signed() == expected_value, f"RTL FAIL for PC {PC}: expected CPU_out {expected_value}, but got {dut.uo_out.value.to_signed()}"
        logger.warning(f"PC je {PC}")
        #go from 1st stage to 2nd stage to take new PC address
        await RisingEdge(dut.clk)
        await ReadOnly()
        PC=dut.uo_out.value.to_unsigned()
        logger.warning(f"PC je {PC}")
        # update python model
        if writeback_enabled:
            Register_values[rd] = expected_value
        
        if mem_write_enabled:
            D_Mem_locations[mem_addr] = mem_write_val
        await Timer(1,"ns")

        #print(Register_values)
        #print(D_Mem_locations)
        #print("\n")
    print(Register_values)
    print(D_Mem_locations)