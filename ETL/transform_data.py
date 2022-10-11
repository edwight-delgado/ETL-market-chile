import argparse # este módulo nos ayuda cuando vamos a crear un script
#import hashlib
#import nltk
#from nltk.corpus import stopwords # los stopwords no nos añaden valor al análisis ulterior (la, los, nos, etc.)
from urllib.parse import urlparse
import pandas as pd 
import re
import logging # con este módulo le vamos imprimiendo en la consola al usuario lo que está pasando
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__) # obtenemos una referencia a nuestro logger con nuestro nombre interno de python

def main(filename):
    logger.info('Starting cleaning process')
    #----------------------

    #----------------------
    df = _read_data(filename)
    #df = _extract_categories(df) # vamos a añadir a la columan host los host que capturemos de la columna url
    #df = _fill_missing_titles(df) # vamos a llenar los titulos vacíos
    df = _to_lower(df)
    #df = _to_datetime(df)
    #df = _remove_duplicate_entries(df, 'title') # eliminamos duplicados
    #df = _drop_rows_with_missing_values(df)
    df['unit_value'] = df['unit'].apply(_extraer_number)
    df['price'] = df['price'].apply(clean_currency).astype('float')
    _save_data(df, filename)

def _read_data(filename):
    logger.info(f'Reading file {filename}')

    return pd.read_csv(filename) # como lo vimos en el jupyter notebooks, leemos el archivo csv

def extract_categories(df):
    pass

def _remove_duplicate_entries(df, column_name):
    logger.info('Removing duplicate entries')
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)

    return df


def _drop_rows_with_missing_values(df):
    logger.info('Dropping rows with missing data')

    return df.dropna()

def clean_currency(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):
        return(x.replace('$', '').replace('.', '').replace('Normal:','').replace(',',''))
    return(x)


def _to_lower(df):
    #df.select_dtypes(include=['object','str'])
    #df.str.lower()
    df= df.applymap(lambda s:s.lower() if type(s) == str else s)
    return df

def _extraer_number(string):
    	return re.findall('[0-9]+', string)

def _to_datetime(df):
    #df['date'] = pd.to_datetime(df['date'])
    return df

def _save_data(df, filename):
    clean_filename = f'clean_{filename}'
    logger.info(f'Saving file at: {clean_filename}')
    df.to_csv(clean_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser() # preguntamos al usuario cuál es el archivo (Dataset) que queremos trabajar
    parser.add_argument( # le añadimos un argumento: filename
        'filename',
        help='The path to the dirty data',
        type=str
    )

    args = parser.parse_args() # ahora parseamos los argumentos
    df = main(args.filename) # pasamos el argumento a la función main y lo pasamos a una variable para imprimirla en la consola
    print(df)