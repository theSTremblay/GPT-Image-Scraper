import tkinter as tk
from tkinter import simpledialog
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import requests
import time
import os
import base64
import glob
from tkinter import simpledialog, Toplevel, Radiobutton, Label, Entry, Button
import ast
import json
import requests
import random


# Call me paranoid, but I've always felt a scraper should feel like
# a person is clicking through the items
# So I've added a random sleep function to simulate a person
# Feel free to remove it if you don't want it
def random_sleep():
    """
    Sleeps for a random duration between 0.5 and 2.5 seconds.
    """
    duration = random.uniform(0.5, 2.5)
    print(f"Sleeping for {duration:.2f} seconds.")
    time.sleep(duration)


def capture_canvas(driver, canvas_element, output_file):
    try:
        # Use the screenshot_as_base64 property of the WebElement to get the image data
        base64_image = canvas_element.screenshot_as_base64

        # Decode the base64 data to binary image data
        image_data = base64.b64decode(base64_image)

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        # Write the data to an image file
        with open(output_file, 'wb') as file:
            file.write(image_data)
        return True
    except Exception as e:
        print(f"Error capturing canvas: {e}")
        return False
def capture_and_save_image(driver, css_selector, output_path):
    """
    Captures an image from the web page using the given CSS selector and saves it to the specified path.

    Parameters:
    - driver: The Selenium WebDriver instance.
    - css_selector: CSS selector to find the image element.
    - output_path: Path to save the captured image.
    """
    try:
        # Find the image element
        image_element = css_selector
        return capture_canvas(driver, image_element, output_path)

    except Exception as e:
        print(f"Error capturing or saving image: {e}")
        return False

def click_canvas_and_turn_page(driver, canvas_selector, strategy = None):
    """
    Clicks on the canvas element and then hits the left arrow key.

    Parameters:
    - driver: The Selenium WebDriver instance.
    - canvas_selector: The CSS selector for the canvas element.
    """
    # Find the canvas element
    try:

        canvas = canvas_selector

        # Create an ActionChains object passing the driver instance
        actions = ActionChains(driver)

        # Click on the canvas
        actions.click(canvas)

        # Send the LEFT arrow key press to turn the page
        if strategy == 3:
            actions.send_keys(Keys.ARROW_RIGHT)
        elif strategy == 4:
            actions.send_keys(Keys.ARROW_LEFT)

        # Perform the actions
        actions.perform()

        # Wait for 1 second to allow the page to load
        time.sleep(1)
        random_sleep()
    except Exception as e:
        print(f"Error finding canvas element: {e}")
        return


def count_png_files(directory):
    """
    Counts the number of PNG files in the specified directory.

    Parameters:
    - directory: The path to the directory where the PNG files are located.

    Returns:
    - The count of PNG files in the directory.
    """
    # Create a pattern for all .png files
    pattern = os.path.join(directory, '*.png')

    # Use glob to list all files matching the pattern
    png_files = glob.glob(pattern)

    # Return the count of the PNG files
    return len(png_files)

def navigate_and_capture_images(driver, image_selector, next_page_selector, output_directory, max_pages=None, strategy = None):
    """
    Navigates through web pages and captures images based on the provided selectors.

    Parameters:
    - driver: The Selenium WebDriver instance.
    - image_selector: CSS selector for images to capture.
    - next_page_selector: CSS selector to find the "next page" button/link.
    - output_directory: Directory to save the captured images.
    - max_pages: Maximum number of pages to scrape (for preventing infinite loops); if None, will continue until no more pages are found.
    """

    try:
        while True:
            # Check if maximum pages limit is reached
            #if max_pages is not None and page_count >= max_pages:
            #    break

            # Capture and save image from the current page
            page_count = count_png_files(output_directory) + 1
            image_path = os.path.join(output_directory, f'image_{page_count}.png')
            image_saved_flag = False
            image_saved_flag = capture_and_save_image(driver, image_selector, image_path)

            if not image_saved_flag:
                print("No image found or error capturing image.")
                return False

            # Try to find and click the "next page" button
            try:
                #Pass image_selector as the canvas element
                next_page_element = image_selector
                next_page_element.click()
            except Exception:

                print("No more pages or next page selector not found.")
                return False

            if strategy is None:
                break
            elif strategy == 1:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elif strategy == 2:
                break
            elif strategy == 3:
                click_canvas_and_turn_page(driver, image_selector, strategy=strategy)
            elif strategy == 4:
                click_canvas_and_turn_page(driver, image_selector, strategy=strategy)
            elif strategy == 5:
                driver.find_element(By.CSS_SELECTOR, next_page_selector).click()


            page_count += 1
        return True
    except Exception as e:
        print(f"Error during navigation and capture: {e}")
        return False

def ask_for_url():
    # Initialize Tkinter root
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # Ask for URL
    url = simpledialog.askstring("URL Input", "Enter the URL to scrape:")
    return url


def ask_user_for_selectors(driver):
    def submit():
        nonlocal image_selector, next_page_action, selector_description
        image_selector = image_input.get()
        if v.get() == 1:
            next_page_action = 'scroll'
            selector_description = ''
        elif v.get() == 2:
            next_page_action = 'none'
            selector_description = ''
        else:
            next_page_action = 'click_selector'
            selector_description = selector_input.get()
        popup.destroy()

    # Inject the click catcher
    inject_click_catcher(driver)

    # Now, when the user clicks an element on the page, an alert will show the CSS selector path.
    # This is a manual process. You need to manually copy the selector from the alert.
    # Then, use the copied selector to get the HTML content of the element as needed.

    # Assuming you have the selector from the user:
    selector = input("Enter the selector: ")  # For demonstration, use the selector copied by the user

    selector_list = extract_and_save_last_selectors(driver, selector)
    #element = driver.find_element_by_css_selector(selector)

    image_selector, next_page_action, selector_description = None, None, None

    popup = tk.Toplevel()
    popup.title("Input Selectors")
    tk.Label(popup, text="Describe what to look for to get the images:").pack()

    image_input = tk.Entry(popup)
    image_input.pack()

    tk.Label(popup, text="Choose the method for getting next page of images:").pack()
    v = tk.IntVar()

    tk.Radiobutton(popup, text="Scroll to the bottom to get more images", variable=v, value=1).pack(anchor=tk.W)
    tk.Radiobutton(popup, text="No other pages", variable=v, value=2).pack(anchor=tk.W)
    tk.Radiobutton(popup, text="Click a selector and scroll left", variable=v, value=3).pack(anchor=tk.W)
    tk.Radiobutton(popup, text="Click a selector and scroll right", variable=v, value=4).pack(anchor=tk.W)
    tk.Radiobutton(popup, text="Click a selector", variable=v, value=5).pack(anchor=tk.W)

    tk.Label(popup, text="If 'Click a selector' is chosen, describe the selector:").pack()
    selector_input = tk.Entry(popup)
    selector_input.pack()

    submit_button = tk.Button(popup, text="Submit", command=submit)
    submit_button.pack()

    popup.grab_set()  # Make the popup window modal.
    popup.wait_window()  # Wait here until the popup is destroyed.

    # After popup is destroyed, these variables are filled with user input.
    try:
        return image_selector, next_page_action, selector_description, v, selector_list
    except NameError:  # In case the window is closed without submission
        return None, None, None, None, None



def navigate_and_grab_html(url, driver):
    # Setup WebDriver

    # Navigate
    driver.get(url)

    # Grab HTML
    html_content = driver.page_source

    return html_content

def split_html_into_chunks(html_content, max_tokens=30000):
    """
    Splits the HTML content into chunks, each with a maximum token count.

    Parameters:
    - html_content: The full HTML content as a string.
    - max_tokens: The maximum token count for each chunk (default: 15000).

    Returns:
    - A list of HTML content chunks, each within the specified token limit.
    """
    # Tokenize the HTML content by spaces to approximate tokenization
    words = html_content.split(' ')

    # Initialize variables to hold chunks and current chunk content
    chunks = []
    current_chunk = []

    # Track the approximate token count in the current chunk
    current_token_count = 0

    for word in words:
        # Estimate token count for the word; add 1 for space or new token
        word_token_count = len(word) + 1

        # Check if adding this word would exceed the max token count
        if current_token_count + word_token_count > max_tokens:
            # Join the current chunk's words and add to the chunks list
            chunks.append(' '.join(current_chunk))
            # Reset the current chunk and token count
            current_chunk = [word]
            current_token_count = word_token_count
        else:
            # Add the word to the current chunk and update the token count
            current_chunk.append(word)
            current_token_count += word_token_count

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def generate_message(description_prompt, html_prompt):
    messages = [
        {"role": "system",
         "content": "Background: A Python script using the Selenium library is being developed to scrape images from web pages. The task involves identifying CSS selectors within the page's HTML that target image elements or navigation controls based on specific descriptions. The goal is to derive a generic CSS selector and a strategy that can be applied to the `find_element` method in Selenium, similar to: `driver.find_element(By.CSS_SELECTOR, '#modal-reader-header h2')`."},
        {"role": "system",
         "content": "Task: Based on the provided HTML content and a description of the target images or navigation elements, return a CSS selector that can be used to locate these elements within the page. Provide the output in the format: `[\"By.CSS_SELECTOR\", \"#selector_example\"]`, where `#selector_example` is the suggested CSS selector."},
        {"role": "system",
         "content": f"Description of target elements: {description_prompt}"},
        {"role": "system",
         "content": f"HTML Content: {html_prompt}"},
        {"role": "user",
         "content": "What is the CSS selectors of the described image container in the HTML Content? canvas, img, or another image hosting HTML component. If the right element is not found return 'None' rather than a CSS selector. only send a 'None' or a CSS selector in the format [\'By.CSS_SELECTOR\', \'#selector_example\'] no other text is needed."}]
    return messages


def generate_and_send_messages(API_ENDPOINT, API_KEY, description_prompt, html_content, user_selected):
    # Split the HTML content into manageable chunks
    html_chunks = split_html_into_chunks(user_selected)

    for chunk in html_chunks:
        # Generate the message for the current chunk
        messages = generate_message(description_prompt, chunk)

        # Send the message to the API and handle the response
        try:

            response_text = generate_chat_completion(API_ENDPOINT, API_KEY, messages)
            if "None" not in response_text:
                print("JSON found")
                return response_text
            # Process the response_text here, e.g., by extracting CSS selectors
        except Exception as e:
            print(f"Error during API call: {e}")
            # Handle the error, e.g., by continuing to the next chunk or stopping
    return "None"


def inject_click_catcher(driver):
    script = """
    document.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        var path = [];
        for (var element = event.target; element && element.nodeType === Node.ELEMENT_NODE; element = element.parentNode) {
            var selector = element.nodeName.toLowerCase();
            if (element.id) {
                selector += '#' + element.id;
            } else if (element.className && typeof element.className === 'string') {
                selector += '.' + element.className.split(/\\s+/).join('.');
            }
            path.unshift(selector);
        }

        var display = document.getElementById('customSelectorDisplay');
        if (!display) {
            display = document.createElement('textarea');
            display.id = 'customSelectorDisplay';
            display.style.position = 'fixed';
            display.style.top = '10px';
            display.style.left = '10px';
            display.style.width = '300px';
            display.style.height = '100px';
            display.style.zIndex = 10000;
            document.body.appendChild(display);
        }

        display.value = path.join(' > ');
        display.focus();
        display.select();
    }, true);
    """
    driver.execute_script(script)


def parse_response_and_find_element(driver, response_text):
    """
    Parses the response text to extract the selector method and value,
    then uses these to find an element with Selenium.

    Parameters:
    - driver: The Selenium WebDriver instance.
    - response_text: The response text from the API, e.g., "['By.CSS_SELECTOR', 'meta[property=\"og:image\"]']".
    """
    # Safely evaluate the response text to convert it into a list
    response_list = ast.literal_eval(response_text)

    # Extract the method and selector value
    method, value = response_list

    # Map the method string to the Selenium By attribute
    method_mapping = {
        "By.ID": By.ID,
        "By.CSS_SELECTOR": By.CSS_SELECTOR,
        "By.XPATH": By.XPATH,
        "By.NAME": By.NAME,
        "By.TAG_NAME": By.TAG_NAME,
        "By.CLASS_NAME": By.CLASS_NAME,
        "By.LINK_TEXT": By.LINK_TEXT,
        "By.PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT
    }

    # Find the element using the dynamically determined method and value
    if method in method_mapping:
        test = method_mapping[method]
        element = driver.find_element(method_mapping[method], value)
        return element , method_mapping[method], value
    else:
        print(f"Unsupported method: {method}")
        return None


def extract_and_save_last_selectors(driver, full_selector):
    # Split the full selector into individual selectors
    selectors = [s.strip() for s in full_selector.split('>')]

    # Take the last three selectors, handling cases where there are fewer than three
    last_selectors = selectors[-3:] if len(selectors) >= 3 else selectors

    # List to store the outer HTML of elements found by the last three selectors
    elements_html = []

    for selector in last_selectors:
        try:
            # Find the element using the current selector and get its outer HTML
            element = driver.find_element(By.CSS_SELECTOR, selector)
            element_html = element.get_attribute('outerHTML')

            # Add the element's outer HTML to the list
            elements_html.append(element_html)
        except Exception as e:
            print(f"Error finding element with selector '{selector}': {e}")
            # Optionally, append None or an error message to elements_html list
            elements_html.append(None)

    return elements_html
def generate_chat_completion(API_ENDPOINT, API_KEY, messages, model="gpt-3.5-turbo", temperature=1, max_tokens=None):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens



    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")



def scrape_with_user_input(url=None):

    # Set the endpoint URL
    endpoint = "https://api.openai.com/v1/chat/completions"

    # Set the API key (YOU WILL NEED TO DO THIS BEFORE DOING ANYTHING ELSE)
    #Create an account on OpenAI and get an API key
    #You can check out their tutorial:  https://platform.openai.com/docs/quickstart?context=python
    API_KEY = ""

    API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

    output_directory = os.path.join(os.getcwd(), 'web_scrapings')
    os.makedirs(output_directory, exist_ok=True)



    # Prompt for URL if not provided
    if url is None:
        url = ask_for_url()

    # Validate URL
    if not url:
        print("No URL provided. Exiting.")
        return

    options = webdriver.ChromeOptions()
    # options.headless = True  # Uncomment if you don't need a browser UI
    driver = webdriver.Chrome(options=options)


    # Navigate to the page and grab HTML
    html_content = navigate_and_grab_html(url, driver=driver)

    # Prompt the user for input
    image_selector, next_page_action, selector_description, radio_select, selectors = ask_user_for_selectors(driver)


    #messages = generate_message(image_selector, html_content)
    element = None
    found_flag = False
    selectors = reversed(selectors)
    for element_user_selected in selectors:
        try:
            response_text = generate_and_send_messages(API_ENDPOINT, API_KEY, selector_description, html_content, element_user_selected)
        except:

            print("Something broke while generating the message from GPT -_-. Please debug "
                  "by stepping through the code")
            return
        try:
            if response_text == "None":
                print("No CSS selector found. Exiting.")
                continue
            else:
                element, method, value = parse_response_and_find_element(driver, response_text)
        except:
            print("Something broke while parsing the doc -_-. Please debug "
                  "by making sure the selectors GPT is selecting are correct")
            return


        try:
            found_flag = navigate_and_capture_images(driver, element, next_page_action, output_directory, max_pages=None, strategy=radio_select)
        except:
            print("Something broke while parsing the doc AND saving the file -_-. Please debug "
                  "by making sure the selectors GPT is selecting are correct")
            return
        if found_flag is True:
            print("image saved")
            break

    # Placeholder for GPT integration and further processing
    print(f"HTML Content Length: {len(html_content)}")
    print(f"Image Selector Description: {image_selector}")
    print(f"Next Page Action: {next_page_action}")
