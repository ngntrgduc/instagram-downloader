## instagram-downloader
Instagram images downloader, built with Python + Selenium.

### Install requirements:
```pip
pip install -r requirements.txt
```

### How to use 
Create new file named `urls.txt` and then paste Instagram post URLs to it, please make sure that post **does not contain videos, just images**. Then, run program:
```py
py main.py
```

### Todo
- [ ] Fix: sometimes downloaded irrelevent images
- [ ] Handle video in post?
- [ ] Refactor code or change the download approach