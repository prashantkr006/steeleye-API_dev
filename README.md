
# API Developer Assessment

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
