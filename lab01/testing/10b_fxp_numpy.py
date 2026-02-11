import numpy as np

"""To test:
      - 10-bit FXP (16-bit word, 6-bits sign extend, 1-bit sign bit,
                    2-bits int, 7-bits frac)
      - Positive Values
         - Decimal to FXP
         - FXP to Decimal
      - Negative Values
         - Decimal to FXP
         - FXP to Decimal
"""

## Trying for +/-1.5 decimal
pos_d_result = 1.5
pos_b_result = np.int16(0b0011000000) # This works, so 10-bit to 16-bit SE is OK

"""Converts decimal to fxp, assumed 16 bit word or less (bad programming)
"""
def dec_fxp(n_frac, dec):
   val = dec
   val_scaled = (dec * np.pow(2, n_frac)).astype(np.int16)
   return val_scaled

assert dec_fxp(7, pos_d_result) == pos_b_result, "Failed: dec_fxp positive"
assert dec_fxp(7, -1*pos_d_result) == -1*pos_b_result, "Failed: dec_fxp negative"

"""Converts fxp to decimal, assumed above idk.
"""
def fxp_dec(n_frac, fxp):
   val = fxp.astype(float)
   val_scaled = val * 2**(-1*n_frac)
   return val_scaled

# print(f"{fxp_dec(7, pos_b_result)}")
assert fxp_dec(7, pos_b_result) == pos_d_result, "Failed: fxp_dec positive"
assert fxp_dec(7, -1*pos_b_result) == -1*pos_d_result, "Failed: fxp_dec negative"

# Checking filter conversion
import fir_TAP63_10b, fir_TAP63

print(fir_TAP63.filt_coeff)
filtc_dec = np.array(fir_TAP63.filt_coeff)

filtc_fxp = np.array(fir_TAP63_10b.filt_coeff)
filtc_fxp_dec = fxp_dec(9, filtc_fxp)

# for i, c in enumerate(filtc_fxp_dec):
#    if round(filtc_dec[i], 3) != round(c, 3):
#       print(f"i:{i}, c:{c}, dec:{filtc_dec[i]}, diff={filtc_dec[i]-c}")


# for i, c in enumerate(np.array(filtc_dec*2**9)):
#    if filtc_fxp[i] != c:
#       print(f"i:{i}, fxp:{filtc_fxp[i]}, c:{c}, diff:{filtc_fxp[i]-c}, c_rounded:{round(c, 0)}, rounded_diff={filtc_fxp[i]-round(c,0)}")

print(filtc_dec[30])
print(filtc_fxp[30]*(2**-9))

print("check convert from dec to fxp vs. fxp")
for i, c in enumerate(np.round(np.array(filtc_dec*2**9))):
   if filtc_fxp[i] != c:
      print(f"i:{i}, fxp:{filtc_fxp[i]}, c:{c}, diff:{filtc_fxp[i]-c}")

print("check convert from fxp to dec vs. fxp")
for i, c in enumerate(np.round(np.array(filtc_dec*2**9))):
   if filtc_fxp[i] != c:
      print(f"i:{i}, fxp:{filtc_fxp[i]}, c:{c}, diff:{filtc_fxp[i]-c}")