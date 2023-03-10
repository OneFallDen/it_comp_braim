from fastapi import FastAPI

from routers import account_router, animal_router, location_router, reg_router

app = FastAPI()


app.include_router(account_router.router)
app.include_router(animal_router.router)
app.include_router(location_router.router)
app.include_router(reg_router.router)
