from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import urllib.request
import time
from pyvirtualdisplay import Display
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import numpy as np
import csv
import os
import random
import time

def scrape_art_page(driver, art_url):
    soup = None
    try:	
        driver.get(art_url)
        soup=BeautifulSoup(driver.page_source, 'lxml')
    except Exception as e:
        print (str(e))
        pass

    return soup

def soup_find_class(soup, tag, class_name):
    return soup.find_all(tag, class_=class_name)

def soup_find_next(soup, tag, class_name=None):
     return soup.findNext(tag, class_=class_name) if class_name  \
         else soup.findNext(tag)

'''
def get_art_image_url(soup):
    items = soup_find_class(soup, 'div', 'met-carousel__item is-active')
    if items:
        ng = soup_find_next(items[0], 'img')
        if ng:
            return ng['data-superjumboimage']

    return None
'''

def get_art_image_url(soup):
    items = soup_find_class(soup, 'li', 'utility-menu__item utility-menu__item--download')
    if items:
        ng = soup_find_next(items[0], 'a')
        if ng:
            return ng['href']

    items = soup_find_class(soup, 'div', 'artwork__image__wrapper')
    if items:
        ng = soup_find_next(items[0], 'img')
        if ng:
            return ng['src']

    return None

def get_art_title(soup):
    items = soup_find_class(soup, 'h1', 'artwork__object-title')
    return items[0].text if items else None

def get_art_items(art_info):
    items = soup_find_class(art_info, 'p', 'artwork__tombstone--row')
    results = []
    for item in items:
        next_label = soup_find_next(item, 'span', 'artwork__tombstone--label')
        if next_label:
            next_label = next_label.text
        next_value = soup_find_next(item, 'span', 'artwork__tombstone--value')
        if next_value:
            next_value = next_value.text
        results.append((next_label, next_value))

    return results

def get_art_description(art_info):
    next_item = soup_find_next(art_info, 'div', 'artwork__label')
    if next_item:
        return next_item.text

    next_item = soup_find_next(art_info, 'div', 'artwork__intro__label')
    if next_item:
        return next_item.text
    
    return None

def get_art_description_1(soup):
    items = soup_find_class(soup, 'div', 'artwork__intro__desc')
    if items:
        ng = soup_find_next(items[0], 'p')
        if ng:
            return ng.text
    return None


def get_art_audios(art_audio):
    items = soup_find_class(art_audio, 'div', 'met-carousel__item artwork-audio-item')
    audio_list = []
    if items:
        for item in items:
             next_item = soup_find_next(item, 'source')
             if next_item:
                 audio_list.append(next_item['src'])
    return audio_list

def extract_art_content(soup):
    data = {}

    title = get_art_title(soup)
    if title:
        data['title'] = title

    art_info = soup_find_class(soup, 'section', 'artwork-info')
    if art_info:
        art_info = art_info[0]
        art_items = get_art_items(art_info)
        if art_items:
            info = {}
            for k, item in enumerate(art_items):
                info[str(k+1)] = {'label':item[0], 'value':item[1]}
            data['info'] = info

        # description
        description = get_art_description(art_info)
        if not description:
            description = get_art_description_1(soup)

        data['description'] = description
    
    art_audio = soup_find_class(soup, 'section', 'artwork-audio')
    if art_audio:
        art_audio = art_audio[0]
        art_audio = get_art_audios(art_audio)
        data['audio'] = art_audio

    return data

def get_language_list(soup):
    optionsList = []
    translations = soup_find_class(soup, 'select', 'translations__select')
    if translations:
        for option in translations[0].find_all('option'):
            x = option['value'].split('/')
            x = x[1] if len(x) == 6 else 'en'
            optionsList.append(x)

    return optionsList

def get_display_location(soup):
    gallery_location = soup_find_class(soup, 'span', 'artwork__location--gallery')
    if gallery_location:
        gallery = soup_find_next(gallery_location[0], 'a')
        if gallery:
            gallery_text = gallery.text
            return gallery_text

    return None

def scrape(driver, base_art_url, art_id):
#    url = 'https://www.metmuseum.org/art/collection/search/736275'
    art_url_en = '%s/art/collection/search/%d' %  (base_art_url, art_id)
    soup = scrape_art_page(driver, art_url_en)
    if soup is None:
        return {}

    data = {}
    data['art_info'] = {}
    data['art_url'] = art_url_en
    data['image_url'] = get_art_image_url(soup)
    data['display_location'] = get_display_location(soup)
    data['art_info']['en'] = extract_art_content(soup)

    language_list = get_language_list(soup)
    #print (language_list)
    if language_list:
        for item in language_list:
            if item == 'en': 
                continue

            url = '%s/%s/art/collection/search/%d' %  (base_art_url, item, art_id)
            #print (url)
            soup = scrape_art_page(driver, url)
            if not soup:
                continue
            data['art_info'][item] = extract_art_content(soup)
        
    return data

def load_urls_from_file(filename):
    reader = csv.reader(open("MetObjects.csv", "rt"), delimiter=",")
    x = list(reader)
    data = np.array(x).astype(str)
    I = np.where(data[:,1] == 'True')
    return data[I,-3]

def download_url(output_dir, url):
    print (url)
    filename = url.split('/')[-1]
    target_filename = os.path.join(output_dir, filename)
    try:
        urllib.request.urlretrieve(url, target_filename)
    except Exception as e:
        print(str(e))

def save_data(base_output_dir, art_id, art_data):
    output_dir = os.path.join(base_output_dir, str(art_id))
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    json_file = os.path.join(output_dir, '%d.json'%art_id)
    with open(json_file, 'w') as fid:
        json.dump(art_data, fid, indent=2, separators=(',',':'), sort_keys=False)

    '''
    if 'image_url' in art_data and art_data['image_url'] is not None:
        download_url(output_dir, art_data['image_url'])
        driver.implicitly_wait(random.randint(1,2))
    
    if 'art_info' in art_data:
        for key, value in art_data['art_info'].items():
            if 'audio' not in value or value['audio'] is None:
                continue
            for item in value['audio']:
                download_url(output_dir, item)
                driver.implicitly_wait(random.randint(1,2))
    '''   

if __name__ == '__main__':
    base_art_url = 'http://www.metmuseum.org'
    #base_output_dir = '/home/pangolins/Ddrive/data/museum/MET-multilingual/regular'
    base_output_dir = '/home/pangolins/Ddrive/data/museum/MET-multilingual-missing/regular'

    random.seed()

    display = Display(visible=0, size=(800, 800))  
    display.start()
    driver = webdriver.Chrome()

    #reader = csv.reader(open("MetObjects.csv", "rt"), delimiter=",")
    reader = csv.reader(open("MetObjects-missing.csv", "rt"), delimiter=",")
    cnt = 0
    for row in reader:
        cnt = cnt + 1
     #   if row[1] == 'True' or cnt == 1:
     #       continue
 
        #art_url = row[-3]
        art_url = row[0]
        print (cnt, art_url)

        art_id = int(art_url.split('/')[-1])
        art_data = scrape(driver, base_art_url, art_id) 
        if art_data:
            save_data(base_output_dir, art_id, art_data)
        #break
        time.sleep(random.randint(3,5))
    driver.close()
