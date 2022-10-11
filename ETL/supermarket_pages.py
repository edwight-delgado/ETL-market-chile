

from inspect import Attribute
from common import config

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import datetime, time
import csv
import logging as log

from os import path

now = datetime.datetime.now().strftime("%m-%d-%Y")
#log.basicConfig(filename='./debug.log', encoding='utf-8', level=log.INFO)
#__global_var = []
class BasePage:
    """clase pricipal (superClase) """
    def __init__(self, items_site_uid) -> None:
        self.site_name = items_site_uid
        self._config = config()['market_sites'][items_site_uid]
        self._queries = self._config['queries']
        self._links = self._config['links']
        self._url = self._config['base_url']
        
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        #self.driver.maximize_window()

    def _visit(self,url):
        """visita la pagina indicada"""
        self.driver.get(url)


    def _select(self,product,query, item_attribute):
        try:
            if item_attribute=='ID':
                attribute = By.ID
            elif item_attribute == 'CLASS_NAME':
                attribute = By.CLASS_NAME
            elif item_attribute == 'CSS':
                attribute= By.CSS_SELECTOR
            #print(element[0].get_attribute('innerHTML'))
            d = product.find_element(by=attribute,value=query).text
            return d
        except:
            log.error("Serious stuff, this is red for a reason in _select method")
            d = ''
            return d

    def select_attribute(self, item_attribute):
        if item_attribute=='ID':
            attribute = By.ID
        elif item_attribute == 'CLASS_NAME':
            attribute = By.CLASS_NAME
        elif item_attribute == 'CSS':
            attribute= By.CSS_SELECTOR

        return attribute

    def brand(self, product):
        #marca del producto
        query = self._queries['product_brand'][0]
        attribute = self._queries['product_brand'][1]
        result = self._select(product, query, attribute)
        print('marca:',result)
        return result if len(result) else ''

    def title(self, product):
        #obtiene el nombre del producto
        query = self._queries['product_name'][0]
        attribute = self._queries['product_name'][1]
        result = self._select(product, query, attribute)
        print('nombre:',result)
        return result if len(result) else ''

    def link(self, product):
        #obtiene el link del producto
        query = self._queries['product_link'][0]
        attribute = self._queries['product_link'][1]
        result = product.find_element(by=By.CSS_SELECTOR, value=query).get_attribute('href')
        return result if len(result) else ''
    
    def oferta(self, product):
        #ingredientes 
        query = self._queries['product_offer'][0]
        attribute = self._queries['product_offer'][1]
        result = self._select(product, query, attribute)
        return result if len(result) else ''

    def price_ref(self, product):
        #obtiene el precio ref del producto

        query = self._queries['product_price_ref']
        result = self._select(product, query)
        return result if len(result) else ''

    def price(self, product):
        #obtiene el precio del producto
        #_scrapper
        query = self._queries['product_price'][0]
        attribute = self._queries['product_price'][1]
        result = self._select(product, query,attribute)
        print('price')
        print(result)
        return result if len(result) else ''

    def rating(self, product):
        #rating del producto
        query = self._queries['product_rating']
        result = self._select(product, query)
        #log.warn("Something is wrong and any user should be informed")
        return result if len(result) else ''

    def unit(self, product):
        #rating del producto
        query = self._queries['product_unit'][0]
        attribute = self._queries['product_unit'][1]
        result = self._select(product, query, attribute)
        #log.warn("Something is wrong and any user should be informed")
        return result if len(result) else ''

    def stock(self, product):
        #rating del producto
        query = self._queries['product_out_stock']
        result = self._select(product, query)
        #log.warn("Something is wrong and any user should be informed")
        return result if len(result) else ''

class HomePage(BasePage):
    def __init__(self, items_site_uid) -> None:
        super().__init__(items_site_uid)
    def num_page(self, url):
        self._visit(url)
        print(f'scrapping --> {url}')
        if self.site_name =='tottus':
            try:
                page_number = self.driver.find_elements(By.CSS_SELECTOR, '.search-results.jsx-4099777552 li.jsx-1104282991')
                print('page dd',page_number)
                return page_number[-1].text
                #print('page number: ',page_number.text)
            except:
                page_number = 1
                return page_number

        else:
            try:
                page_number = WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'page-number')))
                #page_number = self.driver.find_element(by=By.CLASS_NAME,value='page-number').text
                return page_number[-1].text
            except:
                page_number = 1
                return page_number

    def _select_main_link(self):
        """
        metodo que retorna una url valida con paginacion 
        """
        base_url = self._url
        all_links =[]
        for link in self._links:
            url = f'{base_url}/{link}'
            pages = self.num_page(url)
            #print('----------url--------------')
            #print(pages)
            for page in range(1, int(pages) + 1):
                if page > 1:
                    if self.site_name == "tottus":
                        url = f'{base_url}/{link}?page={page}'
                    elif (self.site_name == "santaisabel") or (self.site_name == "jumbos") :
                        url = f'{base_url}/{link}?page={page}'

                
                all_links.append(url)
                #self._select_element(url)
        log.info("links was Success !")
        #print('link are Success!!!')
        return all_links

    def _fetch_item(self,items):
        item_product=[]
        log.info("beggin _fetch_item ....")
        for product in items:
            #print(product.text)
            #time.sleep(1)
            try:
                #get link 
                brand = self.brand(product)
                name =  self.title(product)
                price =  self.price(product)
                link = self.link(product)
                #oferta = self.oferta(product)
                #rating = self.rating(product)
                #unit = self.unit(product)
                
                item_product.append({
                    'brand':brand,
                    'name':name,
                    'price':price,
                    #'oferta':oferta,
                    'link':link,
                    #'rating':rating,
                    #'unit':unit
            
                }) 
            except:
                log.error("Serious stuff, this is red for a reason in _fetch_item")
            
        return item_product
        
    def _select_element(self, url):
        out_file_name = 'data/{site_name}_{datetime}_products.csv'.format(
                    site_name=self.site_name,
                    datetime=now
                )
        item_prop = []
        for this_url in url:
            
            log.info(f"working ... scraping --> {this_url}")
            print(f"working ... scraping --> {this_url}")
            
            #time.sleep(2)
            self._visit(this_url)
            #----------------------- frament waiting for be changed ------------------------------
            product_item = self._queries['product_item'][0]
            item_attribute = self._queries['product_item'][1]
            #attribute = self.select_attribute(item_attribute)
            if item_attribute=='ID':
                attribute = By.ID
            elif item_attribute == 'CLASS_NAME':
                attribute = By.CLASS_NAME
            elif item_attribute == 'CSS':
                attribute= By.CSS_SELECTOR
 
            items = WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located((attribute,product_item)))
            #items = self.driver.find_element(attribute,product_item)
            #------------------------ end frament -------------------------------------------------

            if path.exists(out_file_name):
                #now = datetime.datetime.now().strftime('%Y_%m_%d')
                
                with open(out_file_name, mode='a', encoding='utf-8') as f: # w+ significa escribir, y si no existe, lo crea
                    #print('prueba 2')
                    writer = csv.writer(f)
                    #print(self._fetch_item(items))
                    for item in self._fetch_item(items):
                        print(item)
                        writer.writerow([
                            self.site_name,
                            item['name'],
                            item['price'],
                            item['brand'],
                            #item['unit'],
                            item['link'],
                            now,
                            this_url,
                            #item['oferta'],
                            #item['rating']
                        ])
            #-------------------------------------------------
                        #print(item['name'])
            #--------------------------------------------------
            else:
                csv_headers =  ['site', 'title', 'price', 'brand', 'unit','link','date','this_url','oferta','rating']
                with open(out_file_name, mode='w+') as f: # w+ significa escribir, y si no existe, lo crea
                    writer = csv.writer(f)
                    writer.writerow(csv_headers)
                
                    for item in self._fetch_item(items):
                        writer.writerow([
                            self.site_name,
                            item['name'],
                            item['price'],
                            item['brand'],
                            item['unit'],
                            item['link'],
                            now,
                            this_url,
                            item['oferta'],
                            item['rating']
                        ])
            #-------------------------------------------------
                        #print(item['name'])
            #--------------------------------------------------
            #print(items_site_uid)
            
        print('item link  Success!!!')
        #return item_prop


h = HomePage('santaisabel')
print(h)
links = h._select_main_link()
#print(links)
elements = h._select_element(links)

