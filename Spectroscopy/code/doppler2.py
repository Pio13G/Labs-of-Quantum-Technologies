import pandas as pd
from pandas import concat
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import LinearNDInterpolator
# from scipy import asarray as ar, exp

rstart = 1800
rstop  = 5400
yrang = 2.2

def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


df = pd.read_csv('data/doppler2.csv', header=11, index_col=False)

#noise filter??

#go from time to freq using the michelson

#find the ramp interpolation 
xmasked = concat([df.loc[rstart:2250,"Second"], df.loc[2900:4450,"Second"], df.loc[5050:rstop, "Second"]], axis=0)       #xrange
ymasked = concat([df.loc[rstart:2250,"Volt.1"], df.loc[2900:4450,"Volt.1"], df.loc[5050:rstop, "Volt.1"]], axis=0)       #yrange
nr = df.loc[rstart:rstop, "Second"]
ramp = np.interp(nr, xmasked, ymasked)

linsig = df.loc[rstart:rstop, "Volt.1"] - ramp



# plt.plot(nr, ramp, 'b+')
plt.plot(nr, df.loc[rstart:rstop, "Volt.1"])
plt.plot(nr, linsig)
# plt.xlim(df.loc[0, "Second"], df.loc[len(df["Second"]) - 1, "Second"])
plt.xlim(df.loc[rstart, "Second"], df.loc[rstop, "Second"])
plt.ylim(-yrang, yrang)
# plt.show()

#### D1 first peak ####
x = df.loc[2250:2600,"Second"]
y = linsig.loc[2250:2600]

mean = sum(x*y)/sum(y)                   
sigma = np.sqrt(sum(y*(x-mean)**2)/sum(y))    

popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

# plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')


# #### D1 second peak ####
x = df.loc[2600:2900,"Second"]
y = linsig.loc[2600:2900]

mean = sum(x*y)/sum(y)                   
sigma = np.sqrt(sum(y*(x-mean)**2)/sum(y))    

popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

# plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')


# #### D1 third peak ####
x = df.loc[4450:4750,"Second"]
y = linsig.loc[4450:4750]

mean = sum(x*y)/sum(y)                   
sigma = np.sqrt(np.abs(sum(y*(x-mean)**2)/sum(y)))    

popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

# plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')


# #### D1 fourth peak ####
x = df.loc[4750:5050,"Second"]
y = linsig.loc[4750:5050]

mean = sum(x*y)/sum(y)                   
sigma = np.sqrt(sum(y*(x-mean)**2)/sum(y))    

popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

# plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')


# # plt.title('Fig. 3 - Fit for Time Constant')
# plt.xlabel('Time (s)')
# plt.ylabel('Voltage (V)')
plt.show()