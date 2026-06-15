//register file
module Registers (
    input clk, input rst, input RegWrite, input [2:0] rs1, input [2:0] rs2, input [2:0] rd, input signed [7:0] write_data, output signed [7:0] reg_data_1, output signed [7:0] reg_data_2);
    
    reg[7:0] Regs[7:0];
    

    always @(posedge rst or posedge clk)
    begin
        if(rst) begin
            /*
            for(k=0;k<31;k=k+1) begin
                Registers[k]<=32'b0;
            end*/
            Regs[0]<=0;
            Regs[1]<=0;
            Regs[2]<=0;
            Regs[3]<=0;
            Regs[4]<=0;
            Regs[5]<=0;
            Regs[6]<=0;
            Regs[7]<=0;
            
        end

        else if(RegWrite) begin
            Regs[rd]<= write_data;
        end
    end

    assign reg_data_1=Regs[rs1];
    assign reg_data_2=Regs[rs2];
    //forwarding ako se u t2 koristi rezultat iz t1
    //assign readData1 = (readReg1 == writeReg && regWrite) ? writeData : registers[readReg1];
endmodule
