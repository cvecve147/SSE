from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import time

app = FastAPI()

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def event_generator():
    for i in range(10):
        await asyncio.sleep(1)
        yield f"data: Time: {time.strftime('%H:%M:%S')}\n\n"
    yield "event: complete\ndata: Stream completed\n\n"

@app.get("/sse")
async def sse_endpoint():
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
