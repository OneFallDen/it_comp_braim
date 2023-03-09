from fastapi import FastAPI

from routers import account_router, animal_router

app = FastAPI()


app.include_router(account_router.router)
app.include_router(animal_router.router)
