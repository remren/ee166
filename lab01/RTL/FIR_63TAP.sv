module FIR_63TAP(
    input logic signed [9:0] in,
    input logic signed [9:0] filt_constant,
    output logic signed [9:0] out,
    input logic CLK,
    input logic RSTN,
    input logic EN,
    input logic FILT_SHIFT
);

    // Shift register for input samples
    logic signed [9:0] shift_reg [62:0];  // 63-stage shift register
    logic signed [9:0] filt_consts [62:0];  // 63 coefficients
    logic signed [19:0] mult [62:0];  // 63 multipliers (10-bit * 10-bit = 20-bit)
    logic signed [25:0] sum;  // Accumulator (needs extra bits for 63 additions)

    integer i;

    always_ff @(posedge CLK, negedge RSTN) begin
        if (!RSTN) begin
            // Reset shift register and coefficients
            for (i = 0; i < 63; i = i + 1) begin
                shift_reg[i] <= 10'd0;
                filt_consts[i] <= 10'd0;
            end
            out <= 10'd0;
        end else if (EN) begin
            if (FILT_SHIFT) begin
                // Load coefficients
                filt_consts[0] <= filt_constant;
                for (i = 0; i < 62; i = i + 1) begin
                    filt_consts[i+1] <= filt_consts[i];
                end
                
                // During coefficient loading, also shift in zeros
                shift_reg[0] <= 10'd0;
                for (i = 0; i < 62; i = i + 1) begin
                    shift_reg[i+1] <= shift_reg[i];
                end
            end else begin
                // Normal operation: shift in new input sample
                shift_reg[0] <= in;
                for (i = 0; i < 62; i = i + 1) begin
                    shift_reg[i+1] <= shift_reg[i];
                end
            end
        end
    end

    // Compute multiplications (combinational)
    always_comb begin
        for (i = 0; i < 63; i = i + 1) begin
            mult[i] = filt_consts[i] * shift_reg[i];
        end
    end

    // Sum all products (combinational)
    always_comb begin
        sum = 26'd0;
        for (i = 0; i < 63; i = i + 1) begin
            sum = sum + mult[i];
        end
    end

    // Output with scaling
    always_ff @(posedge CLK, negedge RSTN) begin
        if (!RSTN) begin
            out <= 10'd0;
        end else if (EN && !FILT_SHIFT) begin
            out <= sum >>> 8;  // Scale down (divide by 256 for Q1.8 format)
        end
    end

endmodule