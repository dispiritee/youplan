from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import subprocess

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/stream")
async def stream_video(url: str):
    cmd = ["yt-dlp", "-f", "best", "-o", "-", url]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return StreamingResponse(process.stdout, media_type="video/mp4")
