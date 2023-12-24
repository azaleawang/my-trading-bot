# storing backtest results
import pytz
from sqlalchemy import Column, ForeignKey, TIMESTAMP, Integer, String, BIGINT, Float
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class TradeHistory(Base):
    __tablename__ = "trade_history"

    id = Column(BIGINT, primary_key=True)
    # strategy_id = Column(BIGINT, ForeignKey("strategies.id"), nullable=False)
    container_name = Column(String, ForeignKey("bots.container_name"), nullable=False)
    order_id = Column(BIGINT, unique=True, nullable=False)
    qty = Column(Float, nullable=False)
    action = Column(String, nullable=False)
    avg_price = Column(Float, nullable=False)
    info = Column(JSONB, nullable=False)
    timestamp = Column(BIGINT, nullable=False)
    realizedPnl = Column(Float)
    bot = relationship("Bot", back_populates="trade_history")
    
# {'orderId': '1211943298', 'symbol': 'ETHUSDT', 'status': 'FILLED', 'clientOrderId': 'x-xcKtGhcue8a91b792898fa6e749e21', 'price': '0.00', 'avgPrice': '2052.43000', 'origQty': '0.100', 'executedQty': '0.100', 'cumQty': '0.100', 'cumQuote': '205.24300', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'NONE', 'goodTillDate': '0', 'updateTime': '1701054107239'}
