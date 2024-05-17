from fastapi import FastAPI
from .auth.routers import router as auth_router
from .login.routers import router as login_router
from .books.routers import router as book_router
from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/", include_in_schema=False)
def homepage():
    return RedirectResponse(url="/docs/")


app.include_router(auth_router,
                   prefix='/user',
                   tags=['user'])

app.include_router(login_router,
                   prefix='/login',
                   tags=['login'])

app.include_router(book_router,
                   prefix='/book',
                   tags=['book'])