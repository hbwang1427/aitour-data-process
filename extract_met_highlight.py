import urllib
import urllib2
from bs4 import BeautifulSoup
import os, sys
import json
import validators
#from urllib.request import urlopen
from fake_useragent import UserAgent

def extract_content(base_output_dir, base_url, doc):
    items = doc['results']
    for item in items:
#        print item
#        print item['image']
        item_url = base_url + '/' + item['url']
        content = get_content_detail(item_url)

        # this one has better quality?       
        if not content['img'] and validators.url(item['image']):
            content['img'] = item['image']
        print (item_url)
        print (content, '\n')

        #special handling
        sub_dir = content['class']
        sub_dir = sub_dir.replace('/', '_')
        if not sub_dir: sub_dir = 'Others'
        output_dir = os.path.join(base_output_dir, sub_dir)
        save_content(output_dir, content)
        

def get_content_detail(url):
    response = urllib2.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    content = {'img':'',
               'title':'',
               'artist':'',
               'class':'',
               'date':'',
               'medium':'',
               'description':'',
               'audio':'',
               'location':'',
               'department':''}
    content_list = {'Classification:':'class', 'Author:':'artist', 'Maker:':'artist', 'Artist:':'artist', 'Date:':'date', 'Medium:':'medium'}

    # img
    items = soup.find_all('a', {'name':'#collectionImage'})
    if items:
        ng = items[0].findNext('img')
        if ng:
           s = ng['ng-src']
           content['img'] = s[s.find("(")+1:s.find(")")].strip('\'')
        #content['img'] = items[0]['content']

    # title
    items = soup.find_all('h1', class_='collection-details__object-title right-to-left')
    content['title'] = items[0].text

    # classification
    items = soup.find_all('dt', class_="collection-details__tombstone--label float-right")
    for item in items:
        if item.text in content_list.keys():
         #   print item.text
            val = item.findNext('dd', class_="collection-details__tombstone--value")
            content[content_list[item.text]] = val.text


    # description   
    items = soup.find_all('div', class_="collection-details__label right-to-left")
    if items:
        content['description'] = items[0].text

    # location
    items = soup.find_all('div', class_="collection-details__location")
    if items:
        alink = items[0].findNext('a')
        if alink: content['location'] = alink.text

    # department
    items = soup.find_all('label', class_="collection_details__facets--department-label")
    if items:
       alink = items[0].findNext('a')
       if alink: content['department'] = alink.text.split('(')[0]

    # audio
    items = soup.find_all('div', class_="collection-audio-item__player")
    if items:
      audio = items[0].findNext('source')
      content['audio'] = audio['src']

    return content

def save_content(output_dir, content):
    img_url = content['img']
    img_name = img_url.rsplit('/',1)[-1]
    img_base_name = img_name.split('.')[0]
    final_output_dir = os.path.join(output_dir, img_base_name)
    print ('Output dir: %s' % (final_output_dir))
    if not os.path.isdir(final_output_dir):
        os.makedirs(final_output_dir)

    #image
    img_fname = os.path.join(final_output_dir, img_name)
    if not os.path.isfile(img_fname):
        print ('saving %s' % (img_url))
        urllib.urlretrieve(img_url, img_fname)
    
    audio_url = content['audio']
    if audio_url:
        audio_fname = os.path.join(final_output_dir, audio_url.rsplit('/',1)[-1])
        if not os.path.isfile(audio_fname):
            print ('saving %s' % (audio_url))
            urllib.urlretrieve(audio_url, audio_fname)

    #description
    content_fname = os.path.join(final_output_dir, img_base_name + '.json')
    if not os.path.isfile(content_fname):
        with open(content_fname, 'w') as fid:
            json.dump(content, fid, indent=2, separators=(',',':'), sort_keys=False)


if __name__ == '__main__':
     MET_OUTPUT_DIR = '/home/pangolins/work/data/Museum/MET_test'
     #MET_URL_TEMPLATE='https://www.metmuseum.org/api/collection/collectionlisting?artist=&department=&era=&geolocation=&material=&offset=%d'
     #SUFFIX = '&pageSize=0&perPage=20&showOnly=highlights\%7CwithImage&sortBy=Relevance&sortOrder=asc'
     MET_URL_TEMPLATE='https://www.metmuseum.org/api/collection/collectionlisting?department=11&perPage=20&sortBy=Relevance&sortOrder=asc&offset=%d&pageSize=0'
     SUFFIX=''

     ua = UserAgent()
     #for offset in range(0,4000,20):
     for offset in range(0,1,20):
        url = MET_URL_TEMPLATE % (offset) + SUFFIX
        url = 'https://www.metmuseum.org/art/collection/search#!#perPage=20&searchField=All&sortBy=relevance&offset=20&pageSize=0&department=11'
        #url = 'https://www.metmuseum.org/zh/art/collection/search/436244'
        print (url)
        try:
            header = {'User-Agent':str(ua.chrome)}
            req = urllib2.Request(url, None, header)
            #response = urllib2.urlopen(url, header=header)
            response = urllib2.urlopen(req)
            print (response)
            html_doc = response.read()
            print (html_doc)
        except urllib2.URLError as e:
            print e.reason 

        result = json.loads(html_doc)
        extract_content(MET_OUTPUT_DIR, 'https://www.metmuseum.org', result)
