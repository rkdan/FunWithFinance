"""
Title: stockTrack.py
Author: R.K.Daniels
Created: 1 April, 2020
"""

#==================================================================================================
# Import statements
#==================================================================================================

import bs4
import requests
import ssl
import smtplib
import time
import numpy as np
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib.request import urlopen

from datetime import datetime

#==================================================================================================
# Stock lists
#==================================================================================================
# The list of stock codes that I currently own, and the list of other stock codes that I want to 
# keep track of.
OWNED_TICKER_LIST = ['NZX50', 'SPK', 'RYM', 'FRE', 'DIV', 'FNZ']
POWER_TICKER_LIST = ['NZX50', 'CEN', 'GNE', 'MCY', 'MEL', 'NWF', 'TLT', 'TPW', 'VCT']
#ENERGY_TICKER_LIST = []

#==================================================================================================
# Support functions
#==================================================================================================
def get_price_nzx50():
	"""
	Gets the current price of the NZX50 index and the percentage change from previous closing.
	-----
	Args:
		None

	Returns:
		points (int): The current total points.

		percent_change (float): The percentage change from the closing price of the previous
			day.
	"""
	url = 'https://www.nzx.com/markets/NZSX'
	try:
		page = urlopen(url)
	except:
		return 'Nan', 'Nan'   
	soup = bs4.BeautifulSoup(page,"html.parser")
	# Find the points and percentage information
	price_string = soup.find('ul',{'class': 'prices-snapshot-list left'}).find('li').text
	price_string = price_string.split('\n')
	price_string = price_string[2:4]
	i = 0
	for w in price_string:
		price_string[i] = w.strip()
		i += 1
	# Get the current points total
	points = price_string[0]
	points = int(points.replace(',', ''))
	# Get percetage change
	percent_change = price_string[1]
	percent_change = float(percent_change.replace('%',''))

	return points, percent_change


def get_stock_price(suffix):
	"""
	Gets the current price of the suffix index and the percentage change from previous closing.
	-----
	Args:
		suffix (str): The symbol of the stock to be found.

	Returns:
		price (int): The current price.

		percent_change (fl): The percentage change from the closing price of the previous
			day.
	"""
	url = 'https://www.nzx.com/instruments/' + suffix
	try:
		page = urlopen(url)
	except:
		return 'Nan', 'Nan'
	soup = bs4.BeautifulSoup(page,"html.parser")
	# Find the current price of the stock
	price_string = soup.find('div',{'class': 'small-12 medium-5 columns'}).find('h1').text
	price_string = price_string.strip()
	price = float(price_string.replace('$',''))
	# Find the percentage change
	percent_string = soup.find('div',{'class': 'small-12 medium-5 columns'}).find('span').text
	percent_string = percent_string[-6:]
	percent_change = float(percent_string.replace('%',''))

	return price, percent_change


def save_data(data_array, filename):
	try:
		saved_data = np.load(filename + '.npy')
		new_data = np.concatenate((saved_data, data_array),1)
		np.save(filename, new_data)
	except ValueError:
        # This only deals with ADDING a new stock code, not removing
		padding = np.zeros((1,len(saved_data[0,:,0]),2))
		saved_data_padded = np.concatenate((saved_data, padding))
		new_data = np.concatenate((saved_data_padded, data_array),1)
		np.save(filename, new_data)
	except FileNotFoundError:
		np.save(filename, data_array)


def send_email_update(points, percent_change, ticker):
	"""
	Sends an email to the desired email address from the stock update bot address.
	-----
	Args:
		points (fl): The current price of the stock.

		percent_change (fl): The percentage change from previous day close price.

		ticker (str) : The index code.

	Returns:
		None
	"""
	port = 465
	smtp_server = "smtp.gmail.com"
	sender_email = "stockupdatebot@gmail.com"
	receiver_email = "rkdaniels2209@gmail.com"
	password = "stockupdate"
	# Compose email
	message = MIMEMultipart()
	message['From'] = sender_email
	message['To'] = receiver_email
	message['Subject'] = "Stock Update"
	text = """\
	The ticker for %s has changed:

	Current: %d points
	Percentage change: %.2f%%

	""" % (ticker, points, percent_change)
	body = MIMEText(text, 'plain')
	message.attach(body)
	# Send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message.as_string())

#def get_data(ticker_list):
	
#==================================================================================================
# Run
#==================================================================================================
day_length = 2
owned_array = np.zeros((len(OWNED_TICKER_LIST),day_length,2))
power_array = np.zeros((len(POWER_TICKER_LIST),day_length,2))

current_minute = int(datetime.now().isoformat(sep='T', timespec='minutes')[-2:])
times = np.zeros((3))

i = 0
while i < day_length:
    start = time.time()
    times[i] = current_minute
	# Update general array
    j = 0
    for ticker in OWNED_TICKER_LIST:
        if ticker=='NZX50':
            price, percent_change = get_price_nzx50()
        else:
            price, percent_change = get_stock_price(ticker)
        owned_array[j,i,:] = price, percent_change
  		# INSERT EMAIL STUFF HERE PROBABLY
        j += 1
	# Update power company array
    j = 0
    for ticker in POWER_TICKER_LIST:
        if ticker=='NZX50':
            price, percent_change = get_price_nzx50()
        else:
            price, percent_change = get_stock_price(ticker)
        power_array[j,i,:] = price, percent_change
  		# INSERT EMAIL STUFF HERE PROBABLY
        j += 1
    end = time.time()
    print(end - start)
    i += 1
  	# We want to collect data at 60s time intervals, but the program takes some time interval 
  	# to run, we have to take that into account so that we get consistent timing of data.
    #print(owned_day_array)
    target_minute = (current_minute + 1)%60
    while current_minute != target_minute:
	    current_minute = int(datetime.now().isoformat(sep='T', timespec='minutes')[-2:])
	    time.sleep(20)

filename = "stockData"    
save_data(owned_array, filename)
filename = "powerData"
save_data(power_array, filename)
np.save("minutes.npy", times)



#send_email_update(points, percent_change, "NZX50")