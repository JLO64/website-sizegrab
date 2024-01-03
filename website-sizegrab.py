import requests, os, shutil

URL = "https://www.julianlopez.net/"

# set up a temporary directory
webdir = "/tmp/website-sizegrab"
if os.path.exists(webdir): shutil.rmtree(webdir)
os.makedirs(webdir, exist_ok=True)
os.chdir(webdir)

# Grab HTML
response = requests.get(URL)
html = response.text
with open("page.html", 'w') as f:
    f.write(html)
