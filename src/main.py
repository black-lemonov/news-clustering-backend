from fastapi import FastAPI

from src.lifespan import lifespan
from src.routers.ratings import ratings_router
from src.routers.summaries import summaries_router


app = FastAPI(lifespan=lifespan)

app.include_router(summaries_router)
app.include_router(ratings_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", reload=True)