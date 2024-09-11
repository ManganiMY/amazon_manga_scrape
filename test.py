from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

driver.get("https://www.amazon.co.jp")
print(driver.title)
driver.quit()