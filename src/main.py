import uvicorn
from fastapi import FastAPI

from src.lifespan import lifespan
from src.summaries.router import summaries_router
from src.parsers.router import parsers_router
from src.summarizers.router import summarizers_router


app = FastAPI(lifespan=lifespan)

app.include_router(summaries_router)
app.include_router(parsers_router)
app.include_router(summarizers_router)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000)