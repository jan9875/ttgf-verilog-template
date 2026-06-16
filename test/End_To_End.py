# This test works on all source files *.v from src folder. Hierarchy is: project.v -> CPU_Core.v -> all other src .v files
# Those files need to be added to VERILOG_SOURCES in makefile
# TOPLEVEL is tb.v. tb.v is wrapper over project.v.

import cocotb, logging, operator
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadOnly, Timer

@cocotb.test()
async def End_To_End_test(dut):
    logger= logging.getLogger("cocotb")
    logger.info("Starting End-to-end test")
    c=Clock(dut.clk, 10, "ns")
    cocotb.start_soon(c.start())
    
    # INITIAL RESET 
    dut.rst_n.value=0
    await Timer(1,"ns")
    dut.rst_n.value=1
    await Timer(1,"ns")
    assert dut.user_project.core.state.value==1 , f"FAIL, state is {dut.user_project.core.state.value} and should be 1"
    PC=0
    opcode=0b0010
    rd=0b001
    imm8=0b0_00000010    
    Instruction_word=f"{opcode:04b}{rd:03b}{imm8:09b}"
    upper_byte = Instruction_word[0:8]
    lower_byte  = Instruction_word[8:16]
    dut.ui_in.value=int(upper_byte,2)
    dut.uio_in.value=int(lower_byte,2)
    expected_value=2
    PC+=1
    expected_PC=PC
    await RisingEdge(dut.clk)
    await ReadOnly()
    assert dut.user_project.core.state.value==0 , f"FAIL, state is {dut.user_project.core.state.value} and should be 0"
    assert dut.uo_out.value.to_signed()==expected_value, f"FAIL, expected: {expected_value}, but got: {dut.uo_out.value.to_signed()}"

    expected_value=0
    await RisingEdge(dut.clk)
    await ReadOnly()
    assert dut.user_project.core.ALU_Mux_top.value==0 , f"FAIL, ALU_MUX_top is {dut.user_project.core.ALU_Mux_top.value} and should be 0"
    assert dut.user_project.core.Imm_Gen_out_wire.value==0 , f"FAIL, imm_gen_out_wire is {dut.user_project.core.Imm_Gen_out_wire.value} and should be 0"

    assert dut.user_project.core.state.value==1 , f"FAIL, state is {dut.user_project.core.state.value} and should be 1"
    assert dut.uo_out.value.to_signed()==expected_PC, f"FAIL, expected: {expected_PC}, but got: {dut.uo_out.value.to_signed()}"
