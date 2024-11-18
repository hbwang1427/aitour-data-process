import urllib
import urllib2
from bs4 import BeautifulSoup
import os, sys
import json

HIGHLIGHTS = ['european-paintings', \
              'british-paintings', \
              'italian-paintings', \
              'spanish-paintings', \
              'white-fund-paintings', \
              'claude-monet', \
              'italian-renaissance-art', \
              'vincent-van-gogh', \
              'french-paintings', \
              'northern-european-paintings', \
              'rembrandt']

def extract_highlight_content(soup):
    contents = []
    items = soup.find_all('div', class_='grid-8')
    for item in items:
        data = {}
        zoom = item.findNext('div', class_='zoom')
        data['img_url'] = zoom.find('img')['src']
        slide_content = item.parent.findNext('div', class_='grid-4')
        data['slide_title'] = slide_content.findNext('div', class_='slide-title').findNext('h2').text
        slide_desc = slide_content.findNext('div', class_='accordion details').findNext('div', class_='slide-description')
        provenance = slide_desc.findNext('h4')
        desc = provenance.find_previous_sibling('p')
        data['slide_desc'] = desc.text if desc is not None else ''
        data['desc_url'] = 'www.mfa.org' + slide_content.findNext(text='More Info').parent['href']
        print data['img_url']
        print data['slide_title']
        print data['slide_desc']
        print data['desc_url']
        contents.append(data)

    return contents

def write_highlight_contents(contents, output_dir):
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
    MFA_URL = 'http://www.mfa.org/collections/europe/tour'
    IMG_DIR='/home/pangolins/work/data/Images/museum/FineArts-highlights_test'

    for highlight in HIGHLIGHTS[2:]:
        url = os.path.join(MFA_URL, highlight)
        response = urllib2.urlopen(url)
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        contents = extract_highlight_content(soup)
#        print contents           


        output_dir = os.path.join(IMG_DIR, highlight)
        print output_dir
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.makedirs(output_dir + '/Images')
            os.makedirs(output_dir + '/Descriptions')

        write_highlight_contents(contents, output_dir)
#        for item in img_urls:
#            output_fname = os.path.join(output_dir, item.rsplit('/',1)[-1])
#            print output_fname
#            urllib.urlretrieve(item, output_fname)
