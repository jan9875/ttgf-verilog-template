import cocotb, logging
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.types import LogicArray
from cocotb.clock import Clock
regs={0b000: 1, 0b001: 4, 
        0b010: 2, 0b011: 24,
        0b100: 0, 0b101: 4, 
        0b110: 2, 0b111: 24}

@cocotb.test()
async def Reg_Test_Reset(dut):
    #pre-reset values
    await Timer(1, unit="ns")
    for i in range(8):
        assert dut.Regs[i].value==LogicArray("XXXXXXXX"), f"Failed for reg {i:03b}. Expected value to be 0, but got {dut.Regs[i].value}"

	#post-reset values
    dut.rst.value=1
    await Timer(1, unit="ns")
    for i in range(8):
        assert dut.Regs[i].value==0, f"Failed for reg {i:03b}. Expected value to be 0, but got {dut.Regs[i].value}"
    dut.rst.value=0

#test reg values rs1 rs2
@cocotb.test()
async def Reg_Test_Register_Values(dut):
    logger=logging.getLogger("cocotb")
    logger.info("Starting Reg Test")
    #regs set predetermined values
    for key, val in regs.items():
        dut.Regs.__getitem__(key).value=val

    for reg1 in regs:
        for reg2 in regs:
            dut.rs1.value=reg1
            dut.rs2.value=reg2
            await Timer(1, unit="ns")
            assert dut.reg_data_1.value==regs.get(reg1), f"Failed for rs1={reg1:03b}. Expected value to be {regs.get(reg1)}, but got {dut.reg_data_1.value}"
            assert dut.reg_data_2.value==regs.get(reg2), f"Failed for rs2={reg2:03b}. Expected value to be {regs.get(reg2)}, but got {dut.reg_data_2.value}"
    
#test reg write
@cocotb.test()
async def Reg_Test_RegWrite(dut):
    rd_regs=[0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111]
    write_values=[0x00, 0x01, 0x7F, 0x80, 0xFF]
    
    dut.RegWrite.value=1
    
    c=Clock(dut.clk, 10, "ns")
    cocotb.start_soon(c.start())
    
    for i in range(8):
        dut.rd.value=rd_regs[i]
        for val in write_values:
            dut.write_data.value=val
            await RisingEdge(dut.clk)
            await ReadOnly()
            assert dut.Regs[i].value==val, f"Failed for rd={rd_regs[i]:03b}. Expected value to be {val}, but got {dut.Regs[i].value}"
            await Timer(1, "ns")