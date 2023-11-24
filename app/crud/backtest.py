import logging
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.src.config.database import get_db
from app.src.models.backtest import Backtest_Result
from app.src.schema import schemas


# check if tested before (暫時先不做時間檢查)
def check_backtest_result(
    bt_res: schemas.BacktestResultBase, db: Session = Depends(get_db)
) -> bool:
    try:
        backtest_existed = (
            db.query(Backtest_Result)
            .filter(
                Backtest_Result.strategy_name == bt_res.get("info").get("name"),
                Backtest_Result.symbol == bt_res.get("info").get("symbols")[0],
                Backtest_Result.t_frame == bt_res.get("info").get("t_frame"),
                Backtest_Result.since == bt_res.get("info").get("since"),
                Backtest_Result.type == bt_res.get("info").get("default_type"),
                Backtest_Result.params == bt_res.get("info").get("params"),
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
                db.query(Backtest_Result)
                .filter(Backtest_Result.id == existed_id)
                .update(
                    {
                        Backtest_Result.plot_url: bt_res.get("result").get("plot"),
                        Backtest_Result.details: bt_res.get("result"),
                    }
                )
            )
            db.commit()
            if not updated_result:
                raise HTTPException(
                    status_code=400, detail="Update backtest result failed."
                )
            return (
                db.query(Backtest_Result)
                .filter(Backtest_Result.id == existed_id)
                .first()
            )

        backtest_result = Backtest_Result(
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
        return backtest_result
    except Exception as e:
        logging.error("Error in inserting backtest result: %s", e)
        raise HTTPException(
            status_code=400, detail="Insert backtest result failed."
        ) from e
