import base64

from langchain_huggingface.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
import requests
from PIL import Image, ImageFont, ImageDraw

def create_quote(model, max_new_tokens: int, rep=0) -> str:
    if rep == 0:
        TextMaker = HuggingFacePipeline.from_model_id(
            model_id=model,
            task='text-generation',
            pipeline_kwargs={'max_new_tokens': max_new_tokens, 'temperature': 0.8, 'do_sample': True}
        )
    else:
        TextMaker = model
    prompt = PromptTemplate.from_template("""
    User: Make a quote that sounds really smart, but in reality is actually really dumb and nonsensical. Also come up with a background image in parentheses. DO NOT WRITE ANY CODE FOR THE OUTPUT.
    AI: [Image of brick wall] At times, a street is nothing but a street.
    User: Make a quote that sounds really smart, but in reality is actually really dumb and nonsensical. Also come up with a background image in parentheses. DO NOT WRITE ANY CODE FOR THE OUTPUT.
    AI: [Image of the sunset] I like watermelons very much.
    User: Make a quote that sounds really smart, but in reality is actually really dumb and nonsensical. Also come up with a background image in parentheses. DO NOT WRITE ANY CODE FOR THE OUTPUT.
    AI: 
    """)
    chain = prompt | TextMaker
    quote = chain.invoke({})
    quote = quote.replace(prompt.format(), "")
    if quote.__contains__("def "):
        quote = create_quote(TextMaker, max_new_tokens, 1)

    return quote.splitlines()[0]


def create_image(prompt: str, imageURL: str, outputPath: str):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "steps": 5
    }

    response = requests.post(url=f'{imageURL}/sdapi/v1/txt2img', json=data, headers=headers)

    if response.status_code == 200:
        with open(outputPath, 'wb') as f:
            try:
                f.write(base64.b64decode(response.json()['images'][0]))
            except KeyError:
                print("Error: ", response.json())
    else:
        print(f"Request failed with status code {response.status_code}")

def get_wrapped_text(text: str, font: ImageFont.ImageFont,
                     line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return '\n'.join(lines)


def overlay_text_on_image(image_path: str, text: str):
    image = Image.open(image_path)
    W, H = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("RobotoSlab-Black.ttf", 32)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    # https://blog.lipsumarium.com/caption-memes-in-python/
    text = get_wrapped_text(text, font, W)
    draw.text(((W-w)/2, (H-h)/2), text, font=font, fill='white')
    image.save(image_path)
