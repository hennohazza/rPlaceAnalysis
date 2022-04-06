'''
Script to download r/place images.
https://rplace.space/combined/
This website has a handy archive of the r/place canvas at 30 second intervals.
Seems to be missing the start unfortunately. Hopefully it appears.

Required packages ; BeautifulSoup
'''

# import packages
import requests, os, sys
from bs4 import BeautifulSoup


url = 'https://rplace.space/combined/'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

# extracts all links on the page (in this case all the images + '../')
# download_dir is location of images. 
download_dir = 'Ims/'
for i, link in enumerate(soup.find_all('a')):
    # first link is '../' so skip this
    if i==0:
        pass
    else:
        # found this process times out, so skip the ones downloaded!
        if not os.path.exists(download_dir+link.get('href')):
            print('retrieving image ', link.get('href'))

            img_data = requests.get(url+link.get('href')).content
            with open(download_dir+link.get('href'), 'wb') as handler:
                handler.write(img_data)
