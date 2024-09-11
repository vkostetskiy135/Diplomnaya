from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from DiplomFastAPI.app.routers import user


app = FastAPI()
app.mount("/imgs", StaticFiles(directory="DiplomFastAPI/app/imgs"), name="imgs")

templates = Jinja2Templates(directory="DiplomFastAPI/app/templates")
@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

app.include_router(user.router)
