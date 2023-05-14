from fastapi import FastAPI
import configparser

from routers.book_router import book_router


config = configparser.ConfigParser()
config.read('config.ini')
port = config.getint('server', 'port')

app = FastAPI(
    title="Library"
)

app.include_router(book_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
