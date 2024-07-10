from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import logging

logger = logging.getLogger(__name__)

class element_exists(object):
  def __init__(self,css_selector:str):
    self.css_selector=css_selector
  
  def __call__(self,driver):
    b = driver.execute_script(f'return document.querySelector("{self.css_selector}");')
    if b:
      return b
    else:
      return False
    
def login(driver:Chrome,attempt=1):
  email = driver.find_element(By.NAME, "Email")
  email.send_keys("malaky31@hotmail.fr")
  password = driver.find_element(By.NAME, "Password")
  password.send_keys("12345678")
  button = driver.find_element(By.CSS_SELECTOR, 'button.login')
  try:
    button.click()
  except ElementNotInteractableException as e:
    logger.error(e)
    print(f"Attempt: {attempt}; ")
    print(e)
    time.sleep(2)
    attempt += 1
    login(driver=driver,attempt=attempt)

def enterSiteUrl(driver:Chrome,url:str,attempt=1):
  email = driver.find_element(By.ID, "Store-URL")
  email.send_keys(url)
  startButton=driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
  try:
    startButton.click()
  except ElementNotInteractableException as e:
    logger.error(e)
    print(f"Attempt: {attempt}; ")
    print(e)
    time.sleep(2)
    attempt += 1
    enterSiteUrl(driver=driver,url=url,attempt=attempt)

def getTrackedSites(driver:Chrome):
  driver.get("https://app.winninghunter.com/sales-tracker")
  data=None
  if "Login" in driver.title:
    login(driver=driver)
    try:
      WebDriverWait(driver,10).until(expected_conditions.title_contains("Dashboard"))
    except Exception as e:
      logger.error(e)
      print(e)
    else:
      data = getTrackedSites(driver=driver)
  elif "Sales" in driver.title:
    try:
      WebDriverWait(driver,10).until(element_exists("#store-table"))
    except Exception as e:
      logger.error(e)
      print(e)
    data = driver.execute_script("""
    var table = document.querySelector("#store-table");
    var data=[];
    for(var i=1;i<table.rows.length;i++){
      var row={
        "store":table.rows[i].cells[0].innerText,
        "today":table.rows[i].cells[1].innerText,
        "yesterday":table.rows[i].cells[2].innerText,
        "7days":table.rows[i].cells[3].innerText,
        "30days":table.rows[i].cells[4].innerText
      };
      data.push(row);
    };
    return data;
    """)
  
  return data

def addTrackedSite(driver:Chrome,url:str):
  driver.get("https://app.winninghunter.com/sales-tracker")
  data=None
  if "Login" in driver.title:
    login(driver=driver)
    try:
      WebDriverWait(driver,10).until(expected_conditions.title_contains("Dashboard"))
    except Exception as e:
      logger.error(e)
      print(e)
    data = addTrackedSite(driver=driver,url=url)
  elif "Sales" in driver.title:
    enterSiteUrl(driver=driver,url=url)
    try:
      WebDriverWait(driver,10).until(expected_conditions.title_contains("Details"))
    except Exception as e:
      logger.error(e)
      print(e)
    data = getTrackedSites(driver=driver)
  
  return data