module Datapath_Wrapper (
    input [15:0] Instruction, input clk, input rst, output[7:0] CPU_Out, output is_branch
);
    
    wire RegWrite_wire, ALUSrc_wire, MemRead_wire, MemWrite_wire, MemToReg_wire, PC_enable_sig;
    wire Is_beq_wire, Is_bne_wire, Is_blt_wire, zero_wire, less_than_wire, Branch_control_top;
    wire [2:0] ALUOp_wire;
    wire [7:0] Reg_data1_wire, Reg_data2_wire, Imm_Gen_out_wire, ALU_Mux_top, ALU_Top, MemData_out_wire;

    wire [7:0] ALU_A_top; 
    assign ALU_A_top = (Instruction[15:12] == 4'b0010 || Instruction[15:12] == 4'b1111) ? 8'b0 : Reg_data1_wire;

    assign is_branch=Branch_control_top;
    Registers Registers(.clk(clk), 
                        .rst(rst),
                        .RegWrite(RegWrite_wire), 
                        .rs1(Instruction[8:6]), 
                        .rs2(Instruction[5:3]), 
                        .rd(Instruction[11:9]), 
                        .write_data(CPU_Out), 
                        .reg_data_1(Reg_data1_wire),  
                        .reg_data_2(Reg_data2_wire)
                        );

    Control_Unit control_unit(.Instruction(Instruction[15:12]), 
                              .funct3(Instruction[2:0]),
                              .Control_Mux_out_sig(),
                              .PC_enable_sig(PC_enable_sig),
                              .RegWrite(RegWrite_wire),
                              .ALUSrc(ALUSrc_wire),
                              .MemRead(MemRead_wire),
                              .MemWrite(MemWrite_wire),
                              .MemToReg(MemToReg_wire),
                              .is_BEQ(Is_beq_wire),
                              .is_BLT(Is_blt_wire),
                              .is_BNE(Is_bne_wire),
                              .ALUOp(ALUOp_wire)
                              );


    ALU ALU( .A(ALU_A_top), 
             .B(ALU_Mux_top), 
             .ALU_Op_in(ALUOp_wire), 
             .zero(zero_wire),
             .less_than(less_than_wire), 
             .ALU_result(ALU_Top)
             ); 

    Imm_Gen imm_gen(.Instruction(Instruction), 
                    .Imm_Out(Imm_Gen_out_wire)
                    );

    Branch_Control branch_control(.is_beq(Is_beq_wire),
                                  .is_bne(Is_bne_wire),
                                  .is_blt(Is_blt_wire),
                                  .zero(zero_wire),
                                  .less_than(less_than_wire),
                                  .branch_control_top(Branch_control_top)
                                  );

    Data_Memory data_memory(.clk(clk), 
                            .rst(rst), 
                            .Address(ALU_Top), 
                            .PC_enable_sig(PC_enable_sig),
                            .MemWrite(MemWrite_wire), 
                            .MemRead(MemRead_wire), 
                            .WriteData(Reg_data2_wire), 
                            .MemData_Out(MemData_out_wire));


    Mux1 Data_memory_mux(.sel1(MemToReg_wire), 
                        .A1(ALU_Top), 
                        .B1(MemData_out_wire), 
                        .mux1_out(CPU_Out));

    Mux1 ALU_mux( .sel1(ALUSrc_wire), 
                  .A1(Reg_data2_wire), 
                  .B1(Imm_Gen_out_wire), 
                  .mux1_out(ALU_Mux_top));         
endmodule