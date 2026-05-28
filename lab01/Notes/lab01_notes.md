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
#2 implement in verilog [DONE]
   - implement convolution
      - implement MAC
      - implement conv
   - filter coefficients: either get 10-bit fxp from site, or just scale.
#3 compare TB results to Python [DONE]
   - data coming out of TB will be (?) 10-bit Fxp
   - data in python is decimal
   - want to compare Fxp to Fxp or decimal to decimal
   - in the end, decimal-to-decimal easier for graph.

FIR -> group delay

*** ^ old notes ^ ***

*** TO FIX EVERYTHING AND CHECK MY RESULTS ARE OK ***
1. [x] Produce filter taps that are in the Q1.8 format
    - [x] Make proper float to fxp and fxp to float functions
    - [x] Take from TFilter website
    - [x] Produce own to ensure that my conversion function is OK.
2. [x] Produce input data (sum of sins) in the Q1.8 format
3. [x] Check result vs. reference both RTL and Python
4. [x] Clean up Python
    - [x] Convert floating results to Q1.8
    - [Not Needed] Make a new graph: 3 subplots, 1. floating sum, 2. fxp sum, 3. overlay
    - [x] Redo function graph result_conv_overlay.png to not be awful
    - [x] Have input data in Q1.8
    - [x] Stop having to copy paste manually, have the script also run when Python is ran for the comparison
        - Instead of having the Python run iverilog/Makefile, I modified
          the Makefile to run the Python. Run both with one command.
5. [x] Run on RTL again, check
6. [x] Compare RTL results vs. Python with graphs
7. [x] Compare RTL results vs. Python via RMS for sig number
8. [x] Fix RTL to load in filter constants.


[x] Convert python or convert RTL to float and compare
    - fix tb to give more than 160 values for comparison?
    - add interpolation?
[x] fix filter taps...
    - wtf????? the actual values are borked vs the ones i got from scipy generation...
    - confusion 5/20 10:08 PM
        - i think my work is right, but the TAPs from the original FIR filter site are broken?
        - filter_taps currently (using generated conversion) gives borked output filter result
        - filter_taps_unknown gave the best, but was from generated scipy
        - test_taps looks good, uses my own conversion, but output value are scaled?
    - realization: I had a massive misunderstanding of how to represent my fixed point.
        - If our input signal has a maximum range of +/- 2
        - Then 1 signed bit, 1 integer bit should be sufficient in representing the data.
        - This way, max value is +1(all frac bits?)
        - Thus, the number of fractional bits is 8, not 9
        - The notation is written: Q2.8, as 2 bits are used for the sign/integer, 8 for the fractional.
[x] Make graph taking output of recovered s400 in python, comparison
[Not Needed] Graph Output of s400_500 but FXP, aka the input signal
[x] compare RTL output vs. python
[Yes, but only did abs. mean] obtain RMS difference with dB attenuation of RTL vs. Python
[x] Rewrite SV in preparation for loading in filter constants via shift register for Lab 2 and on.

Notes 5/22 @ 9:32 PM
- Understanding of what's happened
    - TFilter's output for fixed point assumes for the value n for "fixed point precision of taps"
      that 1 bit is for sign, 0 bits are for the integer part, and n-1 bits are for the fractional part.
        - Thus, for n=10, TFilter's output values are for: Q1.9, so there are 9 fractional bits.

    - However, my interpretation was that because the input signal has a max/min decimal value of +/-2
      (summing two sinusoids which both have amplitudes=1 mean at most 1+1=2), my fixed point representation
      would be like so for the given 10-bit fields determined by the lab01 guidelines:
        - Sign: 1 bit, Integer Part: 1 bit, Fractional Part: 8 bits
        - AKA: Q2.8 for 2 bits for sign and integer, 8 bits for fractional

    - Therefore, this is where the discrepency begins. I thought what was 'n' for TFilter was the
      number of fractional bits. Instead, it is the total bits, sign and fractional bits.
        - To see the problem, the example I'll use is what I originally thought n was for.
        - My assumption is n=8, as I have 8 fractional bits from my fixed point representation.
        - TFilter input n=8, so number of bits for fraction TFilter has is:
            - Sign: 1 bit, Integer Part: 0 bits, Fractional Part: n-1 = 8-1 = 7 BITS
        - However, as seen above, my interpretation is that it is Q2.8, meaning:
            - Sign: 1 bit, Integer Part: 2 bits, Fractional Part: 8 BITS. 
        - I HAVE AN ADDITIONAL FACTOR OF TWO, AN EXTRA FRACTIONAL BIT.

    - To continue with another example, for n=10, which is a 10-bit field:
        - TFilter for n=10 means that m=9 fractional bits, there are 9 BITS FOR FRACTION
            - Sign: 1 bit, Integer Part: 0 bits, Fractional Part: 9 bits
        - My desired Fxp representation:
            - Sign: 1 bit, Integer Part: 2 bits, Fractional Part: 8 BITS.

    - SO FOR n=8 or n=10, THEY BOTH DON'T MATCH WHAT I WANT. Need to set n=9 on website.
        - TFilter for n=10 means that m=9 fractional bits, there are 9 BITS FOR FRACTION
            - Sign: 1 bit, Integer Part: 0 bits, Fractional Part: 8 bits
        - My desired Fxp representation:
            - Sign: 1 bit, Integer Part: 2 bits, Fractional Part: 8 BITS.
                
    - THIS IS CORRECT NOW! Why?
        - Because converting floating to Fxp is: clip(round(float * 2^m))
        - And converting Fxp to floating is:     fxp / 2^m
        - Which means that the number of bits for the integer part doesn't matter!
        - Only the number of fractional bits needs to match to ensure correct conversion!!!

    - im wrong again. Qm.n means assumed 1 bit for sign, m for integer, n for fractional.
    - Therefore, Q1.8 is correct to represent 10-bit, 1 sign, 1 int, 8 frac.