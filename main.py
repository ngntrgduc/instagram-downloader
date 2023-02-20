from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pathlib import Path
from time import sleep, time
from PIL import Image
import requests
import random
import io

def next_image():
    try:
        sleep(random.random())
        browser.execute_script("document.getElementsByClassName('_afxw')[0].click();")
        sleep(2 + random.random())
    except Exception as e:
        print(f'Exception: {e}')

def get_image_urls():
    return browser.execute_script("let urls = []; \
                                  let n = document.getElementsByClassName('x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3'); \
                                  urls.push(n[0].getAttribute('src'), n[1].getAttribute('src'), n[2].getAttribute('src')); \
                                  return urls;")

def download_image(url, name, download_path):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = Path(download_path, name)
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")         
    except Exception as e:
        print(f"Can't save image {name}")
        print('FAILED: ', e)


time_start = time()
options = webdriver.EdgeOptions() 
options.add_argument("--start-maximized")
browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

# Make folder 'Downloaded' if not exist
download_folder = Path('Downloaded')
if not download_folder.exists():
    download_folder.mkdir()

# Get post urls in urls.txt
try:
    with open('urls.txt', 'r') as f:
        post_urls = f.read().rstrip().split('\n')
    f.close()
except Exception as e:
    print(f'Exception: {e}')

# Main program
name = len(list(Path('Downloaded').glob('*'))) + 1
for url in post_urls:
    image_urls_in_post = set()
    browser.get(url)
    sleep(random.random()*2 + 5)
    nums_of_image = browser.execute_script("return document.getElementsByClassName('_acnb').length;")

    try:
        sleep(random.random()*1 + 2)
    
        if nums_of_image == 0:
            sleep(2 + random.random())
            image_urls = get_image_urls()
            download_image(image_urls[0], f'{name}.jpg', download_folder)
            name += 1
        elif nums_of_image == 2:
            sleep(2 + random.random())
            image_urls = get_image_urls()
            download_image(image_urls[0], f'{name}.jpg', download_folder)
            download_image(image_urls[1], f'{name+1}.jpg', download_folder)
            name += 2
        elif nums_of_image == 3:
            next_image()
            image_urls = get_image_urls()
            download_image(image_urls[0], f'{name}.jpg', download_folder)
            download_image(image_urls[1], f'{name+1}.jpg', download_folder)
            download_image(image_urls[2], f'{name+2}.jpg', download_folder)
            name += 3
        else:
            image_urls_in_post = set()
            for i in range(nums_of_image - 1):
                next_image()
                image_urls_in_post.update(get_image_urls())
            
            for url in image_urls_in_post:
                download_image(url, f'{name}.jpg', download_folder)
                name += 1
            
    except Exception as e:
        print(f'Exception: {e}')
        continue      

print(f'Done, took {time() - time_start} seconds.')
browser.quit()