# coinmover_bybit

## prerequisites:  

## running on Windows:   
1. unzip the file to the desired location   
2. go to that folder, open the config file in that directory and edit settings (you need at least to enter the API and SECRET key. You can also change the sleeptime (waiting time until next check), percentage move and discord webhook.  
3. unblock the executable (just like you did with wickhunter.exe).  
4. after all the steps are done, doubleclick the executable to run it.   


## running on Linux with Python:   
sudo apt install python3-pip  
pip install pybit  

adviced:  
apt install screen   

Bybit: Create an APIkey 

Copy coinmover_bybit.py and config.ini to your server OR login to you server and enter: wget https://github.com/elmontagne/coinmover_bybit/archive/refs/heads/main.zip   (after that: unzip main.zip).     

Then edit the config file (see below).  
When all configuration is done, you can run the script: python3 coinmover_bybit.py  
If your want to run the script in the backgroud while logged off, you can use 'screen'. within screen, start the script, then ctrl-a d to disconnect the screen. You can always return to this with 'screen -r'.  
First time the script is run, balance is retrieved and after the next cycle the profits will be moved.


## edit config file.  
edit config.ini , fill in:  
api key  
api secret  
percentage_move = percentage of profits to be moved to spot  
sleeptime = after how many minutes you want to run this again  
discord_webhook = your webhook if you want to use discord notifications 


Not done yet: 
maximum margin in use
cum_realised_pnl  
