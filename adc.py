import spidev
import os
import time
import matplotlib
import numpy as np
import os
import pandas as pd
from flask import Flask, render_template, request

#app = Flask(__name__)

matplotlib.use('Agg')

import pylab as plt

i=0

spi = spidev.SpiDev()
spi.open(0,0)	
#spi.max_speed_hz=(4600000)

def ReadADC(ch):
	if((ch > 7) or (ch < 0)):
		return -1
	adc = spi.xfer2([1,(8+ch)<<4,0])
	data = ((adc[1]&3)<<8) + adc[2]
	return data

def ReadVolts(data,deci):
	volts = (data * 3.3) / float(1023)
	volts = round(volts,deci)
	return volts

ch0 = 0
ch1 = 1

x = np.arange(0,100,0.01)
y0 = np.zeros_like(x)
y1 = np.zeros_like(x)
y = [0]*10000

last = time.time()
for i in range(0,9999):
        adc = spi.xfer2([1,(8+ch0)<<4,0],7692000)
        data = ((adc[1]&3)<<8) + adc[2]
        y[i] = data
        i=i+1

current = time.time()
print(current-last)

#print(y)

signal = {'ch0':y,'ch1':y1}
df = pd.DataFrame(signal)
savepath = os.getcwd()
df.to_csv(os.path.join(savepath,'fansignal.csv'))


plt.plot(x,y)
plt.savefig('fansignal.png')
plt.clf()

#@app.route("/")
#def hello():
#	return render_template("adc.html")

#if __name__ == "__main__":
#	app.run(host='0.0.0.0', debug=True)
