from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal
from app.models import Urls, Passwords
from app.schemas import ShortenUrl

from app.utils import validate_url

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/shorten")
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
def get_url(url_id: str, db: Session = Depends(get_db)):
    url = db.get(Urls, url_id)

    if not url:
        return HTTPException(404, detail="Page not found")

    return RedirectResponse(url.url)
