from database import init_db, run_migrations
from fastapi import FastAPI, Request
from routes import auth

app = FastAPI()


@app.on_event("startup")
def on_startup():
    run_migrations()
    init_db()


app.include_router(auth.router)


@app.post("/test")
async def test(request: Request):
    body = await request.body()
    headers = request.headers
    return {"body": body.decode(), "headers": dict(headers)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
