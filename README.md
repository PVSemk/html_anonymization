## HTML Anonymization
### Description
This repository contains a project on HTML anonymization.

We support parsing of custom urls and anonymization of all texts inside. It's implemented via BeatufilSoup, SpaCy and Presidio libraries.

Also we support downloading page's contents (scripts, images, css-files). **Note: This feature is unstable and may not work on a variety of pages**.
### Installation & Usage
To install the project follow the steps:
1. Install required packages with `pip install -r requirements.txt`
2. Run `python main.py [-h] --url URL [--output_folder OUTPUT_FOLDER]
               [--save_media_content] [--page_filename PAGE_FILENAME]`
Description of the arguments:
```
optional arguments:
  -h, --help            show this help message and exit
  --url URL             Url to website for anonymization
  --output_folder OUTPUT_FOLDER
                        Path to output folder
  --save_media_content  Try to store both the site's content (e.g images) and
                        text
  --page_filename PAGE_FILENAME
                        Filename to store the result html
```

### Examples
Examples and results can be found in folders `arxiv`, `rational_harry`, `edgar_po`.