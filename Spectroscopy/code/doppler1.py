import pandas as pd
from pandas import concat
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import LinearNDInterpolator
# from scipy import asarray as ar, exp



def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


df = pd.read_csv('data/doppler1.csv', header=11, index_col=False)

#noise filter??


#find the ramp interpolation 
xmasked = concat([df.loc[0:400,"Second"], df.loc[1000:2300,"Second"], df.loc[3100:3500, "Second"]], axis=0)       #xrange
ymasked = concat([df.loc[0:400,"Volt.1"], df.loc[1000:2300,"Volt.1"], df.loc[3100:3500, "Volt.1"]], axis=0)       #yrange
nr = df.loc[0:3500, "Second"]
ramp = np.interp(nr, xmasked, ymasked)

linsig = df.loc[0:3500, "Volt.1"] - ramp



# plt.plot(nr, ramp, 'b+')
plt.plot(nr, df.loc[0:3500, "Volt.1"])
plt.plot(nr, linsig)
# plt.xlim(df.loc[0, "Second"], df.loc[len(df["Second"]) - 1, "Second"])
plt.xlim(df.loc[0, "Second"], df.loc[3500, "Second"])
plt.ylim(-0.3, 0.3)
# plt.show()

#### D1 first peak ####
x = df.loc[400:700,"Second"]
y = linsig.loc[400:700]

mean = sum(x*y)/sum(y)                   
sigma = np.sqrt(sum(y*(x-mean)**2)/sum(y))    

popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')

#### D1 second peak ####
x = df.loc[700:1000,"Second"]
y = linsig.loc[700:1000]

mean = sum(x*y)/sum(y)                   
sigma = np.sqrt(sum(y*(x-mean)**2)/sum(y))    

popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')


#### D1 third peak ####
x = df.loc[2550:2850,"Second"]
y = linsig.loc[2550:2850]

mean = sum(x*y)/sum(y)                   
sigma = np.sqrt(np.abs(sum(y*(x-mean)**2)/sum(y)))    

popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')


#### D1 fourth peak ####
x = df.loc[2850:3100,"Second"]
y = linsig.loc[2850:3100]

mean = sum(x*y)/sum(y)                   
sigma = np.sqrt(sum(y*(x-mean)**2)/sum(y))    

popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')


# plt.title('Fig. 3 - Fit for Time Constant')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.show()