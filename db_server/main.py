from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from . import router

app = FastAPI()

@app.get('/')
async def Home():
    res ='''
    <html>
        <body>
            <h2>DB Server</h2>
        </body>
    </html>
    '''
    return HTMLResponse(res)

app.include_router(router.route)
