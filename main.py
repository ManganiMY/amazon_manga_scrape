import time
import isbnlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

volumes = {
    "9784088838212" : ["Two On Ice 1","TOI 1"],
    "9784088838199" : ["Kagurabachi 1","KGB 1"],
    "9784088838175" : ["MamaYuyu 1","MMYY 1"],
}

def load_volumes(volumes):
    """Function Loading Volumes"""
    volumes_list = {}
    for isbn, [_, shorthand] in volumes.items():
        isbn10 = isbnlib.to_isbn10(isbn)
        volumes_list[isbn10] = isbn
    return volumes_list

def amazon_extract(volumes_list):
    """Function for Scraping from Amazon"""
    rank_list = {}
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    url = "https://www.amazon.co.jp/dp/"
    for asin, _ in volumes_list.items():
        single_list = []
        driver.get(url + str(asin))
        time.sleep(2)
        detail_box = driver.find_element(By.ID, 'detailBulletsWrapper_feature_div')
        a_elements = detail_box.find_elements(By.CSS_SELECTOR, 'a[href]')

        for a_element in a_elements:
            # Use XPath to select the previous sibling element
            parent_span_text = a_element.find_element(By.XPATH, '..')
            number_str  = parent_span_text.text.split(': #')[1].split('in')[0]
            clean = int(number_str.replace(',', ''))
            single_list.append(clean)
        rank_list[asin]= single_list

    driver.quit()
    return rank_list

if __name__ == "__main__" :
    volumes_list = load_volumes(volumes)
    rankings = amazon_extract(volumes_list)
    final_list = [
        {'name': volumes[volumes_list[key]][0], 
         'ranking': rankings[key][0]
         } for key in volumes_list if key in rankings]
    sorted_list = sorted(final_list, key=lambda x: x['ranking'])
    for item in sorted_list:
        print(f"{item['name']}: {item['ranking']}")
    