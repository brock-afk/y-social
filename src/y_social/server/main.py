from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Y Social</title>
        </head>
        <body>
            <h1>Y Social</h1>
            <p>Y Social is a social media platform.</p>
        </body>
    </html>"""
