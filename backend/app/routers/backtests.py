import asyncio
from typing import Any, Union, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Json
import traceback, logging, json
from app.crud.backtest import get_backtest_result, insert_backtest_result
from app.src.config.database import get_db
from app.src.controller.sqs import send_sqs_message
from app.src.schema.schemas import BacktestResultBase, Message_Resp
import websockets


router = APIRouter()


class Backtest_Strategy(BaseModel):
    name: str = "MaRsi"
    symbols: list = ["BTC/USDT"]
    t_frame: str = "1h"
    since: Union[str, None] = "2017-01-01T00:00:00Z"
    default_type: Union[str, None] = "future"
    params: Union[dict, None] = {"rsi_window": 20}


# TODO 送出之前先檢查要不要從資料庫撈出舊資料
@router.post("/", response_model=Message_Resp)
def run_backtest(strategy: Backtest_Strategy) -> dict:
    try:
        # send message into SQS queue
        strategy_config = {"s3_url": os.getenv("S3_BACKTEST_STRATEGY_URL")}
        message_body = dict(**strategy.model_dump(), **strategy_config)
        response = send_sqs_message(message_body=message_body)
        # response = {}
        if "error" in response:
            print("Error occurred:", response.get("details"))
            return JSONResponse(
                content={
                    "message": f"Backtesting job push into SQS failed. {response.get('details')}"
                },
                status_code=500,
            )
        else:
            return {
                "message": f"Backtesting '{strategy}' job push into SQS id {response.get('MessageId')}."
            }

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


bt_res = {
    "info": {
        "name": "MaRsi",
        "symbols": ["BTC/USDT"],
        "t_frame": "4h",
        "since": "2023-01-01T00:00:00Z",
        "default_type": "future",
        "params": {"rsi_window": 20},
        "s3_url": "https://my-trading-bot.s3.ap-northeast-1.amazonaws.com/backtest/strategy/",
    },
    "result": {
        "Start": "2022-01-01 00:00:00",
        "End": "2023-11-23 00:00:00",
        "Duration": "326 days 00:00:00",
        "Exposure Time [%]": 66.12161471640266,
        "Equity Final [$]": 1120859.2821999998,
        "Equity Peak [$]": 1234099.6822,
        "Return [%]": 12.085928219999978,
        "Buy & Hold Return [%]": 125.99323625319887,
        "Return (Ann.) [%]": 13.581950832484303,
        "Volatility (Ann.) [%]": 39.260540400055056,
        "Sharpe Ratio": 0.3459440622591445,
        "Sortino Ratio": 0.6533733876824362,
        "Calmar Ratio": 0.6484981002786342,
        "Max. Drawdown [%]": -20.943701803673243,
        "Avg. Drawdown [%]": -7.801029779525336,
        "Max. Drawdown Duration": "132 days 08:00:00",
        "Avg. Drawdown Duration": "31 days 09:00:00",
        "# Trades": 3,
        "Win Rate [%]": 66.66666666666666,
        "Best Trade [%]": 14.558902955652231,
        "Worst Trade [%]": -2.079730036644434,
        "Max. Trade Duration": "183 days 08:00:00",
        "Avg. Trade Duration": "131 days 07:00:00",
        "Profit Factor": 8.920607883214219,
        "Expectancy [%]": 5.490908707734432,
        "SQN": 0.7778559670931925,
        "_strategy": "MaRsi(params=)",
        "plot": "backtest/result/MaRsi_BTC-USDT_4h_20231123-021346.html",
    },
}
    

@router.post("/result", response_model=Message_Resp)
def receive_lambda_result(
    data: BacktestResultBase = bt_res, db: Session = Depends(get_db)
):
    try:
        logging.info(f"Received data from Lambda: {data}")
        parsed_result = data.model_dump()
        # if parsed_result.get("plot"):
        #     parsed_result["plot"] = os.getenv("S3_URL") + parsed_result["plot"]
        # print(parsed_result)
        # Let's insert data (or redis)
        bt_res_id = insert_backtest_result(parsed_result, db)
        print("get backtest result id = ", bt_res_id)
        # notify frontend to fetch new data or refresh page
        asyncio.run(send_message({"id": bt_res_id}))
        return {
            "message": "Data received successfully",
        } 
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error in receive_lambda_result: {e}")
        raise HTTPException(status_code=500, detail="Error processing received data." + str(e))

# get backtest result by id
@router.get("/results/{bt_res_id}")
def get_strategy(bt_res_id: int, db: Session = Depends(get_db)):
    db_backtest_result = get_backtest_result(db, bt_res_id)
    return db_backtest_result

# 因為router.post 有資料格式parse的問題＠＠ 所以先用這個測試WS
# @router.get("/results/test/{id}")
# def get_strategy(id: int, db: Session = Depends(get_db)):
#     asyncio.run(send_message({"id": id}))
    
async def send_message(message={"data": "test"}):
    uri = "ws://localhost:8000/ws/backtest_result" # Use localhost when test locally
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(message))
        greeting = await websocket.recv()
        print(f"<<< {greeting}")