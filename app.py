from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_users import fastapi_users, FastAPIUsers
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from markupsafe import Markup

app = FastAPI(
    title='IU9 Server'
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# TODO переделать это в базу данных
testing_contests = [
    {
        'name': 'Очень большое название контеста',
        'id': 1,
        'tasks': [
            {
                'name': 'A+B',
                'id': 1,
                'solved': 1
            },
            {
                'name': 'Ну очень тупая задача',
                'id': 2,
                'solved': 0
            }
        ]
    },

    {
        'name': 'Маленькое',
        'id': 2,
    },

    {
        'name': 'Тоже контест',
        'id': 3
    }
]

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", tags=['ROOT'])
async def hello():
    return FileResponse("templates/login.html")

# регистрация
@app.get("/registration", response_class=HTMLResponse)
async def read_em(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "username": 'Лох'})

current_user = fastapi_users.current_user()

# главный экран пользователя
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("home.html", {"request": request, "username": user.username, "contests": testing_contests})

# Страница с заданием
@app.get("/contest/{contest_id}", response_class=HTMLResponse)
async def home(contest_id: int, request: Request, user: User = Depends(current_user)):
    tasks = testing_contests[contest_id-1].get('tasks')
    print(tasks)
    return templates.TemplateResponse("contest.html", {"request": request, "username": user.username, "tasks": tasks})
