from tracemalloc import start
import requests
import json
import sched, time

# ------------ CHANGE THIS ---------
startingMoney = 100000
moneyToSpend = 10000
btcBought = 0
lastBtcPrice = 0

def percentage(part, whole):
  # print(part, whole)
  if(part != 0):
    return 100 - (100 * float(part)/float(whole))
  else:
    return 0

def buyBtc(currentBtcPrice):
  global btcBought
  global startingMoney
  btcBought += (moneyToSpend / currentBtcPrice)
  startingMoney -= moneyToSpend

def sellBtc(currentBtcPrice):
  global btcBought
  global startingMoney
  btcBought -= (moneyToSpend / currentBtcPrice)
  startingMoney += moneyToSpend
# ------------ TO HERE ---------

# -------- DONT TOUCH THIS ---------
s = sched.scheduler(time.time, time.sleep)
def chronJob(sc):
# -------- DONT TOUCH THIS ---------

  # ------------ CHANGE THIS ---------
    global lastBtcPrice
    print("Checking BTC price to USD and writing to file...")
    # do your stuff
    
    f = open("responseExample.json", "w")

    # get current btc price 
    response = requests.get("https://poloniex.com/public?command=returnTicker")
    respJson = response.json()
    usdtToBtc = respJson["USDT_BTC"]
    currentBtcPrice = float(usdtToBtc['last'])

    # calculate change percentage
    priceVariance = percentage(lastBtcPrice, currentBtcPrice)
    print(priceVariance)
    if(priceVariance < -0.01):
      buyBtc(currentBtcPrice)

    if(priceVariance > 0.02):
      sellBtc(currentBtcPrice)

    f.write(json.dumps(usdtToBtc))
    f.close()

    if (lastBtcPrice != currentBtcPrice):
      lastBtcPrice = currentBtcPrice
    print(btcBought, startingMoney)
# ------------ TO HERE ---------

# -------- DONT TOUCH THIS ---------
    sc.enter(10, 1, chronJob, (sc,))
s.enter(0, 1, chronJob, (s,))
s.run()

