import re
import random


def validate_url(url: str) -> bool:

    url_pattern = r"^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d{1,5})?(?:\/[^\s?#]*)?(?:\?[^\s#]*)?(?:#[^\s]*)?$"
    match = re.fullmatch(url_pattern, url)

    return match is not None


capital_alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lower_alphabets = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"


def generate_random_code(code_length: int | None = None) -> str:
    code = ""

    if not code_length:
        code_length = 10

    choices = [capital_alphabets, lower_alphabets, numbers]

    while len(code) < code_length:
        choice = random.choice(choices)
        char = random.choice(choice)

        code += char

    return code
