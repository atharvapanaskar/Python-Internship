from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_home(request: Request, db: Session = Depends(get_db)):
    content = db.query(models.HomeContent).first()
    return templates.TemplateResponse("home.html", {"request": request, "content": content})


@app.get("/admin", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin")
def admin_login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin123":
        return RedirectResponse("/dashboard", status_code=303)
    return {"error": "Invalid Credentials"}



@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    content = db.query(models.HomeContent).first()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "content": content})

@app.post("/update")
def update_home(
    ngo_name: str = Form(...),
    about_text: str = Form(...),
    mission: str = Form(...),
    vision: str = Form(...),
    donation_link: str = Form(...),
    contact_email: str = Form(...),
    contact_phone: str = Form(...),
    db: Session = Depends(get_db)
):
    content = db.query(models.HomeContent).first()

    if not content:
        content = models.HomeContent()

    content.ngo_name = ngo_name
    content.about_text = about_text
    content.mission = mission
    content.vision = vision
    content.donation_link = donation_link
    content.contact_email = contact_email
    content.contact_phone = contact_phone

    db.add(content)
    db.commit()

    return RedirectResponse("/", status_code=303)
