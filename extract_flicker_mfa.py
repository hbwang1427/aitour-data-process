#!/usr/bin/python

import urllib
import urllib2
from bs4 import BeautifulSoup
import os, sys
import json
import re

HIGHLIGHTS = ['painting']

def extract_highlight_content(soup):
    contents = []
    items = soup.find_all('div', class_='view photo-list-photo-view awake')
    img_urls = []
    for item in items:
        urls = [p.split(':')[1] for p in item['style'].split(';') if p.split(':')[0].find('background-image')>=0]
        img_urls.extend([ u.split('"')[1].replace('//', '') for u in urls])
    return img_urls

def write_(contents, output_dir):
    for content in contents:
        img_url = content['img_url']
        img = img_url.rsplit('/',1)[-1]
        img_fname = os.path.join(output_dir, 'Images', img)
        print 'saving %s' % (img_url)
        urllib.urlretrieve(img_url, img_fname)
        content_fname = os.path.join(output_dir, 'Descriptions', img.split('.')[0] + '.json')
        with open(content_fname, 'w') as fid:
            json.dump(content, fid, indent=2, separators=(',',':'), sort_keys=False)

if __name__ == '__main__':
    FLICKER_URL = 'https://www.flickr.com/search/?text=mfa%20boston%20'
    IMG_DIR='/home/pangolins/work/data/Images/museum/FineArts-flicker'

    for highlight in HIGHLIGHTS:
        url = '%s&view_all=1' % (FLICKER_URL)
        url = 'flicker_mfa.htm'
#        response = urllib2.urlopen(url)
#        html_doc = response.read()
        #soup = BeautifulSoup(html_doc, 'html.parser')
        soup = BeautifulSoup(open(url), 'html.parser')
        img_urls = extract_highlight_content(soup)
        print 'total images : %d' % len(img_urls)
        for url in img_urls:
            img = url.rsplit('/',1)[-1]
            img_fname = os.path.join(IMG_DIR, img)
            print 'saving %s' % (img)
            urllib.urlretrieve('http://'+url, img_fname)
        #print img_urls
