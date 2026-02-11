## Decimal to Fxp (10-bit, 1 signed, 2 int, 7 frac)
# lets say 1 + 0.5 = 1.5
d_result = 1.5
b_result = 0b0011000000

# The number we work with is 10-bit fxp.
# The decimal result is that 10-bit fxp -> scaled by 2^(-n_frac)
# Thus, for decimal to fxp, it's decimal scaled by 2^(n_frac)
# Then take that scaled result, and 2s complement it.

## DEC TO FXP
d_scaled = int(1.5 * int(2**7))
print(d_scaled)

# IDEA???
# in fxp -> (-1)^0 * [0*2^1 + 1*2^0 + 1*2^(-1) + 0 ...]
#        -> 0b|0|01|100 0000
#             s|int|frac

# Checking DEC to FXP
str_b = format(d_scaled, '010b')
print(f"str_b={str_b}")
assert d_scaled == b_result, "Failed check dec to fxp for 1.5"
## FXP to DEC
b_scaled = b_result * 2**(-7)
print(f"b_scaled={b_scaled}")
assert b_scaled == d_result, "Failed check fxp to dec for 1.5"

## Signed
neg_d_result = -1.5
neg_b_result = 0b1011000000

neg_d_scaled = int(neg_d_result * int(2**7))

# Checking DEC to FXP
neg_str_b = format(neg_d_scaled, '010b')
# print(f"check signed bit for neg_str_b={neg_str_b[0]}")
# print(f"neg_str_b={neg_str_b}")
# print(f"negative check dec to fxp for 1.5: {neg_d_scaled == neg_b_result}")

## FXP to DEC
neg_b_scaled = neg_b_result * 2**(-7)
print(f"neg_b_scaled={neg_b_scaled}")
# print(f"negative check fxp to dec for 1.5: {neg_b_scaled == neg_d_result}")


## ------------------------------------------------------------
## DONE WITH THIS EXAMPLE.
## Example from slides: 5.07397461 in dec = 0b0101000100101111
# 12 bits frac, 1 bit signed, 3 bits int, 16 bit word
## DECIMAL TO FXP
ex_d_orig = 5.07397461
ex_d_scaled = int(ex_d_orig * 2**12)
expected_b_result = 0b0101000100101111

# Format 16-bit word
# i hate everything being strings GRAHHHH WTF WHY PYTHON
# GIVE ME EASY BIT MANIPULATION WITHOUT DEPENDENCIES
print(ex_d_scaled)
ex_b = format(ex_d_scaled, '016b')
print(f"{ex_b}, len={len(ex_b)}")
print(f"sign bit:{ex_b[0]}, int bits:{ex_b[1:4]}, \
      frac bits:{ex_b[4:16]}")
# Best way without strings
assert ex_d_scaled == expected_b_result, "Failed Example Test (ex_d_scaled)"
assert ex_b == format(expected_b_result, '016b'), "Example test (ex_b)"

# FXP TO DECIMAL
ex_b_scaled = expected_b_result * 2**(-12)
print(ex_b_scaled)
assert ex_b_scaled == ex_d_orig, "Example test (fxp to decimal)"
assert round(ex_b_scaled, 8) == ex_d_orig, "Example test (fxp to decimal), rounded"
