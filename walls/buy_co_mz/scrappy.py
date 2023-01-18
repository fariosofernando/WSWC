from selenium import webdriver 
from selenium.webdriver.common.by import By
from cockroach import developing_cockroach as developer


import time
from app.blocs.excel import BlocExcel
from browser import browser

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

        product_page = 'valor não encontrado'
        product_name = 'valor nao encotrado'
        product_price = 'valor não encontrado'
        
        try:
          product_page =  ELEMENT.find_element(By.CLASS_NAME, "item-detail").find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
        except:
          print('An exception occurred')

        try:
          product_name = ELEMENT.find_element(By.CLASS_NAME, "item-detail").find_element(By.TAG_NAME, "h4").text
        except:
          print('Nome não do produto {}, não encontrado'.format(product_name))
        
        try:
            product_price = ELEMENT.find_element(By.CLASS_NAME, "item-detail").find_element(By.CLASS_NAME, "price").text
        except:
          print('Preço não do produto {}, não encontrado'.format(product_name))

        document.save_data_in_excel([product_name,product_page,product_price])
        shaved += 1
        print('Product scraping: {}/{}'.format(shaved, len(list_item)))

def next_page(browser:webdriver.Firefox):
    try:
        print('5 seconds to the next page. Wait a moment.')
        time.sleep(5)
        browser.find_element(By.CLASS_NAME, "page-numbers").find_elements(By.TAG_NAME, "li")[-1].click()
        print('Going to the next page...')
        
        # Caracas! Isso resolveu um problema de 1 hora em 1 segundo.
        time.sleep(5)
        browser.refresh() # O refresh permite que os elementos permançam como estavam no primeiro estado.
        time.sleep(1)
        return True
    except:
        developer.log('No more pages to scratch.')
        return False
    