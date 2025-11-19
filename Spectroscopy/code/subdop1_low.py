import pandas as pd
from pandas import concat
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import LinearNDInterpolator
from scipy.signal import find_peaks


df = pd.read_csv('data/S1_BIG.csv', header=11, index_col=False)

rstart = 2800
rstop  = 3650
yrang = 2.2

#find the ramp interpolation 
xmasked = concat([df.loc[rstart:3000,"Second"], df.loc[3500:rstop, "Second"]], axis=0)       #xrange
ymasked = concat([df.loc[rstart:3000,"Volt.2"], df.loc[3500:rstop, "Volt.2"]], axis=0)       #yrange
nr = df.loc[rstart:rstop, "Second"]
ramp = np.interp(nr, xmasked, ymasked)

# plt.plot(nr, ramp)

# Compute T = I/I0
T = df.loc[rstart:rstop, "Volt.2"] / ramp

plt.plot(nr, np.emath.log(T))

# finding local minima of the function ln(T)
peaks, properties = find_peaks(- np.emath.log(T), width=10)
peaks += rstart

# for p in peaks:
#     plt.scatter(df.loc[p, "Second"], np.emath.log(T.loc[p]))

min1 = [peaks[0], peaks[1]] #minima of first dip
min2 = [peaks[2], peaks[3]] #minima of second dip

#finding peak in the first absorbtion peak
peaks, properties = find_peaks(np.emath.log(T.loc[min1[0]:min1[1]]), width=5)
max1 = peaks + min1[0]
plt.scatter(df.loc[max1[0], "Second"], np.emath.log(T.loc[max1[0]]))


#finding peak in the first absorbtion peak
peaks, properties = find_peaks(np.emath.log(T.loc[min2[0]:min2[1]]), width=5)
max2 = peaks + min2[0]

plt.scatter(df.loc[max2[0], "Second"], np.emath.log(T.loc[max2[0]]))

plt.show()
