from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def trades():
	return "trades list"