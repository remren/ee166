`timescale 1ns/1ps

module FIR_63TAP(
    input logic signed [9:0] in,
    input logic signed [9:0] filt_constants[62:0],
    output logic signed [9:0] out,
    input logic CLK,
    input logic RSTN,
    input logic EN,
    input logic COEFF_EN
);

    logic signed [25:0] intermed[63:0];
    logic signed [19:0] mult[63:0];
    logic signed [9:0] big_reg[62:0];
    logic signed [9:0] filt_consts[62:0];

    // Main sequential block
    always_ff @(posedge CLK, negedge RSTN) begin  
        if (!RSTN) begin
            for (int d = 0; d < 63; d = d + 1) begin
                big_reg[d] <= 0;
                filt_consts[d] <= 0;
            end
            out[9:0] <= 0;
        end 
        else begin
            if (EN) begin
                // Shift register
                for (int d = 1; d < 63; d = d + 1) begin
                    big_reg[d] <= big_reg[d-1];
                end
                big_reg[0] <= in;
            
                // Output scaling - shift right by 8 bits via [16:8] to
                //                  eliminate accumulated 2**8 from using Q1.8
                out[9:0] <= {intermed[63][25], intermed[63][16:8]};
            end
            if (COEFF_EN) begin
                // Load coefficients
                for (int d = 0; d < 63; d = d + 1) begin
                    filt_consts[d] <= filt_constants[d];
                end
            end
        end 
    end

    // Combinational systolic chain
    assign intermed[0] = 26'd0;  // Initialize first accumulator
    
    genvar t;
    generate for (t = 0; t < 63; t = t + 1) begin: dsp01
        assign mult[t] = big_reg[62-t] * filt_consts[t];
        assign intermed[t+1] = mult[t] + intermed[t];
    end
    endgenerate

endmodule