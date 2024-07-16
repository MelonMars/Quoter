import argparse
import random
import re
import quoter

parser = argparse.ArgumentParser(description='Quoter')
parser.add_argument("--model", type=str, help="huggingface model id", default="microsoft/phi-2")
parser.add_argument("--max_new_tokens", type=int, help="Max new tokens to generate", default=40)
parser.add_argument("--nameFile", type=str, help="File containing names for misattribution", default="names.txt")
parser.add_argument("--imageURL", type=str, help="URL of the stable diffusion API", default="http://127.0.0.1:7860/")
parser.add_argument("--out", type=str, help="Output file", default="output.png")
args = parser.parse_args()

quote = quoter.create_quote("microsoft/phi-2", 40)

with open("names.txt", "r") as f:
    lines = f.readlines()
    person = random.choice(lines)

pattern = r"\[(.*?)\]"
background = re.search(pattern, quote).group(1)
quoter.create_image(background, args.imageURL, args.out)
print(quote + " - " + person.strip())
