
## Go into venv trading-bot
`source trading-bot/bin/activate`

## install ta-lib
https://www.youtube.com/watch?v=AQFZMvYp2KA

`wget https://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz`

`tar -xvf ta-lib-0.4.0-src.tar.gz`

`cd ta-lib`

`./configure --prefix=/usr`

`make`

`sudo make install`

`whereis ta-lib`

`pip3 install ta-lib`

`python > import talib as ta` (for testing)

## Install all dependencies
`pip install -r requirements.txt`

## Start server
`python main.py`

## Docker for running Python script
```bash
docker build -t py-tradingbot .
docker images
# docker run -d py-tradingbot
# docker run -d --name trading-container -v /home/leah/my-trading-bot/trade/supertrend:/app py-tradingbot python -u ./supertrend.py
# docker logs -f trading-container (or containerid)
```
### 要加上自己的密碼
`backend/trade/supertrend/config.py`