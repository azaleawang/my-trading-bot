import datetime
import pytz
from typing import Union
from sqlalchemy import and_
from app.src.models.trade_history import Trade_History
from sqlalchemy.orm import Session
from app.src.models.bot import Bot
from app.src.schema import schemas


def create_trade_history(db: Session, trade_data: schemas.TradeHistoryCreate, realizedPnl: Union[None, float]):
    
    
    new_trade = Trade_History(
        container_name=trade_data.container_name,
        order_id=int(trade_data.data["orderId"]),
        qty=float(trade_data.data["cumQty"]),
        action=trade_data.action,
        avg_price=float(trade_data.data["avgPrice"]),  # Convert string to integer
        info=trade_data.data,
        realizedPnl=realizedPnl,
        # time=datetime.now(pytz.timezone("Asia/Taipei"))  # Optional, if not using default
        timestamp=int(trade_data.data["updateTime"]),
    )
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade


def get_bot_trade_history(db: Session, userId: int, bot_id: int):
    bot = db.query(Bot).filter(and_(Bot.id == bot_id, Bot.owner_id == userId)).first()
    if bot:
        return bot.trade_history
    else:
        return None
    

"""
[{'info': {'symbol': 'ETHUSDT', 'id': '125306774', 'orderId': '1216771770', 'side': 'SELL', 'price': '2035.41', 'qty': '0.100', 'realizedPnl': '-0.35738426', 'marginAsset': 'USDT', 'quoteQty': '203.54100', 'commission': '0.08141640', 'commissionAsset': 'USDT', 'time': '1701352664686', 'positionSide': 'BOTH', 'maker': False, 'buyer': False}, 'timestamp': 1701352664686, 'datetime': '2023-11-30T13:57:44.686Z', 'symbol': 'ETH/USDT:USDT', 'id': '125306774', 'order': '1216771770', 'type': None, 'side': 'sell', 'takerOrMaker': 'taker', 'price': 2035.41, 'amount': 0.1, 'cost': 203.541, 'fee': {'cost': 0.0814164, 'currency': 'USDT'}, 'fees': [{'cost': 0.0814164, 'currency': 'USDT'}]}]
"""