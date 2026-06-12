import cocotb, logging
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.clock import Clock


@cocotb.test()
async def D_Mem_Test_Reset(dut):
    logger=logging.getLogger("cocotb")
    logger.info("Starting D_Mem Test Reset")
    dut.rst.value=1
    for i in range(16):
        dut.Address.value=i
        await Timer(1, unit="ns")
        assert dut.MemData_Out.value==0, f"Failed for Address={i:02X}. Expected value to be 00, but got {dut.MemData_Out.value.integer:02X}"
    dut.rst.value=0



@cocotb.test()
async def D_Mem_Test_Write(dut):
    logger=logging.getLogger("cocotb")
    logger.info("Starting D_Mem Test Write")
    c=Clock(dut.clk,10,"ns")
    cocotb.start_soon(c.start())

    #test non_enable
    dut.MemWrite.value=1
    dut.PC_enable_sig.value=0
    for i in range(16):
        dut.Address.value=i
        dut.WriteData.value=i
        await RisingEdge(dut.clk)
    
        
    #check internal Memory
    for i in range(16):
        assert dut.memory[i].value==0, f"Failed for Address={i:02X}. Expected value to be 00, but got {int(dut.memory[i].value):02X}"
        #move out of ReadOnly
        await Timer(1, unit="ns")


    #test enable
    dut.PC_enable_sig.value=1
    for i in range(16):
        dut.Address.value=i
        dut.WriteData.value=i
        await RisingEdge(dut.clk)

    #check internal Memory    
    for i in range(16):
        assert dut.memory[i].value==i, f"Failed for Address={i:02X}. Expected value to be {i:02X}, but got {int(dut.memory[i].value):02X}"
        await Timer(1, unit="ns")

    #turn off writing signals
    dut.MemWrite.value=0
    dut.PC_enable_sig.value=0



@cocotb.test()
async def D_Mem_Test_Read(dut):
    logger=logging.getLogger("cocotb")
    logger.info("Starting D_Mem Test Read")
    dut.MemRead.value=1
    for i in range(16):
        dut.Address.value=i
        await Timer(1, unit="ns")
        assert dut.MemData_Out.value==i, f"Failed for Address={i:02X}. Expected value to be {i:02X}, but got {int(dut.MemData_Out.value):02X}"

    