Inputs to FIR filter, 2 sinusoids:
    1. 400 Hz, Amp: 1
    2. 500 Hz, Amp: 1

Therefore, it is only possible to have a maximum amp. of 2.
    - For a 10-bit fixed-point (fxp) signal representation...
        1. want it signed (1-bit)
        2. integer values only 0 to 2, so 2-bits
    - Thus: 1-bit signed, 2 bits for int, and 7 bits for fractional parts
    
    - to convert from decimal to fxp, its Number -> * 2^(number of fractional bits) -> 2s comp
    - other way around from fxp to decimal -> 2s comp -> 2^(-number of fractional bits)
    
[TODO]
#1 Implement filter in python (MATPLOTLIB)
#2 implement in verilog
    - implement convolution
        - implement MAC
        - implement conv
#3 compare TB results to Python

FIR -> group delay
