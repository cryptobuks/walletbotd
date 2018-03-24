# walletbotd

walletbotd is a Telegram bot that allows you to remotely control any cryptocurrency wallet you have running at home, through a simple chat interface from anywhere in the world.

Because of this, it needs to be run aside of a \*coind daemon. It will execute queries directly to your -coind daemon, sending data back and forth with you through Telegram.


In short, the steps to run walletbotd (assuming you already have a wallet running), are:
```
git clone https://github.com/nexus166/walletbotd
cd walletbotd
sudo pip3 install -r requirements.txt
cp wbdconf.py.template wbdconf.py # Edit wbdconf.py!
python3 wbd.py
```

![1](https://user-images.githubusercontent.com/9354925/37871696-97be9740-2ff4-11e8-82ec-f19e5262053f.jpg)



Command list:
```
/info - get generic information about your wallet,

/wallet - display active accounts in your wallet,

/account - display detailed info about an account,
  `/account myaccount1`

/newaccount - create a new account in your wallet,
  `/newaccount mynewaccount2`

/unlock - unlocks your wallet for two minutes to send coins,
  `/unlock mysupersecretwalletpassword`

/send - send MintCoin from automatically selected inputs,
  `/send Mpr3zWUEZrowiKC5dwJanq5faenUzR613L 100000`

/advsend - send MintCoin from a specific account,
  `/advsend myaccount2 Mpr3zWUEZrowiKC5dwJanq5faenUzR613L 100000`
  
/move - move MintCoin from a specific account to another within your wallet,
  `/move myaccount1 myaccount2 100000`

/help - this helper you see right now.
```





![3](https://user-images.githubusercontent.com/9354925/37871694-978f29ec-2ff4-11e8-8fda-381a20c96e9a.jpg)
![2](https://user-images.githubusercontent.com/9354925/37871695-97a6c26e-2ff4-11e8-9de7-257b7cfeff57.jpg)



Credits @enlil0 (telegram)

Contributions (in form of pull requests) are as welcome as donations:
```
BTC > 171Ey4apVsHzdVpQ92TJDAKpqUK7Zb9s43
DOGE > DKorffb2C1wB4bE6ZBdY89vxL9Wq181MPQ
VTC > VimCCV3PcqRuqQy3z8i2joX4XauNEeVRcq
MINT > MqTi9dbapN4T7J7SUZns3zzXKq637H1Syj
TZC > TobmK56ayekd1y5jiTYti4czVwobKBM1hn
```
