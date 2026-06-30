from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Passwords, Urls
from app.schemas import ShortenUrl, UnlockUrl
from app.utils import validate_url

from sqlalchemy import select

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
template = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index(request: Request):

    return template.TemplateResponse(request, "index.html")


@app.post("/api/shorten")
def shorten_url(url: ShortenUrl, db: Session = Depends(get_db)):
    has_password = False
    is_valid_url = validate_url(url.url)

    if url.password is not None:
        has_password = True

    if not is_valid_url:
        return HTTPException(400, detail="Invalid url provided")

    new_url = Urls(url=url.url, has_password=has_password)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    if has_password:
        new_password = Passwords(
            password=url.password, url_id=new_url.id
        )  # change this and make sure to hash passwords
        db.add(new_password)
        db.commit()
        db.refresh(new_password)

    db.refresh(new_url)
    return new_url


@app.get("/u/{url_id}")
def get_url(url_id: str, request: Request, db: Session = Depends(get_db)):
    url = db.get(Urls, url_id)

    if not url:
        return HTTPException(404, detail="Page not found")

    if url.has_password:
        return template.TemplateResponse(
            request,
            "unlock.html",
        )

    return RedirectResponse(url.url)


@app.post("/api/unlock/{code}")
def unlock_url(code: str, lock: UnlockUrl, db: Session = Depends(get_db)):
    pw = db.scalars(select(Passwords).where(Passwords.url_id == code)).first()

    if not pw:
        return HTTPException(503, detail="not password protected")

    if pw.password != lock.password:
        return HTTPException(401, detail="Incorrect password")

    url = db.get(Urls, code)

    if url is None:
        return HTTPException(404, detail="url not found")

    return {"status_code": 200, "url": url.url}
