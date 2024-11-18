import os, sys, random, time, urllib2
from cookielib import CookieJar
import json
import validators
from bs4 import BeautifulSoup
import urllib
import urllib2
from fake_useragent import UserAgent

'''
def extract_content(base_output_dir, url, doc):
    content = get_content(url)
    sub_dir = content['class']
    sub_dir = sub_dir.replace('/', '_')
    if not sub_dir: 
        sub_dir = 'Others'
    output_dir = os.path.join(base_output_dir, sub_dir)
    save_content(output_dir, content)
'''

def get_content(url):
    content = None
    try:
        response = urllib2.urlopen(url)
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        content = get_content_detail(soup)
    except urllib2.URLError as e:
	print (e.reason)

    return content

def get_content_item(node):
    item = node.findNext('span')
    return item.text if item is not None else ''

def get_artist(node):
    item = node.findNext('a')
    if item is None:
        return ''
    return item.text
    
def get_description(doc):
    desc = ''
    item = doc.find('div', class_="o-article__body o-blocks")
    if item:
       item = item.findNext('p')
       if item:
           desc = item.text
    return desc
        
def get_additional_info(doc):
    classification, location, ondisplay = '', '', ''
    node = doc.find('div', class_="o-article__primary-actions o-article__primary-actions--inline-header u-show@large+")
    if not node:
        return classification, location, ondisplay
    
    item  = node.find('h2', class_="title f-module-title-1 u-show@large+")
    if item:
        ondisplay = item.text

    item  = node.findNext('a')
    if item:
        classification = item.text
        item = item.findNext('a')
        if item:
            location = item.text
  
    return classification, location, ondisplay


def get_content_detail(doc):
    content = {'img':'',
               'title':'',
               'artist':'',
               'class':'',
               'date':'',
               'origin':'',
               'medium':'',
               'description':'',
               'audio':'',
               'ondisplay':'',
               'location':'',
               'department':''}
    content_list = {'Origin':'origin', 'Artist':'artist', 'Maker':'artist', 'Artist':'artist', 'Date':'date', 'Medium':'medium', 'Title':'title'}

    # img
    item = doc.find('div', class_="m-article-header__img-container")
    if item:
        ng = item.findNext('img')
        if ng:
           s = ng['srcset']
           content['img'] = s.split(' ')[2]


    items = doc.find_all('h2',  class_="f-module-title-1")
    for item in items:
        if item.text in content_list:
           key = content_list[item.text]
           if item.text == 'Artist':
               content[key] = get_artist(item)
           else:
               content[key] = get_content_item(item) 
   
    classification, location, ondisplay = get_additional_info(doc)
    content['ondisplay'] = ondisplay
    content['class'] = classification
    content['location'] = location
    content['description'] = get_description(doc)
    # classification

    # audio
    items = doc.find_all('audio', class_="video-js vjs-fluid m-vjs-audio")
    if items:
      audio = items[0].findNext('source')
      content['audio'] = audio['src']

    print (content)
    return content

def save_content(output_dir, cnt, content):
    final_output_dir = os.path.join(output_dir, '%05d' % (cnt))
    print ('Output dir: %s' % (final_output_dir))
    if not os.path.isdir(final_output_dir):
        os.makedirs(final_output_dir)

    #image
    img_url = content['img']
    img_name = img_url.rsplit('/',1)[-1]
    img_fname = os.path.join(final_output_dir, img_name)
    if not os.path.isfile(img_fname):
        print ('saving %s' % (img_url))
        try:
            urllib.urlretrieve(img_url, img_fname)
        except:
            print ('failed to save %s' % (img_url))  
        #response = urllib2.urlopen(img_url)
        #f = open(img_fname)
        #f.write(response.read())
        #f.close()
    
    time.sleep(random.randint(1, 2))
    audio_url = content['audio']
    if audio_url:
        #audio_fname = os.path.join(final_output_dir, audio_url.rsplit('/',1)[-1])
        audio_fname = os.path.join(final_output_dir, '%05d.mp3' % (cnt))
        if not os.path.isfile(audio_fname):
            print ('saving %s' % (audio_url))
            try:
                urllib.urlretrieve(audio_url, audio_fname)
            except:
                print ('failed to save %s' % (audio_url))  
            #response = urllib2.urlopen(audio_url)
            #f = open(audio_fname)
            #f.write(response.read())
            #f.close()
    
    time.sleep(random.randint(1, 2))
    #description
    content_fname = os.path.join(final_output_dir, '%05d.json' % (cnt))
    if not os.path.isfile(content_fname):
        try:
            with open(content_fname, 'w') as fid:
                json.dump(content, fid, indent=2, separators=(',',':'), sort_keys=False)
        except:
            print ('failed to save %s' % (content_fname))  

def get_art_urls(url):
    response = urllib2.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    collection_list = soup.find_all('div', class_='o-collection-listing__col-right')[0]
    items = collection_list.find_all('li', class_="m-listing m-listing--variable-height o-pinboard__item")
    if not items:
        return {}

    collections=[]
    for item in items:
       a_link=item.find('a', class_="m-listing__link")
       assert (a_link)
       #print (a_link['href'])
       # break
       collections.append(a_link['href'])

    return collections

def get_art_collection_list(url):
    response = urllib2.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    #items = soup.find_all('ul', class_='m-quick-search-links__links')[0]
    items = soup.find_all('a', class_="tag f-tag tag--senary tag--w-image")
    collections={}
    for item in items:
       collections[item['data-gtm-event']] = item['href']

    return collections

if __name__ == '__main__':
     ARTIC_OUTPUT_DIR = '/media/pangolins/Disc2/artic'
     ARTIC_URL = 'https://www.artic.edu/collection'
     ARTIC_URL_TEMPLATE='https://www.artic.edu/collection?style_ids=Impressionism&page=%d'

     SUFFIX=''

     random.seed()
     #setup global url opener(includes a cookie jar and set user-agent http header)
     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar()), urllib2.HTTPRedirectHandler())
     opener.addheaders = [('User-Agent', str(UserAgent().chrome))]
     #opener.addheaders = [('User-Agent', 'googlebot')]
     urllib2.install_opener(opener)
     
     art_collections = get_art_collection_list(ARTIC_URL)
     print (art_collections.keys())
     
     for collection, base_url in art_collections.items():
         #if collection == 'fashion': continue
         output_dir = os.path.join(ARTIC_OUTPUT_DIR, collection)
         if os.path.isdir(output_dir):
             continue
         cnt = 1
         for offset in range(2000):
             page_url = '%s&page=%d' % (base_url, offset)
             print (page_url)
             art_urls = get_art_urls(page_url)
             if not art_urls:
                 break

             for url in art_urls:
                 print (url)
                 if not os.path.isdir(os.path.join(output_dir, '%05d' % (cnt))):
                     content = get_content(url)
                     save_content(output_dir, cnt, content)
                 print (cnt)
                 cnt = cnt + 1
             #break
             time.sleep(random.randint(10,15))
             #if content is None:
             #    break
         #break
    
        #sleep for random seconds in range [1, 5]
