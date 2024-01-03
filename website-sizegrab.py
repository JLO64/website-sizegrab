import requests, os, shutil, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def calculate_directory_size(directory_path):
    total_size = 0
    for entry in os.scandir(directory_path):
        if entry.is_file():
            # if it's a file, use stat() function
            total_size += entry.stat().st_size
        elif entry.is_dir():
            # if it's a directory, recursively call this function
            total_size += calculate_directory_size(entry.path)
    return total_size

def calculate_website_size_data(URL):
    if not 'http' in URL: return {"total": 0}
    
    sizedict = {}

    # set up a temporary directory
    webdir = "/tmp/website-sizegrab"
    if os.path.exists(webdir): shutil.rmtree(webdir)
    os.makedirs(webdir + "/img")
    os.makedirs(webdir + "/html")
    os.makedirs(webdir + "/scripts")
    os.makedirs(webdir + "/styles")
    os.makedirs(webdir + "/fonts")

    # Grab HTML
    os.chdir(webdir + "/html")
    response = requests.get(URL)
    html = response.text
    with open("page.html", 'w') as f: f.write(html)
    sizedict['html'] = calculate_directory_size(webdir + "/html")

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
    sizedict['img'] = calculate_directory_size(webdir + "/img")

    # Parse HTML for scripts
    os.chdir(webdir + "/scripts")
    script_tags = soup.find_all('script')
    for script in script_tags:
        script_url = script.attrs.get("src")
        if not script_url: continue
        script_url = urljoin(URL, script_url)
        basename = os.path.basename(script_url)
        script_res = requests.get(script_url)
        with open(basename, 'wb') as f: f.write(script_res.content)
    sizedict['scripts'] = calculate_directory_size(webdir + "/scripts")

    # Parse HTML for stylesheets
    os.chdir(webdir + "/styles")
    link_tags = soup.find_all('link', rel='stylesheet')
    for link in link_tags:
        style_url = link.attrs.get("href")
        if not style_url: continue
        style_url = urljoin(URL, style_url)
        basename = os.path.basename(style_url)
        style_res = requests.get(style_url)
        with open(basename, 'wb') as f: f.write(style_res.content)
    sizedict['styles'] = calculate_directory_size(webdir + "/styles")

    # Parse stylesheets for fonts
    os.chdir(webdir + "/fonts")
    for stylesheet in os.listdir(webdir + "/styles"):
        with open(os.path.join(webdir + "/styles", stylesheet), 'r') as f:
            content = f.read()
        urls = re.findall(r'url\((.*?)\)', content)
        for url in urls:
            if url.startswith('//'):
                url = 'http:' + url
            elif url.startswith('/'):
                url = urljoin(URL, url)
            elif not url.startswith('http'):
                continue
            basename = os.path.basename(url)
            font_res = requests.get(url)
            with open(basename, 'wb') as f: f.write(font_res.content)
    sizedict['fonts'] = calculate_directory_size(webdir + "/fonts")
    # Parse HTML for fonts
    font_urls = re.findall(r'@font-face\s*{[^}]*src:\s*url\((.*?)\)', html)
    for url in font_urls:
        if url.startswith('//'):
            url = 'http:' + url
        elif url.startswith('/'):
            url = urljoin(URL, url)
        elif not url.startswith('http'):
            continue
        basename = os.path.basename(url)
        font_res = requests.get(url)
        with open(basename, 'wb') as f: f.write(font_res.content)
    sizedict['fonts'] += calculate_directory_size(webdir + "/fonts")

    sizedict['total'] = calculate_directory_size(webdir)

    return sizedict

website_size_data = calculate_website_size_data("https://www.blitzw.in/")
if website_size_data["total"] == 0: print("ERROR. Did you paste in the whole URL?")
for size_category in website_size_data:
    print(size_category,"size is:", str(round(website_size_data[size_category] / 1024.0, 2)) + "KB")

# Purge `output` folder
# shutil.rmtree(webdir)
