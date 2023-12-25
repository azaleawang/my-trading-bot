import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import traceback, logging, json
from app.crud.backtest import (
    check_backtest_strategy,
    get_backtest_result,
    insert_backtest_result,
)
from app.utils.database import get_db
from app.utils.sqs import send_sqs_message
from app.schema.commons import MessageResp
from app.schema.backtest import BacktestResultBase, BacktestStrategy
import websockets
import math
from app.constants import BACKTEST_RESULT_EXAMPLE as bt_res
from app.exceptions import UnexpectedError, BacktestResultNotFound

router = APIRouter()


@router.post("/", response_model=MessageResp)
def run_backtest(strategy: BacktestStrategy, db: Session = Depends(get_db)):
    # Check if the strategy backtest result is already in the database
    existed_result_id = check_backtest_strategy(strategy, db)
    if existed_result_id:
        asyncio.run(send_message(strategy.user_id, {"id": existed_result_id}))
        return MessageResp(message=f"Backtesting '{strategy}' already in the database.")

    # Send message into SQS queue
    strategy_config = {"s3_url": os.getenv("S3_BACKTEST_STRATEGY_URL")}
    message_body = dict(**strategy.model_dump(), **strategy_config)
    send_sqs_message(message_body=message_body)

    return MessageResp(
        message=f"Backtesting '{strategy}' job successfully push into SQS."
    )


@router.post("/result/", response_model=MessageResp)
def receive_lambda_result(
    data: BacktestResultBase = bt_res, db: Session = Depends(get_db)
):
    try:
        parsed_result = data.model_dump()

        client_id = int(parsed_result["info"]["user_id"])
        parsed_result["result"] = json.loads(parsed_result["result"])
        for key, value in parsed_result["result"].items():
            if isinstance(value, float) and math.isnan(value):
                parsed_result["result"][key] = None

        bt_res_id = insert_backtest_result(parsed_result, db)

        # Notify frontend to fetch new data or refresh page
        asyncio.run(send_message(client_id, {"id": bt_res_id}))
        return MessageResp(message="Data received successfully")
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        traceback.print_exc()
        logging.error(f"Error in receive_lambda_result: {e}")
        raise UnexpectedError(detail="Error in processing received data from Lambda.")


# get backtest result by id
@router.get("/results/{bt_res_id}", responses={404: {"description": "Not found"}})
def get_strategy(bt_res_id: int, db: Session = Depends(get_db)):
    db_backtest_result = get_backtest_result(db, bt_res_id)
    if not db_backtest_result:
        raise BacktestResultNotFound()
    return db_backtest_result


async def send_message(client_id: int, message={"data": "test"}):
    uri = f"ws://localhost:8000/ws/backtest_result/{client_id}"  # Use localhost when test locally
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(message))
        reply = await websocket.recv()
        print(f"<<< {reply}")
