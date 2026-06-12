import cocotb,logging
from cocotb.triggers import Timer

@cocotb.test()
async def ALU_Test_ADD(dut):
    logger=logging.getLogger("cocotb")
    dut.ALU_Op_in.value=0b000
    for i in range(256):
        for j in range(256):
            val_a=i-128
            val_b=j-128
            dut.A.value=val_a
            dut.B.value=val_b
            await Timer(1, unit="ns")
            expected=(val_a+val_b) & 0xFF
            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
            if((val_a+val_b & 0xFF)==0):
                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
            else:
                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"



@cocotb.test()
async def ALU_Test_SUB(dut):
    logger=logging.getLogger("cocotb")
    dut.ALU_Op_in.value=0b001
    for i in range(256):
        for j in range(256):
            val_a=i-128
            val_b=j-128
            dut.A.value=val_a
            dut.B.value=val_b
            await Timer(1, unit="ns")
            expected=(val_a-val_b) & 0xFF
            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
            if((val_a-val_b & 0xFF)==0):
                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
            else:
                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
            if(val_a<val_b):
                assert dut.less_than.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected less_than to be 1, but got {dut.less_than.value}"


@cocotb.test()
async def ALU_Test_AND(dut):
    logger=logging.getLogger("cocotb")
    dut.ALU_Op_in.value=0b010
    for i in range(256):
        for j in range(256):
            val_a=i-128
            val_b=j-128
            dut.A.value=val_a
            dut.B.value=val_b
            await Timer(1, unit="ns")
            expected=(val_a & val_b) & 0xFF
            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
            if(((val_a & val_b) & 0xFF)==0):
                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
            else:
                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
            

@cocotb.test()
async def ALU_Test_OR(dut):
    logger=logging.getLogger("cocotb")
    dut.ALU_Op_in.value=0b011
    for i in range(256):
        for j in range(256):
            val_a=i-128
            val_b=j-128
            dut.A.value=val_a
            dut.B.value=val_b
            await Timer(1, unit="ns")
            expected=(val_a | val_b) & 0xFF
            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
            if(((val_a | val_b) & 0xFF)==0):
                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
            else:
                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
            
@cocotb.test()
async def ALU_Test_XOR(dut):
    logger=logging.getLogger("cocotb")
    dut.ALU_Op_in.value=0b100
    for i in range(256):
        for j in range(256):
            val_a=i-128
            val_b=j-128
            dut.A.value=val_a
            dut.B.value=val_b
            await Timer(1, unit="ns")
            expected=(val_a ^ val_b) & 0xFF
            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
            if(((val_a ^ val_b) & 0xFF)==0):
                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
            else:
                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                

@cocotb.test()
async def ALU_Test_SLL(dut):
    logger=logging.getLogger("cocotb")
    dut.ALU_Op_in.value=0b101
    for i in range(256):
        for j in range(8):
            val_a=i-128
            val_b=j
            dut.A.value=val_a
            dut.B.value=val_b
            await Timer(1, unit="ns")
            expected=(val_a << val_b) & 0xFF
            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
            if(((val_a << val_b) & 0xFF)==0):
                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
            else:
                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                

@cocotb.test()
async def ALU_Test_SLR(dut):
    logger=logging.getLogger("cocotb")
    dut.ALU_Op_in.value=0b110
    for i in range(256):
        for j in range(8):
            val_a=i-128
            val_b=j
            dut.A.value=val_a
            dut.B.value=val_b
            await Timer(1, unit="ns")
            #turn into unsigned, cutoff higher bits
            unsigned_a=val_a & 0xFF
            expected=(unsigned_a >> val_b) & 0xFF
            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
            if(((unsigned_a >> val_b) & 0xFF)==0):
                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
            else:
                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
