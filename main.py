from typing import Optional,Union
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, SessionLocal
from sqlalchemy import or_, func
import datetime
from math import ceil




from fastapi import FastAPI, Depends, Query

<<<<<<< HEAD
=======
from fastapi import FastAPI, Depends, Response, status
>>>>>>> 2efc7f5213832c135d674d517c26de9793c0fcd6

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# get the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


<<<<<<< HEAD
# rout to return all the trades with pagination feature
@app.get("/trades")
async def get_trades(limit:Union[int,None] = Query(
        default=2,
        title="Limit",\
        description="Number of items per page, default =2'"
    ),
    page:Union[int,None] = Query(
        default=1,
        title="Page",\
        description="page number being requested"
    ),db: Session = Depends(get_db)):

    page_size=limit
    total_items_count=db.query(models.Trade).count() #number of entries in models.Trade
    total_no_pages=ceil(total_items_count/page_size)
    start_index=(page-1)*limit
    data=db.query(models.Trade).offset(start_index).limit(page_size).all()

    next_page=""
    if (page) >=total_no_pages:
        next_page=""
    else:
        next_page="localhost:8000?limit={}&page={}".format(limit,page+1)
    
    info=dict()
    info["count"]=total_items_count
    info["totalPages"]=total_no_pages
    info["itemsPerPage"]=limit
    info["nextPage"]=next_page
    return [info,data]

@app.get("/trade_details")
async def get_trades(db: Session = Depends(get_db), limit: Optional[int] = None):
    return db.query(models.TradeDetails).limit(limit).all()



@app.get("/trades/details/filterBy")
async def get_trades(assetClass:Union[str,None] = Query(
        default=None,
        title="Asset Class",\
        description="Asset Class of the Trade"
    )
    ,end:Union[str,None] = Query(
        default=None,
        title="End Date",\
        description="The Maximum date for the tradeDateTime field. Date Format is in the form Day/Month/Year e.g. '10/07/2022'"  
    ),maxPrice:Union[str,None] = Query(
        default=None,
        title="Maximum Price",\
        description="The maximum value for the tradeDetails.price field"  
    ), minPrice:Union[str,None] = Query(
        default=None,
        title="Minimum Price",\
        description="The Minimum value for the tradeDetails.price field"  
    ),start:Union[str,None] = Query(
        default=None,
        title="StartDate",\
        description="The Minimum date for the tradeDateTime field. Date Format is in the form Day/Month/Year  e.g. '10/07/2022"  
    ),tradeType:Union[str,None] = Query(
        default=None,
        title="trade indicator",\
        description="tradeDetails.buySellIndicator .. (Buy or Sell)"  
    ),
    db: Session = Depends(get_db)):
    filters=[]    # for direct queries on Trades table

    if assetClass:
        filters.append(models.Trade.asset_class==assetClass)

    if end:
        datetime_object=datetime.datetime.strptime(end, "%d/%m/%Y")
        filters.append(models.Trade.trade_date_time >= datetime_object)
    
    if start:
        datetime_object=datetime.datetime.strptime(start, "%d/%m/%Y")
        filters.append(func.date(models.Trade.trade_date_time) <= datetime_object)

    if (start or end or assetClass):
        results =db.query(models.Trade).filter(or_(*filters)).all()  # run the queries on the Trade table
    else:
        results=[]
    
    if maxPrice:
        max_price_query=db.query(models.TradeDetails).filter(models.TradeDetails.price >= maxPrice).all()
        temp=[a.trades for a in max_price_query ] # get the  trade table related to the max_price query
        temp=[a[0] for  a in temp ]  # flatten the temp list
        results.extend(temp)  # extend the results list with the outcome of the max_price query

    if minPrice:
        min_price_query=db.query(models.TradeDetails).filter(models.TradeDetails.price <= minPrice).all()
        temp=[a.trades for a in min_price_query ] # get the  trade table related to the min_price query
        temp=[a[0] for  a in temp ]  # flatten the temp list
        results.extend(temp)  # extend the results list with the outcome of the min_price query

    if tradeType:
        trade_type_query=db.query(models.TradeDetails).filter(models.TradeDetails.buySellIndicator == tradeType).all()
        temp=[a.trades for a in trade_type_query ] # get the  trade table related to the tradeType query
        temp=[a[0] for  a in temp ]  # flatten the temp list
        results.extend(temp)  # extend the results list with the outcome of the tradeType query
    
    response=[]
    for a in results:
        if a in response:
            continue
        else:
            response.append(a)

        
    return response
   
    

=======
# rout to return all the trades with pagignation
@app.get("/trades")
async def get_trades(page_num: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    trades = db.query(models.Trade).all()
    start = (page_num - 1) * page_size
    end = start + page_size
>>>>>>> 2efc7f5213832c135d674d517c26de9793c0fcd6

    trades_len = len(trades)
    response = {
        "data": trades[start: end],
        "total": trades_len,
        "count": page_size,
        "pagignation": {

<<<<<<< HEAD
@app.get("/trades/{trade_id}")
async def get_single_trade(trade_id: str, db: Session = Depends(get_db)):
    # return db.query(models.Trade).join(models.TradeDetails, models.TradeDetails.id ==trade_id).first()
    # return db.query(models.Trade).filter(models.Trade.trade_details.has(id=trade_id)).first()
    db.query(models.Trade).filter(models.Trade.trade_details.id==trade_id).first()

=======
        }
    }

    if end >= trades_len:
        response["pagignation"]["next"] = None

        if page_num > 1:
            response["pagignation"]["previous"] = f'/trades?page_num={page_num - 1}&page_size={page_size}'
        else:
            response["pagignation"]["previous"] = None
    else:
        if page_num > 1:
            response["pagignation"]["previous"] = f'/trades?page_num={page_num - 1}&page_size={page_size}'
        else:
            response["pagignation"]["previous"] = None

        response["pagignation"]["next"] = f'/trades?page_num={page_num + 1}&page_size={page_size}'

    return response


@app.get("/trades/{trade_id}", status_code=status.HTTP_200_OK)
async def get_single_trade(response: Response, trade_id: str, db: Session = Depends(get_db)):
    trade = db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()

    if not trade:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"details not found"}
    return trade


# route to search
@app.get("/search", status_code=status.HTTP_200_OK)
async def search_trades(response: Response, counterparty: str, instrument_name: str,
                        instrument_id: str, trader: str,
                        db: Session = Depends(get_db)):
    trade = db.query(models.Trade).filter(models.Trade.counterparty == counterparty and
                                          models.Trade.instrument_name == instrument_name and
                                          models.Trade.instrument_id == instrument_id and
                                          models.Trade.trader == trader).first()
    if not trade:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"details not found"}
    return trade
>>>>>>> 2efc7f5213832c135d674d517c26de9793c0fcd6


# route to create trade
@app.post("/trade", status_code=status.HTTP_201_CREATED)
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
