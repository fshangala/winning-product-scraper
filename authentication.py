from selenium.webdriver import Chrome

def login(driver:Chrome):
  email = self.driver.find_element(By.NAME, "Email")
  email.send_keys("malaky31@hotmail.fr")
  password = self.driver.find_element(By.NAME, "Password")
  password.send_keys("12345678")
  button = self.driver.find_element(By.CSS_SELECTOR, 'button.login')
  button.click()