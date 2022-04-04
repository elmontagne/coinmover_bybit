#!/usr/bin/env python
# coding: utf-8

# In[ ]:
# Created by elmontagne
### author:  elmontagne
### discord: j.b.elmontagne#3234
### site:    https://github.com/elmontagne/coinmover_bybit

import configparser
import os.path
import time
from uuid import uuid4

import requests
from pybit import HTTP

config = configparser.ConfigParser()
config.read("config.ini")
botname = config["bybit_coinmover"]["botname"]
sleeptime = config["bybit_coinmover"]["sleeptime"]
apikey = config["bybit_coinmover"]["apikey"]
apisecret = config["bybit_coinmover"]["apisecret"]
discord_webhook = config["bybit_coinmover"]["discord_webhook"]
maxmargin = config["bybit_coinmover"]["maxmargin"]
percentage_move = config["bybit_coinmover"]["percentage_move"]

sleeptime = int(sleeptime) * 60

session = HTTP("https://api.bybit.com", api_key=apikey, api_secret=apisecret)
while True:
    currenttime = time.localtime()
    timenow = time.strftime("%I:%M:%S %p", currenttime)
    print(timenow, " Checking...")
    file_exists = os.path.isfile("status")
    if file_exists:
        with open("status", "r", encoding="UTF-8") as ff:
            old_pnl = ff.readline()
    else:
        with open("status", "w", encoding="UTF-8") as f:
            f.write("0")
            old_pnl = 0

    # print("Old balance: ",old_pnl)

    wallet = session.get_wallet_balance(coin="USDT")
    balance = wallet["result"]["USDT"]["equity"]
    pnl = wallet["result"]["USDT"]["cum_realised_pnl"]
    used_margin = wallet["result"]["USDT"]["used_margin"]
    print("Current balance: ", balance)
    print("Current PNL: ", pnl)
    marg = (float(used_margin) / float(balance)) * 100

    if float(old_pnl) != 0 and float(pnl) > float(old_pnl):
        profit = float(pnl) - float(old_pnl)
        print("we made profit:", profit)
        transfer = float(profit) * float(percentage_move) / 100
        if float(marg) <= float(maxmargin):
            print("transferring: ", transfer, " to SPOT ")
            transferred = session.create_internal_transfer(
                transfer_id=str(uuid4()),
                coin="USDT",
                amount=str(round(transfer, 2)),
                from_account_type="CONTRACT",
                to_account_type="SPOT",
            )
            status_message = (
                "**TRANSFER**: SUCCESS **account:** "
                + botname
                + " **totalBalance:** "
                + str(balance)
                + " **Profit:** "
                + str(profit)
                + " **transferred:** USDT "
                + str(transfer)
                + " to SPOT."
            )
        else:
            status_message = (
                "**TRANSFER**: FAILED **REASON:** Above maximum defined margin"
            )
    else:
        print("No profit this time: ", (float(pnl) - float(old_pnl)))
        status_message = (
            "**TRANSFER**: No profit this time: "
            + str(float(pnl) - float(old_pnl))
            + " **account**: "
            + botname
        )
    data = {"content": status_message}
    if discord_webhook != "":
        result = requests.post(discord_webhook, json=data)

    with open("status", "w", encoding="UTF-8") as f:
        f.write(str(pnl))
    print("Sleeping for ", sleeptime, "seconds")
    time.sleep(sleeptime)
