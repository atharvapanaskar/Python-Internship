from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

app = FastAPI()
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return HTMLResponse("<h1>NGO Website Running Successfully</h1>")

@app.get("/about-dashboard", response_class=HTMLResponse)
def about_dashboard(request: Request, db: Session = Depends(get_db)):
    about = db.query(models.AboutUs).first()
    return templates.TemplateResponse(
        "about_dashboard.html",
        {"request": request, "about": about}
    )

@app.post("/update-about")
def update_about(
    history: str = Form(...),
    objectives: str = Form(...),
    achievements: str = Form(...),
    core_values: str = Form(...),
    db: Session = Depends(get_db)
):
    about = db.query(models.AboutUs).first()

    if not about:
        about = models.AboutUs()

    about.history = history
    about.objectives = objectives
    about.achievements = achievements
    about.core_values = core_values

    db.add(about)
    db.commit()

    return RedirectResponse("/about", status_code=303)
