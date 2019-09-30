# Weather, Stocks and Crypto Ticker using Wemos D1 mini and SSD1306 OLED screen

## Ticker in action

![Booting up](boot.gif)

![Showing Data](Ticker.gif)


This project was built in part as a means to learn micropython which is basically a subset of python with limited libraries.
Eventually, I found it pretty useful as a standalone device showing current weather and stock prices without having to pick up the phone or open a browser on my desktop.

The tiny 1" display shows:

1. Weather for mutiple cities
2. Crypto or forex prices of your choice
3. Cycle thru 5 chosen stock prices - current price, min /max, % change

The device also has a small red LED which lights up if a particular stock has changed by 5% or more, Or if a forex of your choice has changed more than a particular threshold (e.g., bitcoin changed more than $500)

The code is customizable and you can use your own cities, stocks and forex trade.

You'd have to register for free API keys on Worldtradingdata.com and openweathermap.com
World Trading allows 250 calls in 24 hrs for a free acocunt. the code handles this by restricting the calls every 15 mins or so.
You can change this to update more frequently if you do not intend to run 24x7.

# Usage:
1. Burn the latest micropython interpretor on ESP8266 (I use D1 mini which has a built-in USB controller).
   http://micropython.org/download#esp8266
2. Edit boot.py with your wifi credentials (2.4 ghz)
3. Edit main_led_multicity.py with your api keys and your choice of cities/stocks/forex.
4. Rename main_led_multicity.py to main.py
5. Upload both boot.py and main.py to esp8266. I use http://docs.dfrobot.com/upycraft/ for editing and uploading the code.
6. Enjoy and share!
