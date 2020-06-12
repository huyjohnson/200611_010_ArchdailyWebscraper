#### - Webscraping version 1.0 -
#### - Dezeen - 

import re
import requests
import json
import shutil
from bs4 import BeautifulSoup

# Enter the URL of the webpage you want to download the images from
page = 'https://www.dezeen.com/2018/11/05/tadao-ando-wrightwood-659-architecture-exhibition-space-chicago/#/'
imgNum = 1
architectName = 'Tadao Ando Wrightwood'

# Custom namechange
def fileName(url_x):
    global imgNum
    fileName = '{:03} {}.jpg'.format(imgNum, architectName)
    return fileName

# Returns the webpage source code under page_doc
result = requests.get(page)
page_doc = result.content

# Returns the source code as BeautifulSoup object, as nested data structure
soup = BeautifulSoup(page_doc, 'html.parser')
# Returns footer thumbnail url
img = soup.find('div', class_='extra-lightbox-images')

# Main article images
article = soup.find('section', class_='main-article-body')
s = article.find_all('img', {'srcset' : True })

for url in s:
    urlm = url['srcset']
    urlm_s = urlm.split(', ')
    urlms_f = [a for a in urlm_s if '2364w' in a]
    url_final = [i.split(' ', 1)[0] for i in urlms_f]
    try:
        imgUrl = url_final[0]
    except IndexError:
        continue
    filename = fileName(url)
    # Open the url image, set stream to True, this will return the stream content
    r = requests.get(imgUrl, stream = True)
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero
        r.raw.decode_content = True
        # Open a local file with wb (write binary) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image successfully downloaded: ', filename)
    else:
        print('Image couldn\'t be retrieved')
    imgNum += 1

# For footer thumbnail images
for url in img:
    imgUrl = url['data-lightboximage']
    filename = fileName(url)
    # Open the url image, set stream to True, this will return the stream content
    r = requests.get(imgUrl, stream = True)
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero
        r.raw.decode_content = True
        # Open a local file with wb (write binary) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image successfully downloaded: ', filename)
    else:
        print('Image couldn\'t be retrieved')
    imgNum += 1
