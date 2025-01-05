import io
import random
from pathlib import Path
from time import sleep, perf_counter

import requests
from PIL import Image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from bulk_rename import bulk_rename


def next_image() -> None:
    try:
        sleep(random.random())
        driver.execute_script("document.getElementsByClassName('_afxw')[0].click();")
        sleep(2 + random.random())
    except Exception as e:
        print(f'Exception: {e}')

def get_image_urls() -> list[str]:
    """Get all image urls in the current page"""
    return driver.execute_script(
        "let urls = []; \
        let n = document.getElementsByClassName('x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3'); \
        urls.push(n[0].getAttribute('src'), n[1].getAttribute('src'), n[2].getAttribute('src')); \
        return urls;"
    )

def download_image(url: str, name: str, download_path: str | Path) -> None:
    """Download image to the folder"""
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = Path(download_path, name)
        with open(file_path, 'wb') as f:
            image.save(f, 'JPEG')
    except Exception as e:
        print(f"Can't save image {name}, {url = }")
        print(f'Exception: {e}')

def clear_file(file_name: str) -> None:
    open(file_name, 'w').close()
    print(f'File {file_name} was cleared.')

# Initialize Selenium
time_start = perf_counter()
options = webdriver.ChromeOptions() 
options.add_argument('--start-maximized')
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)

# Make folder 'Downloaded' if not exist
folder_name = 'Downloaded'
download_folder = Path(folder_name)
if not download_folder.exists():
    download_folder.mkdir()

file_name = 'urls.txt'
with open(file_name, 'r') as f:
    data = f.read()

urls = [url for url in data.splitlines() if url]

# Main program
bulk_rename(folder_name)  # Bulk-rename to prevent overwrite other images
name = len(list(download_folder.glob('*'))) + 1
for url in urls:
    image_urls_in_post = set()
    driver.get(url)
    sleep(random.random()*2 + 5)  # Wait for fully loaded
    n_images = driver.execute_script("return document.getElementsByClassName('_acnb').length;")

    try:
        sleep(random.random()*1 + 2)
        if n_images == 0:  # Handle when the post has 1 image only
            image_urls = get_image_urls()
            download_image(image_urls[0], f'{name}.jpg', download_folder)
            name += 1
        elif n_images <= 3:
            if n_images == 3:  # All images will be loaded if go to the next image
                next_image()

            image_urls = get_image_urls()
            for i in range(n_images):
                download_image(image_urls[i], f'{name+i}.jpg', download_folder)
            name += n_images 
        else:
            # TODO - Fix: sometimes downloaded irrelevent images
            image_urls_in_post = set()
            for i in range(n_images - 1):
                next_image()
                image_urls_in_post.update(get_image_urls())
            
            for url in image_urls_in_post:
                download_image(url, f'{name}.jpg', download_folder)
                name += 1

    except Exception as e:
        print(f'Exception: {e}')
        continue

print(f'Done, took {(perf_counter() - time_start) / 60:.4f} mins.')
driver.quit()
clear_file(file_name)