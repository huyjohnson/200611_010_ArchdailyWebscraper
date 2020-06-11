#### - Webscraping version 1.0 -
#### - Archdaily - 

import requests
import json
import shutil
from bs4 import BeautifulSoup

# Enter the URL of the webpage you want to download the images from
page = 'https://www.archdaily.com/104724/ad-classics-maison-bordeaux-oma/5037fb3c28ba0d599b000773-ad-classics-maison-bordeaux-oma-photo'
imgNum = 1
architectName = 'OMA Bordeaux'

def imgUrl(url_x):
    imgUrl = url_x.split('?')[0]
    return imgUrl

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
img = soup.find('div', class_='afd-gal-items')
img_data = img.attrs['data-images']

# Downloads images and renames
for img_prop in json.loads(img_data): # Turn into dictionary
    url = img_prop['url_large']    
    filename = fileName(url)
    # Open the url image, set stream to True, this will return the stream content
    r = requests.get(imgUrl(url), stream = True)
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

