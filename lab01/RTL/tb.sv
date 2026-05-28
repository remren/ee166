`timescale 1ns/1ps

module tb;
    string file_path = "";
    
    logic signed [9:0] filt_constants [62:0];
    logic signed [9:0] in;
    logic rst = 0;
    logic sample_clk = 0;
    logic signed [9:0] out;
    logic en = 0;

    FIR_63TAP DUT (
        .in(in),
        .filt_constants(filt_constants),
        .out(out),
        .CLK(sample_clk),
        .RSTN(rst),
        .EN(en)
    );

    integer fp;
    integer fp2;
    integer status;
    integer i;

    initial begin
        $dumpfile({file_path, "dump.vcd"}); 
        $dumpvars(0, tb);

        // Initialize signals
        in = 10'd0;
        for (i = 0; i < 63; i++) begin
            filt_constants[i] = 10'd0;
        end

        // Reset sequence
        rst = 0;
        en = 0;
        #10;
        rst = 1;
        #10;
        
        // Enable and load coefficients
        en = 1;
        
        // Load filter coefficients from file
        fp = $fopen({file_path, "RTL_filter_taps.csv"}, "r");
        if (fp == 0) begin
            $display("Error: Could not open RTL_filter_taps.csv");
            $finish;
        end

        for (i = 0; i < 63; i++) begin
            status = $fscanf(fp, "%d", filt_constants[i]); 
            if (status != 1) begin
                $display("Error: Failed to read coefficient %0d", i);
                $finish;
            end
        end
        $fclose(fp);

        // Run some cycles to load coefficients and initialize pipeline with zeros
        for (i = 0; i < 130; i++) begin
            #5;
            sample_clk = 1;
            #5;
            sample_clk = 0;
        end

        // Open input and output files
        fp = $fopen({file_path, "RTL_s400_500_input_signal_longer.csv"}, "r");
        if (fp == 0) begin
            $display("Error: Could not open RTL_s400_500_input_signal_longer.csv");
            $finish;
        end
        
        fp2 = $fopen({file_path, "RTL_output.csv"}, "w");
        if (fp2 == 0) begin
            $display("Error: Could not open RTL_output.csv");
            $finish;
        end

        // Process input data - the output will be delayed by 63 cycles
        while (!$feof(fp)) begin
            status = $fscanf(fp, "%d", in); 
            if (status == 1) begin
                #5;
                sample_clk = 1;
                #5;
                sample_clk = 0;
                $fdisplay(fp2, "%d", out);
            end
        end

        // Flush pipeline with zeros to get remaining outputs
        in = 10'd0;
        for (i = 0; i < 63; i++) begin
            #5;
            sample_clk = 1;
            #5;
            sample_clk = 0;
            $fdisplay(fp2, "%d", out);
        end

        $fclose(fp);
        $fclose(fp2);
        
        #50 $finish;
    end

endmodule