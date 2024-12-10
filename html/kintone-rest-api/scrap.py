
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

links=[]

def start_scraping(chrome_options):
    driver = webdriver.Chrome(
        options=chrome_options,
    )
    driver.get("https://cybozu.dev/ja/kintone/docs/rest-api/")
    sleep(5)
    root=driver.find_element(By.CSS_SELECTOR, "li.main--content--navigation--list--item.local-navigation-toggle.open")
    parent_elements=root.find_elements(By.CSS_SELECTOR,"li a")
    for parent_element in parent_elements:
        link=parent_element.get_attribute("href")
        links.append(link)
        print("-------->",link)

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--force-dark-mode")
chrome_options.add_argument("--start-maximized")

try:
    start_scraping(chrome_options)
    print(links)
    print(len(links))
    with open('sublinks.json', 'w') as file:
        json.dump(links, file)
    print("Links have been written to links.json")

except Exception as e:
        print(e)
