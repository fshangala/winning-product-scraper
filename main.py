from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from copiwinsdk import CopiwinSDK
from dotenv import load_dotenv
import os
import winninghunter
import logging

load_dotenv()

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

def getTrackedSiteData(sites:list,store:dict)->dict:
  name = store["hostname"].split(".")[1] if store["hostname"].split(".")[0] == "www" else store["hostname"].split(".")[0]
  filteredSites=filter(lambda x: name in x["store"],sites)
  filteredSites=list(filteredSites)
  if len(filteredSites) == 1:
    return filteredSites[0]
  else:
    return None

if __name__ == "__main__":
  logger = logging.getLogger(__name__)
  logging.basicConfig(filename='scraper.log', encoding='utf-8', level=logging.DEBUG)
  driver = webdriver.Chrome(options=options)
  copiwinSDK = CopiwinSDK(client_id=os.environ.get("COPIWIN_CLIENT_ID"),client_secret=os.environ.get("COPIWIN_CLIENT_SECRET"))
  while True:
    stores=copiwinSDK.getStores()
    if stores:
      sites=winninghunter.getTrackedSites(driver=driver)
      if sites:
        for store in stores:
          data=getTrackedSiteData(sites=sites,store=store)
          if not data:
            sites=winninghunter.addTrackedSite(driver=driver,url=store["url"])
            data=getTrackedSiteData(sites=sites,store=store)
          if data:
            response=copiwinSDK.addStoreData(store_id=store["id"],data=data)
            print(response)         
