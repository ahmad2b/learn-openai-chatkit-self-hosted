from __future__ import annotations

from typing import Any

from chatkit.server import StreamingResult
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from starlette.responses import JSONResponse
from dotenv import load_dotenv

from .chat import MyChatKitServer, create_chatkit_server

load_dotenv()

app = FastAPI(title="ChatKit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

_chatkit_server: MyChatKitServer = create_chatkit_server()


def get_chatkit_server() -> MyChatKitServer:
    """Dependency to get the ChatKit server instance."""
    return _chatkit_server


@app.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    server: MyChatKitServer = Depends(get_chatkit_server),
) -> Response:
    """
    Main ChatKit endpoint - handles all chat requests.

    This endpoint:
    1. Receives request body from frontend
    2. Passes it to ChatKit server for processing
    3. Returns streaming response (text/event-stream) or JSON
    """
    payload = await request.body()
    result = await server.process(payload, {"request": request})

    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")

    if hasattr(result, "json"):
        return Response(content=result.json, media_type="application/json")

    return JSONResponse(result)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}