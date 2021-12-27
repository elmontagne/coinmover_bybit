# coinmover_bybit

## prerequisites:  
sudo apt install python3-pip  
pip install pybit  

adviced:  
apt install screen   

Bybit: Create an APIkey 

## installation:  
Copy coinmover_bybit.py and config.ini to your server OR login to you server and enter: wget https://github.com/elmontagne/coinmover_bybit/archive/refs/heads/main.zip   (after that: unzip main.zip).     
edit config.ini , fill in:  
api key  
api secret  
percentage_move = percentage of profits to be moved to spot  
sleeptime = after how many minutes you want to run this again  
discord_webhook = your webhook if you want to use discord notifications 

When all configuration is done, you can run the script: python3 coinmover_bybit.py  
If your want to run the script in the backgroud while logged off, you can use 'screen'. within screen, start the script, then ctrl-a d to disconnect the screen. You can always return to this with 'screen -r'.  
First time the script is run, balance is retrieved and after the next cycle the profits will be moved.

Not done yet: 
maximum margin in use
cum_realised_pnl  
