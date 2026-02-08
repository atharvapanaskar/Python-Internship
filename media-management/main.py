from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Create database tables
models.Base.metadata.create_all(bind=engine)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# View Media Page
@app.get("/media", response_class=HTMLResponse)
def media_page(request: Request, db: Session = Depends(get_db)):
    media_list = db.query(models.Media).all()
    return templates.TemplateResponse(
        "media.html",
        {"request": request, "media_list": media_list}
    )


# Media Dashboard
@app.get("/media-dashboard", response_class=HTMLResponse)
def media_dashboard(request: Request, db: Session = Depends(get_db)):
    media_list = db.query(models.Media).all()
    return templates.TemplateResponse(
        "media_dashboard.html",
        {"request": request, "media_list": media_list}
    )


# Add Media
@app.post("/add-media")
def add_media(
    title: str = Form(...),
    description: str = Form(...),
    image_url: str = Form(...),
    db: Session = Depends(get_db)
):
    new_media = models.Media(
        title=title,
        description=description,
        image_url=image_url
    )

    db.add(new_media)
    db.commit()

    return RedirectResponse("/media-dashboard", status_code=303)


# Delete Media
@app.get("/delete-media/{media_id}")
def delete_media(media_id: int, db: Session = Depends(get_db)):
    media = db.query(models.Media).filter(models.Media.id == media_id).first()
    if media:
        db.delete(media)
        db.commit()

    return RedirectResponse("/media-dashboard", status_code=303)
