from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from yt_dlp import YoutubeDL
import os

app = FastAPI()

VIDEO_PATH = "static/video.mp4"

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/download")
async def download_video(url: str = Form(...)):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': VIDEO_PATH,
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return HTMLResponse(f"<h2>Ошибка: {e}</h2>", status_code=500)

@app.get("/watch")
async def watch_video():
    if not os.path.exists(VIDEO_PATH):
        return HTMLResponse("<h2>Видео не найдено</h2>", status_code=404)
    return FileResponse(VIDEO_PATH, media_type="video/mp4")

@app.post("/delete")
async def delete_video():
    if os.path.exists(VIDEO_PATH):
        os.remove(VIDEO_PATH)
    return RedirectResponse(url="/", status_code=303)
