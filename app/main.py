from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Passwords, Urls
from app.schemas import ShortenUrl, UnlockUrl
from app.utils import validate_url, hash_pw, check_pw, generate_code

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

    code = generate_code()
    while db.get(Urls, code) is not None:
        code = generate_code()

    new_url = Urls(id=code, url=url.url, has_password=has_password)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    if has_password:
        pw = hash_pw(str(url.password))

        new_password = Passwords(password_hash=pw, url_id=new_url.id)
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

    url.visits += 1  # add one to the visits
    return RedirectResponse(url.url)


@app.post("/api/unlock/{code}")
def unlock_url(code: str, lock: UnlockUrl, db: Session = Depends(get_db)):
    pw = db.scalars(select(Passwords).where(Passwords.url_id == code)).first()

    if not pw:
        return HTTPException(503, detail="Not password protected")

    if not check_pw(lock.password, pw.password_hash):
        return HTTPException(401, detail="Incorrect password")

    url = db.get(Urls, code)

    if url is None:
        return HTTPException(404, detail="Url not found")

    url.visits += 1  # add one to the clicks
    return {"status_code": 200, "url": url.url}


@app.get("/manage/{id}")
def manage(id: str, request: Request, db: Session = Depends(get_db)):
    url = db.scalars(select(Urls).where(Urls.clicks_token == id)).first()

    if not url:
        return HTTPException(404, "Page does not exists")

    return template.TemplateResponse(request, "manage.html")
