import cocotb,logging, operator
from cocotb.triggers import Timer
ALU_Op_values={0b000: operator.add,
               0b001: operator.sub,
               0b010: operator.and_,
               0b011: operator.or_,
               0b100: operator.xor}
#@cocotb.test()
#async def ALU_Test_ADD(dut):
#    logger=logging.getLogger("cocotb")
#    dut.ALU_Op_in.value=0b000
#    for i in range(256):
#        for j in range(256):
#            val_a=i-128
#            val_b=j-128
#            dut.A.value=val_a
#            dut.B.value=val_b
#            await Timer(1, unit="ns")
#            expected=(val_a+val_b) & 0xFF
#            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
#            if((val_a+val_b & 0xFF)==0):
#                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
#            else:
#                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"

@cocotb.test()
async def ALU_Test(dut):
    logger=logging.getLogger("cocotb")
    logger.info("Starting ALU_Test")
    for alu_op, operation in ALU_Op_values.items():
        dut.ALU_Op_in.value=alu_op
        for i in range(256):
            for j in range(256):
                val_a=i-128
                val_b=j-128
                dut.A.value=val_a
                dut.B.value=val_b
                await Timer(1, unit="ns")
                expected=operation(val_a,val_b) & 0xFF
                assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
                if(expected==0):
                    assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
                else:
                    assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
                if(alu_op==0b001 and val_a<val_b):
                    assert dut.less_than.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected less_than to be 1, but got {dut.less_than.value}"


#@cocotb.test()
#async def ALU_Test_SUB(dut):
#    logger=logging.getLogger("cocotb")
#    dut.ALU_Op_in.value=0b001
#    for i in range(256):
#        for j in range(256):
#            val_a=i-128
#            val_b=j-128
#            dut.A.value=val_a
#            dut.B.value=val_b
#            await Timer(1, unit="ns")
#            expected=(val_a-val_b) & 0xFF
#            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
#            if((val_a-val_b & 0xFF)==0):
#                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
#            else:
#                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
#            if(val_a<val_b):
#                assert dut.less_than.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected less_than to be 1, but got {dut.less_than.value}"
#
#
#@cocotb.test()
#async def ALU_Test_AND(dut):
#    logger=logging.getLogger("cocotb")
#    dut.ALU_Op_in.value=0b010
#    for i in range(256):
#        for j in range(256):
#            val_a=i-128
#            val_b=j-128
#            dut.A.value=val_a
#            dut.B.value=val_b
#            await Timer(1, unit="ns")
#            expected=(val_a & val_b) & 0xFF
#            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
#            if(((val_a & val_b) & 0xFF)==0):
#                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
#            else:
#                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
#            
#
#@cocotb.test()
#async def ALU_Test_OR(dut):
#    logger=logging.getLogger("cocotb")
#    dut.ALU_Op_in.value=0b011
#    for i in range(256):
#        for j in range(256):
#            val_a=i-128
#            val_b=j-128
#            dut.A.value=val_a
#            dut.B.value=val_b
#            await Timer(1, unit="ns")
#            expected=(val_a | val_b) & 0xFF
#            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
#            if(((val_a | val_b) & 0xFF)==0):
#                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
#            else:
#                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
#            
#@cocotb.test()
#async def ALU_Test_XOR(dut):
#    logger=logging.getLogger("cocotb")
#    dut.ALU_Op_in.value=0b100
#    for i in range(256):
#        for j in range(256):
#            val_a=i-128
#            val_b=j-128
#            dut.A.value=val_a
#            dut.B.value=val_b
#            await Timer(1, unit="ns")
#            expected=(val_a ^ val_b) & 0xFF
#            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
#            if(((val_a ^ val_b) & 0xFF)==0):
#                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
#            else:
#                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
shift_ALU_op_values={0b101: operator.lshift,
                     0b110: operator.rshift}

@cocotb.test()
async def ALU_Test_Shifts(dut):
    logger=logging.getLogger("cocotb")
    logger.info("Start ALU Shift testing")
    for alu_op,operation in shift_ALU_op_values.items():
        dut.ALU_Op_in.value=alu_op
        for i in range(256):
            for j in range(8):
                val_a=i-128
                val_b=j
                dut.A.value=val_a
                dut.B.value=val_b
                await Timer(1, unit="ns")
                if(alu_op==0b110):
                    val_a=val_a & 0xFF
                expected=operation(val_a,val_b) & 0xFF
                
                assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
                if(expected==0):
                    assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
                else:
                    assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                



#@cocotb.test()
#async def ALU_Test_SLL(dut):
#    logger=logging.getLogger("cocotb")
#    dut.ALU_Op_in.value=0b101
#    for i in range(256):
#        for j in range(8):
#            val_a=i-128
#            val_b=j
#            dut.A.value=val_a
#            dut.B.value=val_b
#            await Timer(1, unit="ns")
#            expected=(val_a << val_b) & 0xFF
#            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
#            if(((val_a << val_b) & 0xFF)==0):
#                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
#            else:
#                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
#
#@cocotb.test()
#async def ALU_Test_SLR(dut):
#    logger=logging.getLogger("cocotb")
#    dut.ALU_Op_in.value=0b110
#    for i in range(256):
#        for j in range(8):
#            val_a=i-128
#            val_b=j
#            dut.A.value=val_a
#            dut.B.value=val_b
#            await Timer(1, unit="ns")
#            #turn into unsigned, cutoff higher bits
#            unsigned_a=val_a & 0xFF
#            expected=(unsigned_a >> val_b) & 0xFF
#            assert dut.ALU_result.value==expected, f"Failed for A={i:02X}, B={j:02X}. Expected value to be {expected:02X}, but got {dut.ALU_result.value.integer:02X}"
#            if(((unsigned_a >> val_b) & 0xFF)==0):
#                assert dut.zero.value==1, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 1, but got {dut.zero.value}"
#            else:
#                assert dut.zero.value==0, f"Failed for A={i:02X}, B={j:02X}. Expected zero to be 0, but got {dut.zero.value}"                
