module PC_Logic_Wrapper (
    input clk, 
    input rst, 
    input [3:0] Instruction, 
    input [7:0] imm_Gen_Top, 
    input zero, 
    input less_than,
    output [7:0] PC_Out
);
    wire beq_sig, bne_sig, blt_sig, branch_control_top, enable_wire;
    wire [7:0] PCplus1_top, adder_top, mux1_out;

    Program_Counter PC(.clk(clk), 
                       .rst(rst), 
                       .PC_in(mux1_out), 
                       .PC_out(PC_Out), 
                       .PC_enable_sig(enable_wire));


    Control_Unit control_unit(.Instruction(Instruction),
                              .is_BEQ(beq_sig), 
                              .is_BNE(bne_sig), 
                              .is_BLT(blt_sig), 
                              .PC_enable_sig(enable_wire),
                              .MemWrite(),
                              .ALUSrc(),
                              .ALUOp(),
                              .RegWrite(),
                              .MemToReg(),
                              .MemRead(),
                              .Control_Mux_out_sig(),
                              .funct3()
                            );


    PCplus1Adder PCplus1Adder(.FromPC(PC_Out), .NextPC(PCplus1_top));


    Adder adder(.in_1(PC_Out), 
                .in_2(imm_Gen_Top), 
                .Add_out(adder_top));


    Mux1 mux1(.A1(PCplus1_top), 
              .B1(adder_top), 
              .sel1(branch_control_top), 
              .mux1_out(mux1_out));
    
    
    Branch_Control branch_control(.is_beq(beq_sig),
                                  .is_bne(bne_sig),
                                  .is_blt(blt_sig),
                                  .zero(zero),
                                  .less_than(less_than),
                                  .branch_control_top(branch_control_top)
                                );

endmodule