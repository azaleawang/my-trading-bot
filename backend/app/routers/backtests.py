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
    "result": '{\n    "Start": "2023-01-01 00:00:00",\n    "End": "2023-11-28 08:00:00",\n    "Duration": "331 days 08:00:00",\n    "Exposure Time [%]": 82.08223311957752,\n    "Equity Final [$]": 1355324.8288,\n    "Equity Peak [$]": 1517576.6848,\n    "Return [%]": 35.532482879999996,\n    "Buy & Hold Return [%]": 124.00617171900525,\n    "Return (Ann.) [%]": 39.69092387742143,\n    "Volatility (Ann.) [%]": 57.32197021057216,\n    "Sharpe Ratio": 0.6924207896486616,\n    "Sortino Ratio": 1.6752137367792543,\n    "Calmar Ratio": 1.8197071583421327,\n    "Max. Drawdown [%]": -21.811709480542106,\n    "Avg. Drawdown [%]": -3.649393432304394,\n    "Max. Drawdown Duration": "137 days 13:00:00",\n    "Avg. Drawdown Duration": "8 days 05:00:00",\n    "# Trades": 2,\n    "Win Rate [%]": 50.0,\n    "Best Trade [%]": 36.58727154426143,\n    "Worst Trade [%]": -0.763650456607301,\n    "Max. Trade Duration": "270 days 20:00:00",\n    "Avg. Trade Duration": "135 days 23:00:00",\n    "Profit Factor": 47.91101901098716,\n    "Expectancy [%]": 17.911810543827063,\n    "SQN": 0.9453312864480757,\n    "_strategy": "MaRsi(params=)",\n    "plot": "backtest/result/MaRsi_BTC-USDT_1h_20231128-082333.html"\n}',
}


@router.post("/result/", response_model=Message_Resp)
def receive_lambda_result(
    data: BacktestResultBase = bt_res, db: Session = Depends(get_db)
):
    try:
        logging.info(f"Received data from Lambda: {data}")
        parsed_result = data.model_dump()
        print(parsed_result)
        parsed_result["result"] = json.loads(parsed_result["result"])
        print(parsed_result)

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
        raise HTTPException(
            status_code=500, detail="Error processing received data." + str(e)
        )


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
    uri = "ws://localhost:8000/ws/backtest_result"  # Use localhost when test locally
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(message))
        greeting = await websocket.recv()
        print(f"<<< {greeting}")
