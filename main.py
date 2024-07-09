from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from copiwinsdk import CopiwinSDK
from dotenv import load_dotenv
import os

load_dotenv()

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
copiwinSDK = CopiwinSDK(client_id=os.environ.get("COPIWIN_CLIENT_ID"),client_secret=os.environ.get("COPIWIN_CLIENT_SECRET"))

while True:
  pass
