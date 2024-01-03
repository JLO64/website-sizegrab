import requests, os, shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.julianlopez.net/about"

# set up a temporary directory
webdir = "/tmp/website-sizegrab"
if os.path.exists(webdir): shutil.rmtree(webdir)
os.makedirs(webdir)
os.makedirs(webdir + "/img")
os.chdir(webdir)

# Grab HTML
response = requests.get(URL)
html = response.text
with open("page.html", 'w') as f: f.write(html)

# Parse HTML for images
os.chdir(webdir + "/img")
soup = BeautifulSoup(html, 'html.parser')
img_tags = soup.find_all('img')
for img in img_tags:
    img_url = img.attrs.get("src")
    if not img_url: continue
    img_url = urljoin(URL, img_url)
    basename = os.path.basename(img_url)
    img_res = requests.get(img_url)
    with open(basename, 'wb') as f: f.write(img_res.content)
os.chdir(webdir)