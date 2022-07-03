from typing import Optional
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, SessionLocal

from fastapi import FastAPI, Depends, Body

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# get the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# rout to return all the trades with pagignation
@app.get("/trades")
async def get_trades(page_num: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    trades = db.query(models.Trade).all()
    start = (page_num - 1) * page_size
    end = start + page_size

    trades_len = len(trades)
    response = {
        "data" : trades[start: end],
        "total" : trades_len,
        "count" : page_size,
        "pagignation" : {

        }
    }

    if end >= trades_len:
        response["pagignation"]["next"] = None

        if page_num > 1:
            response["pagignation"]["previous"] = f'/trades?page_num={page_num-1}&page_size={page_size}'
        else:
            response["pagignation"]["previous"] = None
    else:
        if page_num > 1:
            response["pagignation"]["previous"] = f'/trades?page_num={page_num-1}&page_size={page_size}'
        else:
            response["pagignation"]["previous"] = None

        response["pagignation"]["next"] = f'/trades?page_num={page_num+1}&page_size={page_size}'

    return response


@app.get("/trades/{trade_id}")
async def get_single_trade(trade_id: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()


# route to search
@app.get("/search")
async def search_trades(counterparty: str, instrument_name: str,
                        instrument_id: str, trader: str,
                        db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.counterparty == counterparty and
                                         models.Trade.instrument_name == instrument_name and
                                         models.Trade.instrument_id == instrument_id and
                                         models.Trade.trader == trader).first()


# route to create trade
@app.post("/trade")
async def create_trade(trades: schemas.Trade, db: Session = Depends(get_db)):
    new_trade_Details = models.TradeDetails(price=trades.trade_details.price,
                                            buySellIndicator=trades.trade_details.buySellIndicator,
                                            quantity=trades.trade_details.quantity)
    db.add(new_trade_Details)
    db.commit()
    db.refresh(new_trade_Details)

    new_trade = models.Trade(trade_id=trades.trade_id, trader=trades.trader, asset_class=trades.asset_class,
                             trade_details_id=new_trade_Details.id,
                             counterparty=trades.counterparty, trade_date_time=trades.trade_date_time,
                             instrument_id=trades.instrument_id, instrument_name=trades.instrument_name)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)

    return "trade added successfully"
