import random
import re

import bcrypt


def validate_url(url: str) -> bool:

    url_pattern = r"^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d{1,5})?(?:\/[^\s?#]*)?(?:\?[^\s#]*)?(?:#[^\s]*)?$"
    match = re.fullmatch(url_pattern, url)

    return match is not None


def generate_code() -> str:
    alphanumeric = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVYZ"
    code = ""

    for i in range(6):
        code += random.choice(alphanumeric)

    return code


def hash_pw(password: str) -> str:
    pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return pw


def check_pw(pw: str, hashed_pw: str) -> bool:
    return bcrypt.checkpw(pw.encode(), hashed_pw.encode())
