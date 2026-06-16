#This test works on source files: Registers.v, ALU.v, Control_Unit.v, Imm_Gen.v, Data_Memory.v, Branch_Control.v
#and 2 Muxes.v instances
#Those files need to be added to VERILOG_SOURCES in makefile
#TOPLEVEL is Datapath_Wrapper.v


import cocotb, logging, operator, random
from cocotb.triggers import RisingEdge, Timer, ReadOnly
from cocotb.clock import Clock

R_opcode=0b0000

funct3_values={0b000: operator.add,
               0b001: operator.sub,
               0b010: operator.and_,
               0b011: operator.or_, 
               0b100: operator.xor,
               0b101: operator.lshift, 
               0b110: operator.rshift
               }

Register_values={0b000: 0,
                 0b001: 0,
                 0b010: 0,
                 0b011: 0,
                 0b100: 0,
                 0b101: 0,
                 0b110: 0,
                 0b111: 0}

Register_dummy_values={0b000: 1,
                          0b001: 127,
                          0b010: 2,
                          0b011: 24,
                          0b100: 0,
                          0b101: -4,
                          0b110: -49,
                          0b111: -128}


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

D_Mem_original_values={0b0000: 0, 
                0b0001: 1, 
                0b0010: 2, 
                0b0011: 3,
                0b0100: 4, 
                0b0101: 5, 
                0b0110: 6, 
                0b0111: 7,
                0b1000: 8, 
                0b1001: 9, 
                0b1010: 10, 
                0b1011: 11,
                0b1100: 12, 
                0b1101: 13, 
                0b1110: 14, 
                0b1111: 15}


@cocotb.test()
async def Datapath_R_Type_Test(dut):
    logger= logging.getLogger("cocotb")
    logger.info("Starting R-Type test")
    c=Clock(dut.clk, 10, "ns")
    cocotb.start_soon(c.start())
    
    # INITIAL RESET 
    dut.rst.value=1
    await Timer(1,"ns")
    dut.rst.value=0
    
    # SET DUMMY REG VALUES BOTH IN PYTHON AND DUT
    for key,val in Register_dummy_values.items():
        Register_values[key]=val
        dut.Registers.Regs.__getitem__(key).value=val

    for i in range(500):
        # random instrukcija
        funct3=random.choice(list(funct3_values.keys() ))
        rs1=random.randint(0,7)
        rs2=random.randint(0,7)
        rd=random.randint(0,7)
        

        val1=Register_values.get(rs1)
        val2=Register_values.get(rs2)
        if funct3==0b101 or funct3==0b110:
            val2=val2 % 8
            val1=val1 & 0xFF
        obtain_operator=funct3_values.get(funct3)
        expected_result=obtain_operator(val1, val2) & 0xFF

        instruction_word=f"{R_opcode:04b}{rd:03b}{rs1:03b}{rs2:03b}{funct3:03b}"
        dut.Instruction.value=int(instruction_word,2)

        await Timer(1,"ns")
        assert dut.CPU_Out.value==expected_result, f"Failed for funct3: {funct3}, Rs1: {rs1}, Rs2: {rs2}, Rd: {rd}, Regs_value: {Register_values}. Expected CPU_Out to be {expected_result}, but got {dut.CPU_Out.value.to_unsigned()}"

        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.Registers.Regs.__getitem__(rd).value==expected_result, f"Failed for funct3: {funct3}, Rs1: {rs1}, Rs2: {rs2}, Rd: {rd}. Expected writeback to be {expected_result}, but got {dut.Registers.Regs.__getitem__(rd).value.to_unsigned()}"
        await Timer(1, "ns")

        Register_values.update({rd: expected_result})

        # REFRESH BOTH PYTHON REGS AND DUT REGS WITH INITIAL VALUES
        if i %30 == 1:
            for key,val in Register_dummy_values.items():
                Register_values[key] = val
                dut.Registers.Regs.__getitem__(key).value=val
            await Timer(1,"ns")


    # RESET REGS BOTH IN PYTHON AND DUT
    for key,val in Register_dummy_values.items():
        Register_values[key] = 0
    dut.rst.value=1
    await Timer(1,"ns")
    dut.rst.value=0    






@cocotb.test()
async def Datapath_I_Type_Test(dut):
   
    logger= logging.getLogger("cocotb")
    logger.info("Starting I-Type test")
    c=Clock(dut.clk, 10, "ns")
    cocotb.start_soon(c.start())


    # SET DUMMY REG VALUES BOTH IN PYTHON AND DUT
    for key,val in Register_dummy_values.items():
        Register_values[key]=val
        dut.Registers.Regs.__getitem__(key).value=val


    for i in range(500):
        opcode=random.choice(list(I_opcodes.keys()))
        rs1=random.randint(0,7)
        rd=random.randint(0,7)
        if opcode in (0b1011,0b1100):
            imm6=random.randint(0,7)
        else:
            imm6=random.randint(-32,31)
        

        val1=Register_values.get(rs1) & 0xFF
        
        obtain_operator=I_opcodes.get(opcode)
        expected_result=obtain_operator(val1, imm6) & 0xFF

        instruction_word=f"{opcode:04b}{rd:03b}{rs1:03b}{(imm6 & 0x3f):06b}"
        dut.Instruction.value=int(instruction_word,2)

        await Timer(1,"ns")
        assert dut.CPU_Out.value==expected_result, f"Failed for opcode: {opcode}, Rs1: {rs1}, Rd: {rd}, imm6: {imm6} , Regs_value: {Register_values}. Expected CPU_Out to be {expected_result}, but got {dut.CPU_Out.value.integer}"

        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.Registers.Regs.__getitem__(rd).value==expected_result, f"Failed for opcode: {opcode}, Rs1: {rs1}, Rd: {rd}, imm6: {imm6} , Regs_value: {Register_values}. Expected writeback to be {expected_result}, but got {dut.Registers.Regs.__getitem__(rd).value.integer}"
        await Timer(1, "ns")

        Register_values.update({rd: expected_result})

        # REFRESH BOTH PYTHON REGS AND DUT REGS WITH INITIAL VALUES
        if i %30 == 1:
            for key,val in Register_dummy_values.items():
                Register_values[key] = val
                dut.Registers.Regs.__getitem__(key).value=val
            await Timer(1,"ns")

    # RESET REGS BOTH IN PYTHON AND DUT
    for key,val in Register_dummy_values.items():
        Register_values[key] = 0
    dut.rst.value=1
    await Timer(1,"ns")
    dut.rst.value=0



    # LW_test

    # DUMMY D_MEM VALUES INSERTED INTO DUT AND PYTHON
    for loc, val in D_Mem_original_values.items():
        dut.data_memory.memory.__getitem__(loc).value=val;
        D_Mem_locations[loc]=val


    for i in range(500):
        
        rd=random.randint(0,7)
        rs1=random.randint(0,7)
        imm6=random.randint(-32,31)

        base=Register_values.get(rs1)
        
        expected_result=D_Mem_locations.get( (base+imm6) & 0xF ) 

        instruction_word=f"{lw_opcode:04b}{rd:03b}{rs1:03b}{(imm6 & 0x3f):06b}"
        dut.Instruction.value=int(instruction_word,2)

        await Timer(1,"ns")
        assert dut.CPU_Out.value==expected_result, f"Failed for lw iteracija: {i},  Rs1: {rs1}, Rd: {rd}, imm6: {imm6} , Regs_value: {Register_values} , D_Mem_values: {D_Mem_locations}. Expected CPU_Out to be {expected_result}, but got {dut.CPU_Out.value.integer}"

        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.Registers.Regs.__getitem__(rd).value==expected_result, f"Failed for lw iteracija: {i}, Rs1: {rs1}, Rd: {rd}, imm6: {imm6} , Regs_value: {Register_values} , D_Mem_values: {D_Mem_locations}. Expected writeback to be {expected_result}, but got {dut.Registers.Regs.__getitem__(rd).value.integer}"
        await Timer(1, "ns")
        Register_values.update({rd: expected_result})

    # RESET REGS BOTH IN PYTHON AND DUT
    for key,val in Register_dummy_values.items():
        Register_values[key] = 0
    dut.rst.value=1
    await Timer(1,"ns")
    dut.rst.value=0






@cocotb.test()
async def Datapath_LI_Type_Test(dut):
    logger= logging.getLogger("cocotb")
    logger.info("Starting LI-Type test")
    c=Clock(dut.clk, 10, "ns")
    cocotb.start_soon(c.start())
    
    #load imm --- rd=imm8
    for i in range(500):
        rd=random.randint(0,7)
        imm8=random.randint(-128,127)

        instruction_word=f"{LI_opcode:04b}{rd:03b}{(imm8 & 0xFF):09b}"
        dut.Instruction.value=int(instruction_word,2)
        expected_result=imm8 & 0xFF
        
        await Timer(1,"ns")
        assert dut.CPU_Out.value==expected_result, f"Failed for li iteracija: {i}, Rd: {rd}, imm8: {imm8} , Regs_value: {Register_values}. Expected CPU_Out to be {expected_result}, but got {dut.CPU_Out.value.integer}"

        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.Registers.Regs.__getitem__(rd).value==expected_result, f"Failed for lw iteracija: {i}, Rd: {rd}, imm8: {imm8} , Regs_value: {Register_values} . Expected writeback to be {expected_result}, but got {dut.Registers.Regs.__getitem__(rd).value.integer}"
        await Timer(1, "ns")
        Register_values.update({rd: expected_result})
    #print(D_Mem_locations)

    # RESET REGS BOTH IN PYTHON AND DUT AND RESET D_MEM IN DUT
    for key,val in Register_dummy_values.items():
        Register_values[key] = 0
    dut.rst.value=1
    await Timer(1,"ns")
    dut.rst.value=0




@cocotb.test()
async def Datapath_SB_Type_Test(dut):
    logger= logging.getLogger("cocotb")
    logger.info("Starting SB-Type test")
    c=Clock(dut.clk, 10, "ns")
    cocotb.start_soon(c.start())


    # SET DUMMY REG VALUES BOTH IN PYTHON AND DUT
    for key,val in Register_dummy_values.items():
        dut.Registers.Regs.__getitem__(key).value=val
        Register_values[key]=val

    #D_MEM LOCATIONS IN DUT HAVE BEEN RESET SO LOAD BACK
    for key,val in D_Mem_original_values.items():
        dut.data_memory.memory.__getitem__(key).value=val
    
    #D_MEM LOCATIONS IN PYTHON PERSIST FROM LW-TEST

    await Timer(1,"ns")
    for i in range(16):
        assert dut.data_memory.memory.__getitem__(i).value.to_unsigned()==D_Mem_locations.get(i), f"DATA_MEMORY FAIL: iter:{i}, lokacija je: {dut.data_memory.memory.__getitem__(i).value.to_unsigned()}"


    for i in range(500):
        rs1=random.randint(0,7)
        rs2=random.randint(0,7)

        imm6=random.randint(-32,31)
        imm6_cut= imm6 & 0x3F
        imm_upper3=(imm6_cut>>3) & 0x7
        imm_lower3=imm6_cut & 0x7
        
        base=Register_values.get(rs1)
        val2=Register_values.get(rs2)

        
        mem_location=(base+imm6) & 0xF
        

        instruction_word=f"{sw_opcode:04b}{imm_upper3:03b}{rs1:03b}{rs2:03b}{imm_lower3:03b}"
        dut.Instruction.value=int(instruction_word,2)
        
        await RisingEdge(dut.clk)
        await ReadOnly()

        assert dut.data_memory.memory.__getitem__(mem_location).value.to_signed()==val2, f"Failed for lw iteracija: {i}, Rs2: {rs2}, Rs1:{rs1}, imm6: {imm6} , Regs_value: {Register_values}, D_Mem_values: {D_Mem_locations} . Expected value to be {val2}, but got {dut.data_memory.memory[mem_location].value.to_signed()}"
        await Timer(1,"ns")
        D_Mem_locations.update({mem_location:val2})
    print(D_Mem_locations)



    #B_TEST
    print(Register_values)
    for i in range(500):
        rs1=random.randint(0,7)
        rs2=random.randint(0,7)
        b_opcode=random.choice(list(B_opcodes.keys()))

        imm6=random.randint(-32,31)
        imm6_cut= imm6 & 0x3F
        imm_upper3=(imm6_cut>>3) & 0x7
        imm_lower3=imm6_cut & 0x7

        val1=Register_values.get(rs1)
        val2=Register_values.get(rs2)

        instruction_word=f"{b_opcode:04b}{imm_upper3:03b}{rs1:03b}{rs2:03b}{imm_lower3:03b}"
        dut.Instruction.value=int(instruction_word,2)
        
        # CPU OUT ALWAYS A-B
        expected_CPU_out=(val1-val2) & 0xFF
        expected_CPU_out = expected_CPU_out if expected_CPU_out < 128 else expected_CPU_out - 256
        # EXPECTED BRANCH_TOP CALCULATION
        operation=B_opcodes.get(b_opcode)
        result=operation(val1,val2)
        if(result):
            expected_branch_top=1
        else:
            expected_branch_top=0
        

        await Timer(1,"ns")
        assert dut.CPU_Out.value.to_signed()==expected_CPU_out, f"B_test fail for opcode: {b_opcode}, rs1: {rs1}, val1: {val1}, rs2: {rs2}, val2: {val2}. Expected CPU_out to be {expected_CPU_out}, but got {dut.CPU_Out.value.to_signed()}"
        assert dut.is_branch.value==expected_branch_top, f"B_test fail for is_branch. Expected is_branch to be {expected_branch_top}, but got {dut.is_branch.value}"
        
@cocotb.test()
async def Datapath_NOP_test(dut):
    logger= logging.getLogger("cocotb")
    logger.info("Starting NOP test")
    c=Clock(dut.clk, 10, "ns")
    cocotb.start_soon(c.start())

    dut.Instruction.value=0b1111000000000000
    expected_value=0
    await Timer(1,"ns")
    assert dut.CPU_Out.value==expected_value, f"B_test fail for NOP opcode : 1111. Expected CPU_out to be {expected_value}, but got {dut.CPU_Out.value.to_signed()}"