# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import Timer

def get_expected_imm(instruction):
    opcode=instruction>>12 & 0xF

    if opcode in [0b0010]:
        #return bottom 8 bits
        return instruction & 0xFF
    

    elif opcode in [0b0001, 0b0011, 0b1000,
                     0b1001, 0b1010, 0b1011, 0b1100,
                    ]:
        #return bottom 6 bits sign extended to 8 bits
        imm6=instruction & 0x3F
        if(imm6 & 0x20):
            return imm6 | 0xC0
        else:
            return imm6
        

    elif opcode in [0b0100, 0b0101, 0b0110, 0b0111]:
        #assemble lower3 + upper3
        imm_lower3=instruction & 0x7
        imm_upper3=(instruction >>9 ) & 0x7
        imm6=(imm_upper3<<3) | imm_lower3
        #extend to 8 bits for sign
        if(imm6 & 0x20):
            return imm6 | 0xC0
        else:
            return imm6
        

    else:
        raise ValueError(f"Invalid opcode {opcode:04b} for imm_gen")


@cocotb.test()
async def Imm_Gen_test(dut):
    dut._log.info("Start")
    I_opcodes_to_test=[0b0001, 0b0011, 0b1000,
                     0b1001, 0b1010, 0b1011, 0b1100]
                     
    
    #test I-type opcodes with imm6
    for opcode in I_opcodes_to_test:
        for dummy in [0x00, 0x01, 0x1F, 0x20, 0x3F]:
            test_instruction = (opcode <<12) | dummy

            dut.Instruction.value = test_instruction
            await Timer(1, unit="ns")

            expected= get_expected_imm(test_instruction)

            assert dut.Imm_Out.value== expected, f"Failed for opcode {opcode:04b} with dummy {dummy:06b}. Expected Imm_Out to be {expected:08b}, but got {int(dut.Imm_Out.value):08b}"
    
    #test SB-type opcodes with split imm6
    SB_opcodes_to_test=[0b0100, 0b0101, 0b0110, 0b0111]

    for opcode in SB_opcodes_to_test:
        for dummy in [0x00, 0x01, 0x1F, 0x20, 0x3F]:
            lower3=dummy & 0x7
            upper3=(dummy >>3) & 0x7
            test_instruction = (opcode <<12) | (upper3<<9) | lower3

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
