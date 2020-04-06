"""
Created: Mon Apr  6 14:15:52 2020

Written by: R.K.DANIELS
"""

OWNED_TICKER_LIST = ['NZX50', 'SPK', 'RYM', 'FRE', 'DIV', 'FNZ']

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')

# Load in data from saved file

# At this stage we'll play with fake data
data = np.random.rand(6,406,2)
# =============================================================================
# 
# nzx50 = data[0,:,:]
# nzx50_price = nzx50[:,0]
# 
# spk = data[1,:,:]
# spk_price = spk[:,0]
# =============================================================================

# =============================================================================
# b = 0.0
# for i in range(len(nzx50_price)):
# 	nzx50_price[i] = nzx50_price[i] + b
# 	spk_price[i] = spk_price[i] + b/2
# 	b += 0.01
# =============================================================================
	
	
	
plt.figure()
i = 0
for ticker in OWNED_TICKER_LIST:
	ticker_data = data[i,:,:]
	price = ticker_data[:,0]
	plt.plot(price, 'x', label=ticker)
	i += 1
	
plt.legend()
plt.show()