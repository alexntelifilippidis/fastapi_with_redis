import uvicorn
from fastapi import FastAPI

from API import asynchronous_routes, synchronous_routes

app = FastAPI()
app.include_router(synchronous_routes.synchronous)
app.include_router(asynchronous_routes.asynchronous)


@app.get("/")
def read_root():
    return {"Hello go to localhost:8000/docs to see the docs"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
