`timescale 1ns/1ps

string file_path = "";
module tb;
    logic signed [9:0] filt_constant;
    logic signed [9:0] in;
    logic rst = 0;
    logic sample_clk = 0;
    logic signed [9:0] out;
    logic en = 1;
    logic filter_en = 1;

    FIR_63TAP DUT (
        .in(in),
        .filt_constant(filt_constant),
        .out(out),
        .CLK(sample_clk),
        .RSTN(rst),
        .EN(en),
        .FILT_SHIFT(filter_en)
    );

    integer fp;
    integer fp2;
    integer status;

    initial begin
        $dumpfile({file_path, "dump.vcd"}); 
        $dumpvars(0, tb);

        // Reset sequence
        rst = 0;
        #1;
        sample_clk = ~sample_clk;
        #1;
        sample_clk = ~sample_clk;
        #1;
        rst = 1;
        #1;
        en = 1;
        filter_en = 1;

        // Load filter coefficients
        fp = $fopen({file_path, "RTL/filter_taps.txt"}, "r");
        if (fp == 0) begin
            $display("Error: Could not open filter_taps.txt");
            $finish;
        end

        for (int p = 0; p < 63; p = p + 1) begin
            status = $fscanf(fp, "%d", filt_constant); 
            sample_clk = ~sample_clk;
            #1;
            sample_clk = ~sample_clk;
            #1;
        end
        
        $fclose(fp);

        // Process input data
        fp = $fopen({file_path, "RTL/s400_500_input_signal.csv"}, "r");
        if (fp == 0) begin
            $display("Error: Could not open combined.csv");
            $finish;
        end
        
        fp2 = $fopen({file_path, "output.csv"}, "w");
        if (fp2 == 0) begin
            $display("Error: Could not open output.csv");
            $finish;
        end

        en = 1;
        filter_en = 0;

        while (!$feof(fp)) begin
            status = $fscanf(fp, "%d", in); 
            if (status == 1) begin
                sample_clk = ~sample_clk;
                #1;
                sample_clk = ~sample_clk;
                #1;
                $fdisplay(fp2, "%d", out);
            end
        end

        $fclose(fp);
        $fclose(fp2);
        
        #50 $finish;
    end

endmodule