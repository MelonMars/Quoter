import base64

from fastapi import FastAPI
import random
import re
import quoter


app = FastAPI()


@app.get("/quote")
async def get_quote(model: str, max_new_tokens: int, imageURL: str, out: str, nameFile: str = "names.txt"):
    quote = quoter.create_quote(model, max_new_tokens)
    with open(nameFile, "r") as f:
        lines = f.readlines()
        person = random.choice(lines)
    pattern = r"\[(.*?)\]"
    quote += "\n" + " - " + person.strip()
    background = re.search(pattern, quote).group(1)
    quoter.create_image(background, imageURL, out)
    quoter.overlay_text_on_image(out, quote.replace(background, ""))

    with open(out, "rb") as f:
        return {"Message": base64.b64encode(f.read())}
