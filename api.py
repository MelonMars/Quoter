import base64

from fastapi import FastAPI
import random
import re
import quoter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/quote")
async def get_quote():
    model = "microsoft/phi-2"
    max_new_tokens = 40
    nameFile = "names.txt"
    imageURL = "http://127.0.0.1:7860/"
    quote = quoter.create_quote(model, max_new_tokens)
    with open(nameFile, "r") as f:
        lines = f.readlines()
        person = random.choice(lines)
    pattern = r"\[(.*?)\]"
    background = re.search(pattern, quote).group(1)
    quote += " - " + person.strip()
    print(quote)
    out = "out.png"
    quoter.create_image(background, imageURL, out)
    quoter.overlay_text_on_image(out, quote.replace(background, "").replace("[", "").replace("]", ""))

    with open(out, "rb") as f:
        return {"Message": base64.b64encode(f.read())}

