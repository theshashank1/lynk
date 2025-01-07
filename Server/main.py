from fastapi import FastAPI, Request

app = FastAPI()











@app.post("/test")
async def test(request: Request):
    body = await request.body()
    headers = request.headers
    return {"body": body.decode(), "headers": dict(headers)}
    
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
