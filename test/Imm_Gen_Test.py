# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import Timer

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    #clock = Clock(dut.clk, 10, unit="ns")
    #cocotb.start_soon(clock.start())

    # Reset
    #dut._log.info("Reset")
    #dut.ena.value = 1
    #dut.ui_in.value = 4
    #dut.uio_in.value = 8
    #dut.rst_n.value = 0
    #await ClockCycles(dut.clk, 1)
    #dut._log.info(dut.uo_out.value)

    #dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.Instruction.value = 0b0010000010101010
    

    # Wait for one clock cycle to see the output values
    #await ClockCycles(dut.clk, 2)
    await Timer(1, unit="ns")

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.Imm_Out.value == 0b10101010, f"Expected Imm_Out to be 0b10101010, but got {dut.Imm_Out.value}"

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
