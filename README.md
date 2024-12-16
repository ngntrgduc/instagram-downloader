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
- [ ] Handle video in post?
- [ ] Change the download approach?
- [ ] Speed up by using asyncio?
- [x] Refactor code 
- [x] Write script to bulk-rename all downloaded images -> prevent overwriting images when some images were deleted