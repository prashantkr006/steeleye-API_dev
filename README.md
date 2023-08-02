
# end points using FastAPI

This is an API developed by using [fastApi](https://fastapi.tiangolo.com/) framework. The API here contains
four end points

- list all trades( with pagignation feature)
- display single trade by trade id
- search trades based on

    - counterparty
    - instrumentId
    - instrumentName
    - trader
- filter trades based on conditions


## project installation
To setup the project in your local machine 
first clone the repository to the local machine, 
then install all the requirements of app from requirements.txt file.
by running the command

```pip install -r requirements.txt```

then start the server, the command below will start the server

``` uvicorn main:app --reload```

now go to http://127.0.0.1:8000, that's it you are ready to go.
to test the working features of app visit here: http://127.0.0.1:8000/docs#/ 


## Solution and approach
- end point: list all trades with pagignation,

    for this solution called ```GET``` method in which passed parameters which were our database(from where data was responding)
    then page_num and page_size variables which were used for pagignation these were dynamically changing.
    
    - pagignation logic
        
        ```response = {
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

            response["pagignation"]["next"] = f'/trades?page_num={page_num+1}&page_size={page_size}'```

- end point: response single trade by id

    For this, just applied Query parameter of fastAPI, and in query input the required id and ```GET``` method will return the data
- end point: search trade based on different inputs

    with SQLAchemy Query filtered out the data from database and responded it to the client
    ```db.query(models.Trade).filter(models.Trade.counterparty == counterparty and models.Trade.instrument_name == instrument_name and models.Trade.instrument_id == instrument_id and models.Trade.trader == trader).first()```


## extras
added responses for the api end points by handling exception & status code
