import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import postie
from api import stash
from ui import stash as stash_ui

api_prefix = '/api'
# APP
app = FastAPI()
app.mount("/static", StaticFiles(directory="resources/public"), name="static")
# -- API --
app.include_router(postie.router, prefix=api_prefix)
app.include_router(stash.router, prefix=api_prefix)
# -- UI --
app.include_router(stash_ui.router)


def main():
    uvicorn.run(app)


if __name__ == "__main__":
    main()
