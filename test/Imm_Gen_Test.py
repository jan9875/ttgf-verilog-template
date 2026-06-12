# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import Timer

def get_expected_imm(instruction):
    opcode=instruction>>12 & 0xF

    if opcode in [0b0010]:
        #return bottom 8 bits
        return instruction & 0xFF
    elif opcode in [0b0001, 0b0011, 0b0100, 
                     0b0101, 0b0110, 0b0111, 0b1000,
                     0b1001, 0b1010, 0b1011, 0b1100,
                     0b1101, 0b1110, 0b1111]:
        #return bottom 6 bits sign extended to 8 bits
        imm6=instruction & 0x3F
        if(imm6 & 0x20):
            return imm6 | 0xC0
        else:
            return imm6
    else:
        raise ValueError(f"Invalid opcode {opcode:04b} for imm_gen")


@cocotb.test()
async def Imm_Gen_test(dut):
    dut._log.info("Start")
    opcodes_to_test=[0b0001, 0b0011, 0b0100, 
                     0b0101, 0b0110, 0b0111, 0b1000,
                     0b1001, 0b1010, 0b1011, 0b1100]
                     
    
    #test opcodes with imm6
    for opcode in opcodes_to_test:
        for dummy in [0x00, 0x01, 0x1F, 0x20, 0x3F]:
            test_instruction = (opcode <<12) | dummy

            dut.Instruction.value = test_instruction
            await Timer(1, unit="ns")

            expected= get_expected_imm(test_instruction)

            assert dut.Imm_Out.value== expected, f"Failed for opcode {opcode:04b} with dummy {dummy:06b}. Expected Imm_Out to be {expected:08b}, but got {int(dut.Imm_Out.value):08b}"
    
    #test opcode with imm8
    opcode=0b0010
    for dummy in [0x00, 0x01, 0x7F, 0x80, 0xFF]:
        test_instruction = (opcode <<12) | dummy

        dut.Instruction.value = test_instruction
        await Timer(1, unit="ns")
        expected= get_expected_imm(test_instruction)

        assert dut.Imm_Out.value== expected, f"Failed for opcode {opcode:04b} with dummy {dummy:08b}. Expected Imm_Out to be {expected & 0xFF:08b}, but got {int(dut.Imm_Out.value) & 0xFF:08b}"
    
    dut._log.info("All test passed")
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

    #dut._log.info("Test project behavior")

    # Set the input values you want to test
    #dut.Instruction.value = 0b0010000010101010
    

    # Wait for one clock cycle to see the output values
    #await ClockCycles(dut.clk, 2)
    #await Timer(1, unit="ns")

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    #assert dut.Imm_Out.value == 0b10101010, f"Expected Imm_Out to be 0b10101010, but got {dut.Imm_Out.value}"

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
