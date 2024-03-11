import asyncio

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from . import router

app = FastAPI()

@app.get('/')
async def Home():
    res ='''
    <html>
        <body>
            <h2>Notifier Service</h2>
        </body>
    </html>
    '''
    return HTMLResponse(res)

app.include_router(router.route)
asyncio.create_task(router.consume())