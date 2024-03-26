# GPT-Image-Scraper

A robust Image Scraper that leverages OpenAI's GPT Chat Completions and Selenium to determine the relevant HTML and uses it to Scrape Images from websites. 

## Description

Broadly the scraper requires limited to no knowledge of HTML or CSS so if you code mostly backend REJOICE! 

* Here is an educational example scraping an image header from an nba box score-this gives an idea of the tkinter window and the popup that will show when you click on an image. Go Bucks!

![Example](img/example1.gif)

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

The model I am using by default is gpt-3.5-turbo, there are other models like "gpt-4" you can take from the OpenAI website. 

### Executing program

* Try Running from an IDE at first
* Be aware of the two Inputs at the start of the program one in the terminal and the other in the tkinter popup- after that it should be automated and download the image to webscrapings

## Considerations

* This code leverage OpenAI's API - a paid platform 
* OpenAI's account and pricing models can be found here: https://openai.com/pricing

&nbsp;&nbsp; :flushed:	 &nbsp;         If you found any code helpful in the repo, drop a star sir. Helps out with the jobs sir


![](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExczh4MzNvcnphNTl1MnBiOXU3eDB4ODRjdWY0eDRiNDNiMHF0MWh6eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bLAyLX9obxrECmqJZ1/giphy.gif)

## More-to-Come

I have run through a set of examples. I plan to be uploading gifs later and making bug fixes soon

The code may need to be made more robust I'll work on that after the inital commit




