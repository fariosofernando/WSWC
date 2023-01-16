from selenium import webdriver 
from selenium.webdriver.common.by import By
import openpyxl
from cockroach import developing_cockroach as developer


import time
from app.blocs.excel import BlocExcel

# Função para clicar no butão de cockies.
#
def accept_cockies(firefox : webdriver.Firefox, class_name: str):
    button = firefox.find_element(By().CLASS_NAME, class_name)
    button.click()


def scraping(document:BlocExcel, list_item):
    # Consummer.
    # html navigational structure.

    shaved = 0
    for ELEMENT in list_item:
        product_price2 = ''
        product_page = ELEMENT.find_element(By.XPATH, "//div[@class='woo-entry-image clr']").find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
        product_name = ELEMENT.find_element(By.XPATH, "//div[@class='woo-entry-image clr']").find_elements(By.TAG_NAME, "a")[0].find_element(By.TAG_NAME, "img").get_attribute("alt")
        product_price = ELEMENT.find_element(By.XPATH, "//ul[@class='woo-entry-inner clr']").find_element(By.CLASS_NAME, "price-wrap").find_element(By.CLASS_NAME, "price").find_elements(By.TAG_NAME, "bdi")[0].text
        
        try:
          product_price2 = ELEMENT.find_element(By.XPATH, "//ul[@class='woo-entry-inner clr']").find_element(By.CLASS_NAME, "price-wrap").find_element(By.CLASS_NAME, "price").find_elements(By.TAG_NAME, "bdi")[1].text
        except:
          ...

        if product_price2 !='': document.save_data_in_excel([product_name,product_page,product_price+' - '+product_price2])
        else: document.save_data_in_excel([product_name,product_page,product_price])
        
        shaved += 1
        print('Product scraping: {}/{}'.format(shaved, len(list_item)))

def next_page(browser:webdriver.Firefox):
    try:
        print('2 seconds to the next page. Wait a moment.')
        time.sleep(2)
        browser.find_element(By.XPATH, "//a[@class='next page-numbers']").click()
        print('Going to the next page.')
        
        # Caracas! Isso resolveu um problema de 1 hora em 1 segundo.
        time.sleep(2)
        browser.refresh() # O refresh permite que os elementos permançam como estavam no primeiro estado.
        time.sleep(1)
        return True
    except:
        developer.log('No more pages to scratch.')
        return False
    