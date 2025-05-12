from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from yt_dlp import YoutubeDL

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/stream")
async def stream_video(url: str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'format': 'best[ext=mp4]/best',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            direct_url = info.get("url")

            if not direct_url:
                return HTMLResponse("Не удалось получить ссылку на видео", status_code=500)

            return RedirectResponse(direct_url)

    except Exception as e:
        return HTMLResponse(f"Ошибка: {str(e)}", status_code=500)
