from machine import I2C,RTC,Pin
import machine
import time
import ssd1306
import ntptime
import json
import urequests


i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)  #Init i2c
lcd=ssd1306.SSD1306_I2C(128,64,i2c)             #create LCD object,Specify col and row
led=Pin(2, Pin.OUT)
x=ntptime.settime()

if station.isconnected()==True:
 lcd.text("Online!",2,1)

 lcd.text(str(station.ifconfig()[0]),0,23)
 
else:
 lcd.text("Connecting..",2,1)
lcd.show()
time.sleep(3)
 
stocks=['ACB','BPMX','CGC','PULM','TSLA']
city=['5036493','1261481','1263214']
cityid=','.join(city)
stocksid=','.join(stocks)
wthapp="youropenweathermapapikey"
stkapp="yourworldtradingdataapikey"

up_weather=0
up_stock=0
up_curr=0
prevbtc=8000

Name=[None]*len(stocks)
Symbol=[None]*len(stocks)
Live=[None]*len(stocks)
highlow=[None]*len(stocks)
change=[None]*len(stocks)
changepct=[None]*len(stocks)
city=[None]*len(city)
tmp=[None]*len(city)
wind=[None]*len(city)
hum=[None]*len(city)
minmax=[None]*len(city)
desc=[None]*len(city)

while True:
  lcd.fill(0)
  lcd.show()
  led(0)
  c = time.localtime(x)
  if time.time()-up_weather>300:
    lcd.text("Updating Weather",0,10) 
    lcd.show()
    try:
     r = urequests.get("http://api.openweathermap.org/data/2.5/group?id={cityid}&units=imperial&appid={wthapp}".format(wthapp=wthapp,cityid=cityid)).json()
    except (urequests.exceptions.RequestException) as err:
     continue 
    for i in range(len(city)):
      city[i]=r["list"][i]["name"]
      tmp[i]= "TEMP:" + str("%.0f" %(r["list"][i]["main"]["temp"]))+" F"
      wind[i]="Wind:" + str("%.0f" %r["list"][i]["wind"]["speed"])
      hum[i]="RH:" + str(r["list"][i]["main"]["humidity"])+"%"
      minmax[i]="Min:" +str("%.0f" %r["list"][i]["main"]["temp_min"]) + " Max:" + str("%.0f" %r["list"][i]["main"]["temp_max"])
      desc[i]=r["list"][i]["weather"][0]["description"]
    up_weather=time.time()
    r=0
    
  if time.time()-up_stock>600:
    lcd.text("Updating Stocks",0,30) 
    lcd.show()
    try:
     r = urequests.get("https://www.worldtradingdata.com/api/v1/stock?symbol={stocksid}&api_token={stkapp}".format(stocksid=stocksid,stkapp=stkapp)).json()
    except (urequests.exceptions.RequestException) as err:
     continue 
    for i in range(len(stocks)):
      Name[i]= r["data"][i]["name"]
      Symbol[i]= r["data"][i]["symbol"]
      Live[i]= ":"+str(r["data"][i]["price"])
      highlow[i]="H:" + str(r["data"][i]["day_high"]) + " L:" + str(r["data"][i]["day_low"])
      change[i]=r["data"][i]["day_change"]
      changepct[i]=r["data"][i]["change_pct"]
    up_stock=time.time()
    r=0
    
  if time.time()-up_curr>900:
    lcd.text("Updating Crypto",0,50)
    lcd.show()
    try:
     r = urequests.get("https://www.worldtradingdata.com/api/v1/forex?base=USD&sort=newest&api_token={stkapp}".format(stkapp=stkapp)).json()
    except (urequests.exceptions.RequestException) as err:
     continue 
    INR="INR:"+str(round(float(r["data"]["INR"]),2))
    currinr=round(float(r["data"]["INR"]),2)
    currbtc=round(1/float(r["data"]["BTC"]),2)
    chgbtc=(currbtc-prevbtc)/currbtc
    prevbtc=currbtc
    EUR="EUR:"+str(round(1/float(r["data"]["EUR"]),2))
    BTC="BTC:"+str(round(1/float(r["data"]["BTC"]),2))
    ETH="ETH:"+str(round(1/float(r["data"]["ETH"]),2))
    BCH="BCH:"+str(round(1/float(r["data"]["BCH"]),2))
    up_curr=time.time()
    r=0
    
  # Display weather data for 10 sec
  for i in range(len(city)):  
   lcd.fill(0)
   lcd.show()
   lcd.text(city[i],25,0)
   lcd.rect(0,8,128,50,1)    
   lcd.text(desc[i].upper(),2,13) 
   lcd.text(tmp[i],2,23)
   lcd.text(hum[i],64,43)
   lcd.text(wind[i],2,43)
   lcd.text(minmax[i],2,33)
   lcd.show()                                      
   time.sleep(5)
   
  # Display current crypto prices
  lcd.fill(0)
  lcd.show()
  lcd.text("FOREX/CRYPTO",15,0)
  lcd.rect(0,8,128,54,1)
  lcd.text(INR,1,10)
  lcd.text(EUR,1,20)
  lcd.text(BTC,1,30)
  lcd.text(ETH,1,40)
  lcd.text(BCH,1,50)
  lcd.show()
  if currinr>70 or currinr<68 or chgbtc>0.5 or chgbtc<-0.5:
    for i in range(10):
      led(1)
      time.sleep(0.2)
      led(0)
      time.sleep(0.2)
  time.sleep(10)

  # Display Stock data and iterate thru the list 
  for i in range(len(stocks)):
    lcd.fill(0)
    lcd.show()
    lcd.text("STOCKS LIVE",15,0)
    lcd.rect(0,8,128,50,1)
    lcd.text(Name[i],1,13)
    lcd.text(Symbol[i]+Live[i],1,23)
    lcd.text(highlow[i],1,33)
    lcd.text("%change:" + str(changepct[i]),1,43)
    lcd.show()
    try:
      chpct=float(changepct[i])
    except (ValueError,TypeError):
      chpct=0
    if chpct>4.99 or chpct<-4.99:
     for j in range(10):
      led(1)
      time.sleep(0.2)
      led(0)
      time.sleep(0.2)
    time.sleep(5)


