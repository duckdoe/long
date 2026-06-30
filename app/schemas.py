from pydantic import BaseModel


class ShortenUrl(BaseModel):
    """
    Base request model for recieving url shortening requests
    """

    url: str
    password: str | None = None  # shortened urls can contain a password


class UnlockUrl(BaseModel):
    """
    Base request model for unlocking a protected url
    """

    password: str
