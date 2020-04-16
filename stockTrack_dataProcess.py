"""
Created: Mon Apr  6 14:15:52 2020

Written by: R.K.DANIELS
"""

OWNED_TICKER_LIST = ['NZX50', 'SPK', 'RYM', 'FRE', 'DIV', 'FNZ']
POWER_TICKER_LIST = ['NZX50', 'CEN', 'GNE', 'MCY', 'MEL', 'NWF', 'TLT', 'TPW', 'VCT']

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')

def moving_average(x, w):
	return (np.convolve(x, np.ones(w), 'valid')/w)

# Load in data from saved file
data = np.load("powerData.npy")
#data = data[1:6]	
plt.figure()
i = 0
for ticker in POWER_TICKER_LIST:
	ticker_data = data[i]
	price = ticker_data[:,0]
	# Clean data of Nans
	for elem in range(len(price)):
		if str(price[elem]) == 'nan':
			price[elem] = price[elem-1]
	normalized_price = (price - np.min(price)) / (np.max(price) - np.min(price))
	if ticker=='NZX50':
		plt.plot(normalized_price, label=ticker, linewidth=6, alpha=0.2)
	else:
		plt.plot(normalized_price, label=ticker)
	i += 1
	
plt.legend()
plt.show()