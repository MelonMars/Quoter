from langchain_huggingface.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
import requests


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
                f.write(response.json()['images'][0])
            except KeyError:
                print("Error: ", response.json())
    else:
        print(f"Request failed with status code {response.status_code}")
