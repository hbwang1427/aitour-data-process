import json
import numpy as np
import csv
import os

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import pyautogui
import random
import time
import shutil

def download_url(driver, url, tag_name='img'):
    print (url)
    driver.get(url)
    elem = driver.find_element_by_tag_name(tag_name)
#    print (elem)
    if elem is not None:
        actionChain = ActionChains(driver)
        # prompt to download
        actionChain.context_click(elem).perform()
        if tag_name == 'img':
            pyautogui.typewrite(['down','down', '1', '2', 'enter'])
        else:
            pyautogui.typewrite(['down','down', 'down', 'down', 'enter'])

        handles = driver.window_handles
        # switch to the popup window
        driver.switch_to_window(handles.pop())
        pyautogui.press('enter')
        time.sleep(random.randint(3,5))

def download_art_image(driver, data, output_dir):
    if 'image_url' not in data or data['image_url'] is None:
        print (data['art_url'])
        return
    url = data['image_url']
    filename = os.path.join(output_dir, url.split('/')[-1])
    if not os.path.isfile(filename):
         print (url)
         download_url(driver, url, 'img')

def download_art_audio(driver, data, output_dir):
    if 'art_info' not in data or data['art_info'] is None:
        return
   
    art_info = data['art_info']
    for language, info in art_info.items():
        if 'audio' in info and info['audio']:
            for url in info['audio']:
                filename = os.path.join(output_dir, url.split('/')[-1])
                if os.path.isfile(filename):
                    continue
                print (url)
#                download_url(driver, url, 'source')

if __name__ == '__main__':
    base_art_url = 'http://www.metmuseum.org'
    #base_output_dir = '/home/pangolins/Ddrive/data/museum/MET-multilingual/highlights'
    base_output_dir = '/home/pangolins/Ddrive/data/museum/MET-multilingual-missing/highlights'
    #tmp_output_dir = '/home/pangolins/Downloads'
    #tmp_output_dir = '/home/pangolins/Ddrive/data/museum/MET-multilingual/images'
    tmp_output_dir = '/home/pangolins/Ddrive/data/museum/MET-multilingual-missing/images'
    
    #display = Display(visible=0, size=(800, 800))  
    #display.start()
    

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=other")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    #reader = csv.reader(open("MetObjects.csv", "rt"), delimiter=",")
    reader = csv.reader(open("MetObjects-missing.csv", "rt"), delimiter=",")
    cnt = 0
    for row in reader:
        cnt = cnt + 1
        #if row[1] == 'False' or cnt == 1:
        #    continue
 
        #art_url = row[-3]
        art_url = row[0]
        #print (cnt, art_url)

        art_id = int(art_url.split('/')[-1])
        output_dir = os.path.join(base_output_dir, str(art_id))
        json_file = os.path.join(output_dir, '%d.json' % (art_id))
        data = json.load(open(json_file, 'r'))
        #download_art_audio(driver, data, tmp_output_dir)        
        download_art_image(driver, data, tmp_output_dir)        
        
        files = os.listdir('/home/pangolins/Downloads')
        for f in files:
            print (f)
            shutil.move(os.path.join('/home/pangolins/Downloads/',f), os.path.join(output_dir,f))
        time.sleep(random.randint(8,10))
    #    break
    driver.close()
