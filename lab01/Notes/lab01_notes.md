Inputs to FIR filter, 2 sinusoids:
    1. 400 Hz, Amp: 1
    2. 500 Hz, Amp: 1

Therefore, it is only possible to have a maximum amp. of 2.
    - For a 10-bit fixed-point (fxp) signal representation...
        1. want it signed (1-bit)
        2. integer values only 0 to 1, so 1-bit
    - Thus: 1-bit signed, 1 bit for int, and 8 bits for fractional parts
    - Why? Because to reach a max decimal value of 2 in fxp is just:
      - 0 for the signed bit, 1 for the integer bit, and 0xF for the fractional part
      - Which is approximately 2 (in reality in decimal: 1 + 0.99 something close to 1)
    
    - to convert from decimal to fxp, its Number -> * 2^(number of fractional bits) -> 2s comp
    - other way around from fxp to decimal -> 2s comp -> 2^(-number of fractional bits)
    
[TODO]
#1 Implement filter in python (MATPLOTLIB) [DONE]
   - exploring verification with FXP, also how scaling works with fxp (im dumb)
   - realizing im probably the problem, trying to force an interpretation onto python's systems.
      - solution: work in numpy. has unsigned and signed. therefore, even though we want 10-bit words, work in 16-bit words (numpy only supports standard word sizes)
         - deal with it using sign extension
#2 implement in verilog
   - implement convolution
      - implement MAC
      - implement conv
   - filter coefficients: either get 10-bit fxp from site, or just scale.
#3 compare TB results to Python
   - data coming out of TB will be (?) 10-bit Fxp
   - data in python is decimal
   - want to compare Fxp to Fxp or decimal to decimal
   - in the end, decimal-to-decimal easier for graph.

FIR -> group delay
