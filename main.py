from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random, string

app = FastAPI()

# Simulación de base de datos
links_db = {}

class LinkRequest(BaseModel):
    long_url: str

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/api/generate")
async def generate_link(link_request: LinkRequest):
    short_code = generate_short_code()
    links_db[short_code] = link_request.long_url
    return {"shortLink": f"https://live-music.pages.dev/link/{short_code}"}

@app.get("/link/{short_code}")
async def redirect_link(short_code: str):
    long_url = links_db.get(short_code)
    if not long_url:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")

    html_content = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url={long_url}">
        <script>
            setTimeout(() => {{
                window.location.href = "https://play.google.com/store/apps/details?id=com.live.music";
            }}, 3000);
        </script>
    </head>
    <body>
        Si tu app no abre automáticamente, <a href="https://play.google.com/store/apps/details?id=com.live.music">haz clic aquí</a>.
    </body>
    </html>
    """
    return html_content
