# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script file developed by edwight
github.com/edwight-delgado

"""

from common import config
from supermarket_pages import HomePage
import requests
import os
import transform_data
def main(site):
    this_site = config()['market_sites'][site]
    _url = this_site['base_url']
    try:
        r = requests.get(_url, timeout=6)
        code = r.status_code
        print(code)
        if code == 200:
            print(r.status_code)
            h = HomePage(site)
            links = h._select_main_link()
            h._select_element(links)
    except (requests.ConnectionError,requests.Timeout):
        print('no internet conetion ')

if __name__ == '__main__':

    MENU = """
    ---------------------------------------------------
                        MENU
    ---------------------------------------------------
    -- 1 Scrapping PRESS 1 or s
    -- 2 transform the data PRESS 2 or t
    -- 3 transform all the data PRESS 3 or a
    -- 4 Quit PRESS 4 or q

    """
    directory = 'data/'
    files_list = os.listdir(directory)
   
    option = input(MENU)
    if option =='1' or option == 's':
        maket_site = config()['market_sites'].keys()
        for value, key in enumerate(maket_site):
            print(value, key)
            
        option2 = int(input('select any value:'))

        if option2 in range(len(maket_site)):
            site = list(maket_site)[option2]
            main(site)
        else:
            print('option invalida:')
    elif option == '2' or option == 't':
        for value,files in enumerate(files_list):
            print(value, files)

        option_file = int(input('select any value:'))
        if option_file in range(len(files_list)):
            transform_data.main(directory + files_list[int(option_file)]) # limpiamos la data y se le da formato 
        else:
            print('option invalida:')

    elif option == '3' or option == 'a':
        for files in files_list:
            transform_data.main(directory + files)
