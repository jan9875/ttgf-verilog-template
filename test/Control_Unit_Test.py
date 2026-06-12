import cocotb, logging
from cocotb.triggers import Timer

@cocotb.test()
async def Control_Unit_test(dut):
    logger=logging.getLogger("cocotb_logger")
    logger.info("Starting Control Unit Test")
    expected_R_type ={
        #funct3: ALUOp
        0b000: 0b000, #ADD
        0b001: 0b001, #SUB
        0b010: 0b010, #AND
        0b011: 0b011, #OR
        0b100: 0b100, #XOR
        0b101: 0b101, #SLL
        0b110: 0b110, #SRL
        0b111: 0b000, #default
    }

    expected_PC_enable_sig=1;
    expected_Control_Mux_out_sig=1;
    expected_ALUSrc=0;
    expected_MemToReg=0;
    expected_RegWrite=1;
    expected_MemRead=0;
    expected_MemWrite=0;
    expected_is_BEQ=0;
    expected_is_BNE=0;
    expected_is_BLT=0;
    
    for funct3, expected_ALUOp in expected_R_type.items():
        dut.Instruction.value=0b0000
        dut.funct3.value=funct3
        await Timer(1, unit="ns")
        
        assert dut.PC_enable_sig.value== expected_PC_enable_sig, f"Failed for opcode {opcode:04b}. Expected PC_enable_sig to be {expected_PC_enable_sig}, but got {dut.PC_enable_sig.value}"
        assert dut.Control_Mux_out_sig.value== expected_Control_Mux_out_sig, f"Failed for opcode {opcode:04b}. Expected Control_Mux_out_sig to be {expected_Control_Mux_out_sig}, but got {dut.Control_Mux_out_sig.value}"
        assert dut.ALUSrc.value== expected_ALUSrc, f"Failed for opcode {opcode:04b}. Expected ALUSrc to be {expected_ALUSrc}, but got {dut.ALUSrc.value}"
        assert dut.MemToReg.value== expected_MemToReg, f"Failed for opcode {opcode:04b}. Expected MemToReg to be {expected_MemToReg}, but got {dut.MemToReg.value}"
        assert dut.RegWrite.value== expected_RegWrite, f"Failed for opcode {opcode:04b}. Expected RegWrite to be {expected_RegWrite}, but got {dut.RegWrite.value}"
        assert dut.MemRead.value== expected_MemRead, f"Failed for opcode {opcode:04b}. Expected MemRead to be {expected_MemRead}, but got {dut.MemRead.value}"
        assert dut.MemWrite.value== expected_MemWrite, f"Failed for opcode {opcode:04b}. Expected MemWrite to be {expected_MemWrite}, but got {dut.MemWrite.value}"
        assert dut.is_BEQ.value== expected_is_BEQ, f"Failed for opcode {opcode:04b}. Expected is_BEQ to be {expected_is_BEQ}, but got {dut.is_BEQ.value}"
        assert dut.is_BNE.value== expected_is_BNE, f"Failed for opcode {opcode:04b}. Expected is_BNE to be {expected_is_BNE}, but got {dut.is_BNE.value}"
        assert dut.is_BLT.value== expected_is_BLT, f"Failed for opcode {opcode:04b}. Expected is_BLT to be {expected_is_BLT}, but got {dut.is_BLT.value}"
        assert dut.ALUOp.value== expected_ALUOp, f"Failed for opcode {opcode:04b}. Expected ALUOp to be {expected_ALUOp}, but got {dut.ALUOp.value}"






    expected={
        #opcode: (PC_enable_sig, Control_Mux_out_sig, ALUSrc, MemToReg, RegWrite, MemRead, MemWrite, is_BEQ, is_BNE, is_BLT, ALUOp)
        0b0001: (1,1,1,0,1,0,0,0,0,0,0b000), #ADDI
        0b0010: (1,1,1,0,1,0,0,0,0,0,0b000), #LI
        0b0011: (1,1,1,1,1,1,0,0,0,0,0b000), #LW
        0b0100: (1,1,1,1,0,0,1,0,0,0,0b000), #SW
        0b0101: (1,1,1,1,0,0,0,1,0,0,0b001), #BEQ
        0b0110: (1,1,1,1,0,0,0,0,1,0,0b001), #BNE
        0b0111: (1,1,1,1,0,0,0,0,0,1,0b001), #BLT
        0b1000: (1,1,1,0,1,0,0,0,0,0,0b010), #ANDI
        0b1001: (1,1,1,0,1,0,0,0,0,0,0b011), #ORI
        0b1010: (1,1,1,0,1,0,0,0,0,0,0b100), #XORI
        0b1011: (1,1,1,0,1,0,0,0,0,0,0b101), #SLLI
        0b1100: (1,1,1,0,1,0,0,0,0,0,0b110), #SLRI
        0b1101: (0,0,0,0,0,0,0,0,0,0,0b000), #default
        0b1110: (0,0,0,0,0,0,0,0,0,0,0b000), #default
        0b1111: (0,0,0,0,0,0,0,0,0,0,0b000), #NOP
    }
    
    for opcode, expected_value in expected.items():
        dut.Instruction.value=opcode
        dut.funct3.value=0b000 #funct3 for non R-type instructions doesnt matter
        await Timer(1, unit="ns")

        expected_PC_enable_sig, expected_Control_Mux_out_sig, expected_ALUSrc, expected_MemToReg, expected_RegWrite, expected_MemRead, expected_MemWrite, expected_is_BEQ, expected_is_BNE, expected_is_BLT, expected_ALUOp=expected_value

        assert dut.PC_enable_sig.value== expected_PC_enable_sig, f"Failed for opcode {opcode:04b}. Expected PC_enable_sig to be {expected_PC_enable_sig}, but got {dut.PC_enable_sig.value}"
        assert dut.Control_Mux_out_sig.value== expected_Control_Mux_out_sig, f"Failed for opcode {opcode:04b}. Expected Control_Mux_out_sig to be {expected_Control_Mux_out_sig}, but got {dut.Control_Mux_out_sig.value}"
        assert dut.ALUSrc.value== expected_ALUSrc, f"Failed for opcode {opcode:04b}. Expected ALUSrc to be {expected_ALUSrc}, but got {dut.ALUSrc.value}"
        assert dut.MemToReg.value== expected_MemToReg, f"Failed for opcode {opcode:04b}. Expected MemToReg to be {expected_MemToReg}, but got {dut.MemToReg.value}"
        assert dut.RegWrite.value== expected_RegWrite, f"Failed for opcode {opcode:04b}. Expected RegWrite to be {expected_RegWrite}, but got {dut.RegWrite.value}"
        assert dut.MemRead.value== expected_MemRead, f"Failed for opcode {opcode:04b}. Expected MemRead to be {expected_MemRead}, but got {dut.MemRead.value}"
        assert dut.MemWrite.value== expected_MemWrite, f"Failed for opcode {opcode:04b}. Expected MemWrite to be {expected_MemWrite}, but got {dut.MemWrite.value}"
        assert dut.is_BEQ.value== expected_is_BEQ, f"Failed for opcode {opcode:04b}. Expected is_BEQ to be {expected_is_BEQ}, but got {dut.is_BEQ.value}"
        assert dut.is_BNE.value== expected_is_BNE, f"Failed for opcode {opcode:04b}. Expected is_BNE to be {expected_is_BNE}, but got {dut.is_BNE.value}"
        assert dut.is_BLT.value== expected_is_BLT, f"Failed for opcode {opcode:04b}. Expected is_BLT to be {expected_is_BLT}, but got {dut.is_BLT.value}"
        assert dut.ALUOp.value== expected_ALUOp, f"Failed for opcode {opcode:04b}. Expected ALUOp to be {expected_ALUOp}, but got {dut.ALUOp.value}"