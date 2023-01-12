from selenium import webdriver 
from selenium.webdriver.common.by import By
import openpyxl
from cockroach import developing_cockroach as developer


import time
from app.lib.blocs.excel import BlocExcel


from app.lib.models.urls import URL_BEBIDAS

# Inicializando o documento excel.
_document = BlocExcel(fileName='bazara_bebidas', columnNames=['PRODUCT_NAME', 'PRODUCT_LINK'], sheetName='BEBIDAS')

# Função para clicar no butão de cockies.
#
def accept_cockies(firefox : webdriver.Firefox, class_name: str):
    time.sleep(45) # await load page
    button = firefox.find_element(By().CLASS_NAME, class_name)
    button.click()


def scraping(list_item):
    # Consummer.
    # html navigational structure.

    shaved = 0
    for ELEMENT in list_item:

        div_class_product_item_info = ELEMENT.find_elements(By().TAG_NAME, 'div')
        div_class_image_grid = div_class_product_item_info[0].find_elements(By().TAG_NAME, 'div')

        # photo bloc
        #
        a_class_product_photo = div_class_image_grid[0].find_element(By().TAG_NAME, 'a')
        span1 = a_class_product_photo.find_element(By().TAG_NAME, "span")
        span2 = span1.find_element(By().TAG_NAME, "span")
        img = span2.find_element(By().TAG_NAME, "img")

        # details bloc
        #
        div_class_product_item_details = div_class_product_item_info[0].find_element(By().CLASS_NAME, 'product-item-details')
        strong_class_product_ite_name = div_class_product_item_details.find_element(By().CLASS_NAME, 'product-item-link')
        product_name = strong_class_product_ite_name.get_attribute('title')
        product_page = strong_class_product_ite_name.get_attribute('href')

        # print(product_name)
        _document.save_data_in_excel([product_name,product_page])
        shaved += 1
        print('Product scraping: {}/{}'.format(shaved, len(list_item)))

    _document.generate_and_save_excel()

    developer.log('✔ Program finished. Found errors. 0.', name= 'Scraping')

def next_page(browser:webdriver.Firefox):
    try:
        print('5 seconds to the next page. Wait a moment.')
        time.sleep(5)
        browser.find_element(By().CLASS_NAME, "pages-item-next").find_element(By().TAG_NAME, "a").click()
        print('Going to the next page...')
        return True
    except:
        developer.log('No more pages to scratch.')
        return False
    