import datetime
import pytz
from sqlalchemy import and_
from app.src.models.trade_history import Trade_History
from sqlalchemy.orm import Session
from app.src.models.bot import Bot
from app.src.schema import schemas


def create_trade_history(db: Session, trade_data: schemas.TradeHistoryCreate):
    new_trade = Trade_History(
        container_name=trade_data.container_name,
        action=trade_data.action,
        avg_price=float(trade_data.data["avgPrice"]),  # Convert string to integer
        info=trade_data.data,
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