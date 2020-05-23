#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
from colorama import Fore, Style

try:
    user_county = sys.argv[1]
except:
    print(Fore.RED+"I need the county name"+ Style.RESET_ALL)


CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

def get_code(county):
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)  
    driver.get('https://cidades.ibge.gov.br/brasil/sp/{}/panorama'.format(county.lower()))
    word = driver.find_elements_by_xpath('//div[@class="topo__valor"]')
    print(word)
    driver.close()

get_code(user_county)