```
   ___     _   _    U  ___ u _____  U _____ u   ____
  / " \ U |"|u| |    \/"_ \/|_ " _| \| ___"|/U |  _"\ u
 | |"| | \| |\| |    | | | |  | |    |  _|"   \| |_) |/
/| |_| |\ | |_| |.-,_| |_| | /| |\   | |___    |  _ <
U \__\_\u<<\___/  \_)-\___/ u |_|U   |_____|   |_| \_\
   \\// (__) )(        \\   _// \\_  <<   >>   //   \\_
  (_(__)    (__)      (__) (__) (__)(__) (__) (__)  (__)
```

# Quoter

This is a program that uses AI to create fake quotes on fake backdrops, credited to random people selected from a txt.

## To run:
Install `requirements.txt` and then run the API with `uvicorn api:app`. Then you can either use it from running `term.py` or opening `site.html` in the browser.

You also need to install [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui), and run it with the commands `--api --cors-allow-origins * --use-cpu all --precision full --no-half --skip-torch-cuda-test`. Technically `--use-cpu` and `--skip-torch-cuda-test` are optional, but I need them for Stable diffusion to work, and I've only tested with it.

#### Web version:


Just open `site.html`, and then it's really straightforward.
The website should be ran on localhost, and only used for localhost.

#### Terminal version

Run `term.py` and the arguments are:
```
--model: The model that comes up with the quote. The default (and only one tested) in microsoft/phi-2
--max_new_tokens: The max length of the generated quote in tokens
--nameFile: file containing possible names, default is names.txt
--imageURL: URL of the stable diffusion API, gotten from the site that opens up when you run stable diffusion. The default is http://127.0.0.1:7860/
--out: Output filepath, will be created or overwritten. The default is output.png
```

Also, I would just like to point out that for some reason I get a lot of stuff about animals.
