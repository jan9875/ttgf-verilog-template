import cocotb
from cocotb.triggers import Timer
@cocotb.test()
async def test_adder(dut):
    a=(4,99, 5, 128)
    b=(5,101, -7, 150)
    y=(9,-6, -2, 22)
    for i in range(4):
        dut.in_1.value= a[i] 
        dut.in_2.value= b[i]
        
        await Timer(1, "ns")
        assert dut.Add_out.value.to_signed()== y[i], f"Error at iteration {i}"

