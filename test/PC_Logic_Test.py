import cocotb, logging
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.clock import Clock

non_branch_opcodes=[0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 
                   0b1000, 0b1001, 0b1010, 0b1011, 0b1100, 
                   ]
branch_opcodes={0b0101: "BEQ", 0b0110: "BNE", 0b0111: "BLT"}
imm_gen_values=[0x00, 0x01, 0xFF]
special_opcode=0b1111

@cocotb.test()
async def PC_Logic_Test_Reset_And_Non_Branch(dut):
    #test reset
    logger=logging.getLogger("cocotb")
    logger.info("Starting PC Subsystem Test Reset")
    dut.rst.value=1
    c=Clock(dut.clk,10,"ns")
    cocotb.start_soon(c.start())
    #check reset 5 times to see if it holds
    for i in range(5):
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.PC_Out.value==0, f"Failed for reset. Expected value to be 00, but got {dut.PC_Out.value.integer:02X}"
    
    await Timer(1, "ns")


    dut.rst.value=0
    PC=0


    #non_branch test
    for value in non_branch_opcodes:

        #phase1 - non-branch instruction
        dut.Instruction.value=value
        await RisingEdge(dut.clk)
        await ReadOnly()
        expected=(PC+1) & 0xFF
        assert dut.enable_wire.value==1, f"Failed for non-branch instruction. Expected enable to be 1, but got {dut.enable_wire.value}"
        assert dut.branch_control_top.value==0, f"Failed for non-branch instruction. Expected branch_control to be 0, but got {dut.branch_control_top.value}"
        
        assert dut.PCplus1_top.value==expected+1, f"Failed for non-branch instruction. Expected PCplus1 to be {(expected+1):02X}, but got {dut.PCplus1_top.value.integer:02X}"
        assert dut.mux1_out.value==expected+1, f"Failed for non-branch instruction. Expected mux1_out to be {(expected+1):02X}, but got {dut.mux1_out.value.integer:02X}"

        assert dut.PC_Out.value==expected, f"Failed for non-branch instruction. Expected PC to be {expected:02X}, but got {dut.PC_Out.value.integer:02X}"
        
        await Timer(1, "ns")

        #phase2 - NOP
        dut.Instruction.value=special_opcode
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.enable_wire.value==0, f"Failed for special opcode. Expected enable to be 0, but got {dut.enable_wire.value}"
        assert dut.PC_Out.value==expected, f"Failed for special opcode. Expected PC to be {expected:02X}, but got {dut.PC_Out.value.integer:02X}"
        PC+=1
        await Timer(1, "ns")

    PC=0
    #test full cycle
    dut.rst.value=1
    await Timer(1,"ns")
    dut.rst.value=0
    dut.Instruction.value=non_branch_opcodes[0]
    for i in range(256):
        
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.PC_Out.value==((PC+1) % 256), f"Failed for full cycle. Expected PC to be {((PC+1) % 256):02X}, but got {dut.PC_Out.value.integer:02X}"
        PC+=1
    assert dut.PC_Out.value==0, f"Failed for PC overflow. Expected PC to be 0, but got {dut.PC_Out.value.integer:02X}"


@cocotb.test()
async def PC_Logic_Test_Branch_BEQ(dut):
    c=Clock(dut.clk, 10, "ns")
    cocotb.start_soon(c.start())
    logger=logging.getLogger("cocotb")
    logger.info("Starting PC Subsystem Test Branch")
    PC=0

    for opcode in branch_opcodes.keys():

        #Branch test, flags off, PC gets incremented, no jump
        dut.Instruction.value=opcode
        if(opcode==0b0101):
            dut.zero.value=0
        elif(opcode==0b0110): 
            dut.zero.value=1
        else:
            dut.less_than.value=0
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.PC_Out.value==(0x01), f"Failed for Branch: {branch_opcodes.get(opcode)}. Expected PC to be 0x01, but got {dut.PC_Out.value.integer:02X}"
    
        await Timer(1, "ns")
        dut.rst.value=1
        await Timer(1, "ns")
        dut.rst.value=0


        #Branch test, corresponding flag on, PC jump
        if(opcode==0b0101):
            dut.zero.value=1
        elif(opcode==0b0110): 
            dut.zero.value=0
        else:
            dut.less_than.value=1
        
        for value in imm_gen_values:
        
            dut.imm_Gen_Top.value=value
            await RisingEdge(dut.clk)
            await ReadOnly()
            assert dut.PC_Out.value==value, f"Failed for Branch: {branch_opcodes.get(opcode)}. Expected PC to be {value}, but got {dut.PC_Out.value.integer:02X}"
            await Timer(1,"ns")
            dut.rst.value=1
            await RisingEdge(dut.clk)
            dut.rst.value=0



        #Branch test jump overflow, PC=50, jump=F0 (240)
        assert dut.PC_Out.value==0, f"Failed for Branch: {branch_opcodes.get(opcode)}. Expected PC to be 0, but got {dut.PC_Out.value.integer:02X}"

        dut.Instruction.value=non_branch_opcodes[0]
        #advance 50 cycles
        for i in range(50):
            await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.PC_Out.value.integer==50, f"Failed for Branch: {branch_opcodes.get(opcode)}. Expected PC to be 50, but got {dut.PC_Out.value.integer}"
        await Timer(1,"ns")


        dut.Instruction.value=opcode
        dut.imm_Gen_Top.value=0xF0 #240
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.PC_Out.value==((50+240) & 0xFF), f"Failed for Branch: {branch_opcodes.get(opcode)}. Expected PC to be {((50+240) & 0xFF)}, but got {dut.PC_Out.value.integer:02X}"
        await Timer(1,"ns")
        dut.rst.value=1
        await Timer(1, "ns")
        dut.rst.value=0
