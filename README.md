# GPT-Image-Scraper

A robust Image Scraper that leverages OpenAI's GPT Chat Completions and Selenium to determine the relevant HTML used to Scrape Images from websites. 

## Description

Broadly the scraper requires limited knowledge of HTML or CSS so if you code mostly backend REJOICE! 

There are two areas that require manual input at the start:

```bash
1: Terminal Input: When you navigate to the URL you are parsing you will need to click on the image and a popup will show you the html of the page- copy this and input it into the input in your terminal or IDE
2: Tkinter GUI Input: Will prompt you to describe the field you want to parse. The fields are optional but tell GPT what to look for more precisely- the better your description the better the output should be- you can play around with it. 
```
TODO: Educational, since the output is not always accurate. Working on testing it on more websites and testing more of the "page turning" functions. Still working on that

## Getting Started

### Dependencies
  Python 3 - (3.10 or greater if troubleshooting)

## Installation

These are the necessary libraries for this project written into pip commands:

```bash
pip install selenium
pip install requests
```

### Installing


*  API_KEY in GPT_utils is needed before starting. It is what holds the OpenAI credentials. Making an Open AI account and troubleshooting can be found here:

https://platform.openai.com/docs/quickstart?context=python

### Executing program

* Try Running from an IDE at first
* Be aware of the two Inputs at the start of the program one in the terminal and the other in the tkinter popup- after that it should be automated and download the image to webscrapings

## Considerations

* This code leverage OpenAI's API - a paid platform 
* OpenAI's account and pricing models can be found here: https://openai.com/pricing

## More-to-Come

I have run through a set of examples. I plan to be uploading gifs later and making bug fixes soon

The code may need to be made more robust I'll work on that after the inital commit


