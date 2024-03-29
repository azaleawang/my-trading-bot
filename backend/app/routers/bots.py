from datetime import datetime
import json, time
from app.utils.logger import logger
from typing import List

from app.utils.redis import get_redis_client, read_pnl_from_redis, write_pnl_to_redis
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
import pandas as pd
import pytz
import requests
from sqlalchemy.orm import Session
from app.crud.bot import (
    create_user_bot,
    delete_user_bot,
    find_worker_server,
    get_bot_by_id,
    get_bots,
    stop_user_bot,
    update_worker_server_memory,
    update_worker_server_status,
    worker_scaling,
    assign_worker_server,
    calculate_pnl,
    check_bot_owner,
    check_name
)
from app.schema import bot as schemas
from app.schema.user import User
from app.utils.database import get_db
from app.crud.trade_history import get_bot_trade_history
from app.crud.bot_error import get_error_log_by_container
from app.crud.container_status import (
    get_container_status,
    parse_and_store,
)
from app.utils.deps import get_current_user
from app.exceptions.bot import BotNotFound

router = APIRouter()


@router.get("/admin", response_model=schemas.BotCheckResp)
def get_all_bots(db: Session = Depends(get_db)):
    try:
        db_all_bots = get_bots(db)
        return {"data": db_all_bots}
    except Exception as e:
        logger.error(f"Error in get_all_bots: {e}")
        raise HTTPException(status_code=500, detail="Error fetching bots." + str(e))


@router.post("/", response_model=schemas.BotCreatedResp)
def create_bot_for_user(
    bot: schemas.BotBase,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        check_bot_owner(bot, user)
        container_name = f"User{bot.owner_id}_{bot.strategy}_{bot.name}"

        # get available worker server ip
        worker_server = assign_worker_server(db)

        check_name(db, bot.name, bot.owner_id)
        response = requests.post(
            f"{worker_server.private_ip}/start-container?container_name={container_name}",
            json=bot.model_dump(),
        )
        if response.status_code == 200:
            bot_docker_info = response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to start container in worker server.",
            )

        bot_dict = bot.model_dump()
        bot_create = schemas.BotCreate(
            **bot_dict, **bot_docker_info, worker_instance_id=worker_server.instance_id
        )
        db_bot = create_user_bot(db, bot_create)
        worker_server = update_worker_server_memory(
            db, worker_server.instance_id, db_bot.memory_usage
        )

        return {
            "data": db_bot,
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Error in create_bot_for_user: {e}")
        raise HTTPException(status_code=500, detail="Error creating bot." + str(e))


@router.put("/{bot_id}")
def stop_bot_for_user(
    bot_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    try:
        worker_ip = find_worker_server(db, bot_id)
        db_bot = get_bot_by_id(bot_id=bot_id, db=db)
        check_bot_owner(db_bot, user)
        if not db_bot:
            raise BotNotFound()

        user_bot = stop_user_bot(bot_id, worker_ip, db)

        # Add the memory update and scaling logic to background tasks
        background_tasks.add_task(
            handle_memory_and_scaling,
            db,
            worker_ip,
            user_bot.worker_instance_id,
            -user_bot.memory_usage,
            bot_id,
            user_bot.name,
        )

        return {"message": f"Bot #{bot_id} {user_bot.name} stopped!"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error stopping bot." + str(e))


def handle_memory_and_scaling(
    db, worker_ip, worker_instance_id, memory_usage, bot_id, bot_name
):
    update_worker_server_memory(db, worker_instance_id, memory_usage)

    if worker_scaling(db, worker_ip):
        update_worker_server_status(db, worker_ip=worker_ip)
        logger.info(
            f"Bot #{bot_id} {bot_name} stopped and worker server (ip={worker_ip}) stopped!"
        )


@router.delete("/{bot_id}")
def delete_bot_for_user(
    bot_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    try:
        worker_ip = find_worker_server(db, bot_id)
        user_bot = delete_user_bot(bot_id, worker_ip, db)

        check_bot_owner(user_bot, user)
        return {
            "message": f"Bot #{bot_id} {user_bot.name} removed from Docker containers!"
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error stopping bot." + str(e))


@router.get("/{bot_id}/trade-history", response_model=schemas.BotHistoryResp)
def read_bot_trade_history(
    bot_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_bot, db_bot_history = get_bot_trade_history(db, bot_id)
    check_bot_owner(db_bot, user)
    if db_bot_history is None:
        raise HTTPException(status_code=404, detail="Trading bot not found")

    return {"data": db_bot_history}


@router.get("/{bot_id}/bot-error", response_model=List[schemas.BotError])
def read_bot_error_for_user(
    bot_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        db_bot = get_bot_by_id(bot_id=bot_id, db=db)

        if not db_bot:
            raise BotNotFound()
        check_bot_owner(db_bot, user)
        db_bot_error = get_error_log_by_container(bot_id, db)
        return db_bot_error
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error fetching error log." + str(e)
        )


@router.post("/container-monitoring")
def receive_and_store_container_monitoring_info(data: schemas.ContainerInfoDict):
    parse_and_store(container_data=data.data)
    return {"message": "Data from docker-monitoring worker received successfully"}


@router.get("/{bot_id}/container-monitoring", response_model=schemas.ContainerStateDict)
def get_container_monitoring_logs(
    bot_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_bot = get_bot_by_id(bot_id=bot_id, db=db)
    if not db_bot:
        raise BotNotFound()
    check_bot_owner(db_bot, user)
    container_info = get_container_status(db, bot_id)

    return {"data": container_info}


#
# api for getting bot's pnl chart
@router.get("/{bot_id}/pnl-chart", response_model=schemas.PnlChart)
async def get_bot_pnl_chart(
    bot_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        trade_data = []
        [bot_info, bot_trade_history] = get_bot_trade_history(db, bot_id)
        if not bot_info:
            raise BotNotFound()
        check_bot_owner(bot_info, user)

        # Get buy/sell data from db
        for trade in bot_trade_history:
            trade_data.append(
                {
                    "qty": trade.qty * (1 if trade.info["side"] == "BUY" else -1),
                    "price": trade.avg_price,
                    "pnl": trade.realizedPnl or 0,
                    "timestamp": trade.timestamp,
                }
            )

        trade_df = pd.DataFrame(trade_data)
        trade_df.sort_values(by="timestamp", inplace=True)
        trade_df.reset_index(drop=True, inplace=True)

        # get bot start time (ISO format)
        bot_create_iso_str = bot_info.created_at.astimezone(pytz.utc).isoformat()

        # get bot start timestamp
        bot_create_timestamp_ms = int(bot_info.created_at.timestamp()) * 1000
        bot_stop_iso_str = (
            datetime.now(pytz.utc).isoformat()
            if bot_info.stopped_at is None
            else bot_info.stopped_at.astimezone(pytz.utc).isoformat()
        )
        symbol = bot_info.symbol.replace("/", "")

        redis_client = await get_redis_client()
        creation_time = int(time.time() - int(bot_info.created_at.timestamp()))
        if not redis_client or creation_time <= 900:
            # if created in 15 min then calculate pnl
            return {
                "data": calculate_pnl(
                    symbol,
                    bot_create_iso_str,
                    bot_create_timestamp_ms,
                    bot_stop_iso_str,
                    trade_df,
                )
            }

        key = f"pnldata:{bot_info.owner_id}:{bot_id}"
        value = await read_pnl_from_redis(redis_client=redis_client, key=key)
        if value is None:
            pnl_data = calculate_pnl(
                symbol,
                bot_create_iso_str,
                bot_create_timestamp_ms,
                bot_stop_iso_str,
                trade_df,
            )

            await write_pnl_to_redis(
                redis_client=redis_client,
                key=key,
                value=json.dumps(pnl_data),
                ttl=900 if bot_info.stopped_at is None else None,
            )

        return {"data": pnl_data if value is None else value}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
