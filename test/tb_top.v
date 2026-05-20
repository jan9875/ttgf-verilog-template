`default_nettype none
`timescale 1ns / 1ps

module tb_top;
    reg clk, rst_n, ena;
    reg[7:0] ui_in, uio_in;
    wire [7:0] uo_out, uio_out, uio_oe;
    tt_um_example uut(.clk(clk), 
                      .rst_n(rst_n), 
                      .ena(ena), 
                      .ui_in(ui_in),
                      .uo_out(uo_out),
                      .uio_in(uio_in),
                      .uio_out(uio_out),
                      .uio_oe(uio_oe));


    always begin 
        #5 clk=~clk;

    end

    initial begin


        clk=0;
        rst_n=0;
        ena=1;
        $dumpfile("./wave1.vcd");   
        $dumpvars(0, tb_top); 
        
        ui_in=8'b00000100;
        uio_in=8'b00001000;
         
        
        

        #10;
        rst_n=1;
        #5
        $strobe("Time %0t: out= %b", $time, uo_out);

        #15;
        ui_in=8'b00010110;
        uio_in=8'b10000011;
        
        $strobe("Time %0t: out= %b", $time, uo_out);
        #10;
        $finish;

    end
    
endmodule
