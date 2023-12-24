import logging
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.utils.database import get_db
from app.models.backtest import BacktestResult
from app.src.schema import schemas
from sqlalchemy import text, func

# If the strategy has been tested before, return the strategy backtest result
def check_backtest_strategy(
    strategy, db: Session = Depends(get_db)):
    try:
        backtest_existed = (
            db.query(BacktestResult)
            .filter(
                BacktestResult.strategy_name == strategy.get('name'),
                BacktestResult.symbol == strategy.get('symbols')[0],
                BacktestResult.t_frame == strategy.get('t_frame'),
                BacktestResult.since == strategy.get('since'),
                BacktestResult.type == strategy.get('default_type'),
                BacktestResult.params == strategy.get('params'),
                BacktestResult.updated_at + text("'1 day'::interval") > func.now(),
            )
            .first()
        )
        if backtest_existed:
            print("find backtest: id = ", backtest_existed.id)
            return backtest_existed.id  # strategy backtest existed
        else:
            return None  # strategy not existed
    except Exception as e:
        logging.error("Error in checking backtest strategy history: %s", e)
        raise HTTPException(
            status_code=500, detail="Check backtest strategy history failed."
        ) from e
    
    # return backtest_existed.id  # strategy existed
    # return None  # strategy not existed
    

# check if tested before (暫時先不做時間檢查)
def check_backtest_result(
    bt_res: schemas.BacktestResultBase, db: Session = Depends(get_db)
):
    try:
        backtest_existed = (
            db.query(BacktestResult)
            .filter(
                BacktestResult.strategy_name == bt_res.get("info").get("name"),
                BacktestResult.symbol == bt_res.get("info").get("symbols")[0],
                BacktestResult.t_frame == bt_res.get("info").get("t_frame"),
                BacktestResult.since == bt_res.get("info").get("since"),
                BacktestResult.type == bt_res.get("info").get("default_type"),
                BacktestResult.params == bt_res.get("info").get("params"),
            )
            .first()
        )
        if backtest_existed:
            print("find backtest: id = ", backtest_existed.id)
            return backtest_existed.id  # strategy existed
        else:
            return None  # strategy not existed
    except Exception as e:
        logging.error("Error in checking backtest result: %s", e)
        raise HTTPException(
            status_code=500, detail="Check backtest result failed."
        ) from e


def insert_backtest_result(
    bt_res: schemas.BacktestResultBase, db: Session = Depends(get_db)
):
    try:
        existed_id = check_backtest_result(bt_res, db)
        if existed_id:
            # update plot url and result details
            updated_result = (
                db.query(BacktestResult)
                .filter(BacktestResult.id == existed_id)
                .update(
                    {
                        BacktestResult.plot_url: bt_res.get("result").get("plot"),
                        BacktestResult.details: bt_res.get("result"),
                    }
                )
            )
            db.commit()

            if not updated_result:
                raise HTTPException(
                    status_code=400, detail="Update backtest result failed."
                )
            return existed_id
            # return (
            #     db.query(BacktestResult)
            #     .filter(BacktestResult.id == existed_id)
            #     .first()
            # )

        backtest_result = BacktestResult(
            strategy_name=bt_res.get("info").get("name"),
            symbol=bt_res.get("info").get("symbols")[0],
            t_frame=bt_res.get("info").get("t_frame"),
            since=bt_res.get("info").get("since"),
            type=bt_res.get("info").get("default_type"),
            plot_url=bt_res.get("result").get("plot"),
            params=bt_res.get("info").get("params"),
            details=bt_res.get("result"),
        )
        db.add(backtest_result)
        db.commit()
        db.refresh(backtest_result)
        return backtest_result.id
    except Exception as e:
        logging.error("Error in inserting backtest result: %s", e)
        raise HTTPException(
            status_code=400, detail="Insert backtest result failed."
        ) from e


# read backtest result by strategy id
def get_backtest_result(db: Session, backtest_id: int):
    return db.query(BacktestResult).filter(BacktestResult.id == backtest_id).first()
