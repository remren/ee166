`timescale 1ns/1ps

module FIR_63TAP(
    input logic signed [9:0] in,
    input logic signed [9:0] filt_constant,
    output logic signed [9:0] out,
    input logic CLK,
    input logic RSTN,
    input logic EN,
    input logic FILT_SHIFT
);

    // intermediate variables
    logic signed [25:0] intermed [63:0];
    logic signed [19:0] mult [63:0];
    logic signed [9:0] filt_consts [63:0];
    logic signed [9:0] in2;

    always_ff @(posedge CLK, negedge RSTN) begin  
        if (!RSTN) begin
            filt_consts[0] <= 10'd0;
            intermed[0] <= 26'd0;
            out[9:0] <= 10'd0;
            in2 <= 10'd0;
        end else if (EN) begin
            intermed[0] <= 26'd0;
            filt_consts[0] <= filt_constant;
            in2 <= in;
            out[9:0] <= 10'($signed(intermed[63]) >>> 8);
        end
    end

    genvar i;
    generate for (i = 0; i < 63; i = i + 1) begin : dsp02
        always_comb begin
            mult[i] = 20'(filt_consts[i]) * 20'(in2);
        end
        
        always_ff @(posedge CLK, negedge RSTN) begin  
            if (!RSTN) begin
                intermed[i+1] <= 26'd0;
                filt_consts[i+1] <= 10'd0;
            end else if (EN) begin
                intermed[i+1] <= intermed[i] + mult[i];
                if (FILT_SHIFT) begin
                    filt_consts[i+1] <= filt_consts[i];
                end
            end
        end
    end
    endgenerate

endmodule