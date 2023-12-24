import logging
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.utils.database import get_db
from app.models.backtest import BacktestResult
from app.src.schema import backtest as schemas
from sqlalchemy import text, func


# If the strategy has been tested before, return the strategy backtest result
def check_backtest_strategy(
    strategy: schemas.BacktestStrategy, db: Session = Depends(get_db)
):
    try:
        backtest_existed = (
            db.query(BacktestResult)
            .filter(
                BacktestResult.strategy_name == strategy.name,
                BacktestResult.symbol == strategy.symbols[0],
                BacktestResult.t_frame == strategy.t_frame,
                BacktestResult.since == strategy.since,
                BacktestResult.type == strategy.default_type,
                BacktestResult.params == strategy.params,
                BacktestResult.updated_at + text("'1 day'::interval") > func.now(),
            )
            .first()
        )

        return backtest_existed.id if backtest_existed else None

    except Exception as e:
        logging.error("Error in checking backtest strategy history: %s", e)
        raise HTTPException(
            status_code=500, detail="Check backtest strategy history failed."
        ) from e


def check_backtest_result(
    bt_res: schemas.BacktestResultBase, db: Session = Depends(get_db)
):
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

    return backtest_existed or None


def insert_backtest_result(bt_res, db: Session = Depends(get_db)):
    try:
        existed_backtest = check_backtest_result(bt_res, db)
        if existed_backtest:
            # Update plot url and result details
            existed_backtest.plot_url = bt_res.get("result").get("plot")
            existed_backtest.details = bt_res.get("result")

            db.commit()
            return existed_backtest.id

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
            status_code=500, detail="Insert backtest result failed."
        )


# read backtest result by strategy id
def get_backtest_result(db: Session, backtest_id: int):
    return db.query(BacktestResult).filter(BacktestResult.id == backtest_id).first()
