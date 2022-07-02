from typing import Optional
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, SessionLocal

from fastapi import FastAPI, Depends

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# get the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# rout to return all the trades
@app.get("/trades")
async def get_trades(db: Session = Depends(get_db), limit: Optional[int] = None):
    return db.query(models.Trade).limit(limit).all()


# route to return single trade by id
# @app.get("/trades/{trade_id}")
# async def single_trade(id):
#     return "single trade by id"


# route to return trades based on searched query
# @app.get("/trades/")
# async def search_trades(counterparty, instrumentId, instrumentName, trader):
#     return "trades according to search values"


# route to create new trades
# @app.post("/trade_details")
# async def create_trade_details(req: schemas.TradeDetails):
#     return "creating trade details"


# route to create trade
@app.post("/trade")
async def create_trade(trades: schemas.Trade, db: Session = Depends(get_db)):
    new_trade = models.Trade(trade_id=trades.trade_id, trader=trades.trader, asset_class=trades.asset_class,
                             counterparty=trades.counterparty, trade_date_time=trades.trade_date_time,
                             instrument_id=trades.instrument_id, instrument_name=trades.instrument_name)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)

    return new_trade
    # new_trade_Details = models.TradeDetails(price=req.trade_details.price,
    #                                         buySellIndicator=req.trade_details.buySellIndicator,
    #                                         quantity=req.trade_details.quantity)
    # db.add(new_trade_Details)
    # db.commit()
    # db.refresh(new_trade_Details)
    # new_trade = models.Trade(trade_id=req.trade_id, trader=req.trader, asset_class=req.asset_class,
    #                          counterparty=req.counterparty,
    #                          trade_details_id=new_trade_Details.id,
    #                          instrument_id=req.instrument_id
    #                          , instrument_name=req.instrument_name, trade_date_time=req.trade_date_time)
    # db.add(new_trade)
    # db.commit()
    # db.refresh(new_trade)
    # data = db.get(models.Trade, new_trade.trade_id)
    # return data
