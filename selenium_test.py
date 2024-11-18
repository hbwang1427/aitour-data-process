from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import urllib.request
import time
from pyvirtualdisplay import Display
import json
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

def soup_find_class(soup, tag, class_name):
    return soup.find_all(tag, class_=class_name)

def soup_find_next(soup, tag, class_name=None):
     return soup.findNext(tag, class_=class_name) if class_name  \
         else soup.findNext(tag)

def get_art_image_link(soup):
    items = soup_find_class(soup, 'div', 'met-carousel__item is-active')
    if items:
        ng = soup_find_next(items[0], 'img')
        if ng:
            return ng['data-superjumboimage']

    return None

def get_art_title(soup):
    items = soup_find_class(soup, 'h1', 'artwork_object-title')
    return items[0].text if items else None

def get_art_items(art_info):
    items = soup_find_class(art_info, 'p', 'artwork__tombstone--row')
    for item in items:
        next_label = soup_find_next(item, 'span', 'artwork__tombstone--label')
        if next_label:
            next_label = next_label.text
        next_value = soup_find_next(item, 'span', 'artwork__tombstone--value')
        if next_value:
            next_value = next_value.text
        print (next_label, next_value)

def get_art_description(art_info):
    next_item = soup_find_next(art_info, 'div', 'artwork__label')
    if next_item:
        return next_item.text
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
 
def get_content_detail(soup):
#    soup = BeautifulSoup(page_source, 'lxml')
#    print (soup)
    content = {'image':'',
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

    # image link
    image_link = get_art_image_link(soup)
    content['image'] = image_link if image_link is not None else ''
    print (image_link)
    filename = image_link.split('/')[-1]
    urllib.request.urlretrieve(image_link, filename)

    # title
    title = get_art_title(soup)
    content['title'] = title if title is not None else ''

    art_info = soup_find_class(soup, 'section', 'artwork-info')
    if art_info:
        art_info = art_info[0]
        get_art_items(art_info)
        description = get_art_description(art_info)
        print (description)
    
    art_audio = soup_find_class(soup, 'section', 'artwork-audio')
    if art_audio:
        art_audio = art_audio[0]
        art_audio = get_art_audios(art_audio)
        print (art_audio)

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

#with open('test.html', 'r') as f:
#    soup = BeautifulSoup(f, 'lxml')

#content = get_content_detail(soup)
#print (content)
#system.exit(0)

#display = Display(visible=0, size=(800, 800))  
#display.start()

driver = webdriver.Chrome()
#driver.get("http://www.python.org")
#url = 'https://www.metmuseum.org/art/collection/search/736275'
#url = 'https://www.metmuseum.org/art/collection/search/438817'
#url = 'https://www.metmuseum.org/zh/art/collection/search/436535'
url = 'https://images.metmuseum.org/CRDImages/ad/original/DT163.jpg'
driver.get(url)
#soup=BeautifulSoup(driver.page_source, 'lxml')
#content = get_content_detail(soup)
#print(content)
main_window_handle = driver.current_window_handle
#print (main_window_handle)
from selenium.webdriver import ActionChains
#elem = driver.find_element_by_css_selector("//a[@src='https://images.metmuseum.org/CRDImages/ad/original/DT3927.jpg']")
elem = driver.find_element_by_tag_name("img")
#print (elem)
actionChain = ActionChains(driver)
actionChain.context_click(elem).perform()
import pyautogui
pyautogui.typewrite(['down','down', 'enter', 'enter'])
'''
signin_window_handle = None
while not signin_window_handle:
    for handle in driver.window_handles:
        print (handle)
        if handle != main_window_handle:
            signin_window_handle = handle
            break
'''
handles = driver.window_handles
#driver.remove(main_window_handle)
driver.switch_to_window(handles.pop())

pyautogui.press('enter')
#driver.implicitly_wait(30)

#driver.close()
os.system.exit(0)
try:
    #elem = driver.find_element_by_class_name('translations__select')
    translations_select = driver.find_element_by_css_selector( "//select[@id='translations__select']")
    options = translations_select.find_elements_by_tag_name("option") #get all the options into a list
    print (options)
    optionsList = []

    for option in options: #iterate over the options, place attribute value in list
        optionsList.append(option.get_attribute("value"))

    for optionValue in optionsList:
        url = 'https://www.metmuseum.org%s' % optionValue
        print (url)
        driver.get(url) 
        print (driver.title)
#        print ("starting loop on option %s" % optionValue)
#        driver.implicitly_wait(30)
##        select = Select(driver.find_element_by_xpath( "//select[@id='transliations__select']"))
#        Select(translations_select).select_by_value(optionValue)
except Exception as e:
    print (str(e))
driver.close()
