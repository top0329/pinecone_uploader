
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
    driver.get("https://jp.cybozu.help/k/ja/user.html")
    sleep(5)
    count=0
    root=driver.find_element(By.CSS_SELECTOR, "li[id=\'j1_18\']")
    parent_elements=root.find_element(By.TAG_NAME,"ul").find_elements(By.TAG_NAME,"li")
    for parent_element in parent_elements:
        try:
            count+=1
            parent_element.find_element(By.TAG_NAME,"i").click()

            sleep(2)
            links_elements=parent_element.find_element(By.TAG_NAME,"ul").find_elements(By.TAG_NAME,"li")

            for link_element in links_elements:
                try:
                  link_element.find_element(By.TAG_NAME,"i").click()
                  sleep(2)
                  sublink_elements=link_element.find_element(By.TAG_NAME,"ul").find_elements(By.TAG_NAME,"li")
                  for sublink_element in sublink_elements:
                      link=sublink_element.find_element(By.TAG_NAME,"a").get_attribute("href")
                      links.append(link)
                      print("-------->",link)
                  link_element.find_element(By.TAG_NAME,"i").click()
                  sleep(2)
                except Exception as e:
                  link=link_element.find_element(By.TAG_NAME,"a").get_attribute("href")
                  links.append(link)
                  print("-------->",link)
                  link_element.find_element(By.TAG_NAME,"i").click()
                  sleep(2)

            parent_element.find_element(By.TAG_NAME,"i").click()
            sleep(2)
            print(f"Successfully get in {count} element")

        except Exception as e:
            parent_element.find_element(By.TAG_NAME,"i").click()
            sleep(2)
            print(f"Error in {count} element")

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
