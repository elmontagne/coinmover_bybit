#!/usr/bin/env python
# coding: utf-8

# In[ ]:
# Created by elmontagne
### author:  elmontagne
### discord: j.b.elmontagne#3234
### site:    https://github.com/elmontagne/coinmover_bybit

from pybit import HTTP
from uuid import uuid4
import time
import os.path
import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')
sleeptime = config['bybit_coinmover']['sleeptime']
apikey = config['bybit_coinmover']['apikey']
apisecret = config['bybit_coinmover']['apisecret']
discord_webhook = config['bybit_coinmover']['discord_webhook']
maxmargin = config['bybit_coinmover']['maxmargin']
percentage_move = config['bybit_coinmover']['percentage_move']

sleeptime = int(sleeptime)*60

session = HTTP("https://api.bybit.com",
               api_key=apikey, api_secret=apisecret)
while True:
    currenttime = time.localtime()
    timenow = time.strftime("%I:%M:%S %p", currenttime)
    print(timenow," Checking...")
    file_exists = os.path.isfile('status')
    if file_exists:
        with open('status', 'r') as ff:
            old_balance=ff.readline()
    else:
        f = open("status","w")
        f.write("0")	
        old_balance=0

    print("Old balance: ",old_balance)	
 
    wallet = session.get_wallet_balance(coin="USDT")
    balance = wallet['result']['USDT']['equity']
    print("Current balance: ",balance)

    if float(old_balance) != 0 and float(balance) > float(old_balance):
        profit = float(balance) - float(old_balance)
        print("we made profit:",profit)
        transfer = float(profit) * float(percentage_move) / 100
        print("transferring: ",transfer, " to SPOT ")
        transferred = session.create_internal_transfer(transfer_id=str(uuid4()),coin="USDT",amount="1",from_account_type="CONTRACT",to_account_type="SPOT")
        status_message = "Transferred: USDT "  + str(transfer) + " to SPOT."
    else:
        print("No profit this time: ", (float(balance) - float(old_balance)))
        status_message = "No profit this time: "+str(float(balance) - float(old_balance))
    data = {
   "content" : status_message
}
    if discord_webhook != '':
        result = requests.post(discord_webhook, json = data)



    with open('status', 'w') as f:
        f.write(str(balance))
    print("Sleeping for ",sleeptime,"seconds")
    time.sleep(sleeptime)
