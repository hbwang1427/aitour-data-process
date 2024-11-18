import urllib
import urllib2
from bs4 import BeautifulSoup
import os, sys
import json
import validators

def extract_content(base_output_dir, base_url, url):
    response = urllib2.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('div', class_='field-item even')
    for item in items:
       print '------'
       a_src = item.findNext('img')
       a_link = item.findNext('a')
       if a_src is not None and a_link is not None:
           print a_link['href']
           content = get_content_detail(base_url + a_link['href'])
           print content
           if content['artist']:
               sub_dir = content['class']
               output_dir = os.path.join(base_output_dir, sub_dir)
               content['img'] = base_url + content['img']
               save_content(output_dir, content)

def get_content_detail(url):
    # img
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
    response = urllib2.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    # title
    items = soup.find_all('h1', class_='page-title')
    content['title'] = items[0].text

    # class
    items = soup.find_all('div', class_='field field-name-field-medium')
    if items:
       a_link = items[0].findNext('a')
       if a_link: content['class'] = a_link.text
    
    items = soup.find_all('div', class_='field field-name-field-materials')
    if items:
      content['medium'] = items[0].text[9:]

    # artist  
    items = soup.find_all('span', class_="odd artist first last")
    if items:
       alink = items[0].findNext('a')
       if alink: 
           content['artist'] = alink.text
       next_item = items[0].findNext('div', class_='field-item even')
       if next_item: content['date'] = next_item.text
    
    # image  
    items = soup.find_all('div', class_="img-container")
    if items:
       a_src = items[0].findNext('img')
       if a_src: content['img'] = a_src['src'].split('?')[0]

    items = soup.find_all('div', class_="ds-1col node node-artwork node-sticky view-mode-full clearfix")
    if items:
       next_item = items[0].findNext('p')
       if next_item: content['description'] = next_item.text

    return content

def save_content(output_dir, content):
    img_url = content['img']
    img_name = img_url.rsplit('/',1)[-1]
    img_base_name = img_name.split('.')[0]
    final_output_dir = os.path.join(output_dir, img_base_name)
    print 'Output dir: %s' % (final_output_dir)
    if not os.path.isdir(final_output_dir):
        os.makedirs(final_output_dir)

    #image
    img_fname = os.path.join(final_output_dir, img_name)
    if not os.path.isfile(img_fname):
        print 'saving %s' % (img_url)
        urllib.urlretrieve(img_url, img_fname)
    
    audio_url = content['audio']
    if audio_url:
        audio_fname = os.path.join(final_output_dir, audio_url.rsplit('/',1)[-1])
        if not os.path.isfile(audio_fname):
            print 'saving %s' % (audio_url)
            urllib.urlretrieve(audio_url, audio_fname)

    #description
    content_fname = os.path.join(final_output_dir, img_base_name + '.json')
    if not os.path.isfile(content_fname):
        with open(content_fname, 'w') as fid:
            json.dump(content, fid, indent=2, separators=(',',':'), sort_keys=False)


if __name__ == '__main__':
     ICA_OUTPUT_DIR = '/home/pangolins/work/data/Museum/ICA_Boston'
     ICA_URL_TEMPLATE='https://www.icaboston.org/collection?page=%d'

     for offset in range(0,13):
        url = ICA_URL_TEMPLATE % (offset)
        print url
        extract_content(ICA_OUTPUT_DIR, 'https://www.icaboston.org', url)
