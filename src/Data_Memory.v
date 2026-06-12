//Data memory
module Data_Memory (
    input clk, input rst, input [7:0] Address, input PC_enable_sig, input MemWrite, input MemRead, input signed [7:0] WriteData, output signed [7:0] MemData_Out
);
    integer i;
    wire _unused = &{Address[7:4], 1'b0};
    reg[7:0] memory[15:0];
    always @(posedge clk or posedge rst) begin
        if(rst) begin
            for (i=0; i<16; i=i+1 ) begin
                memory[i]<=8'b0;
            end
        end
        else if(MemWrite && PC_enable_sig) begin
            memory[Address[3:0]]<=WriteData;
        end
    end 
    assign MemData_Out= (MemRead)? memory[Address[3:0]]: 8'b0;
endmodule
