from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from . import router

app = FastAPI()
origins = [
   "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
