# Market Scrapping for Chile 
![ETL!](https://www.era-environmental.com/hs-fs/hubfs/ETL-era-environmetal-management.png?width=566&name=ETL-era-environmetal-management.png "ETL")

El proposito de este proyecto es extraer la data de los principales marketplace de chile como lo son [Santaisabel](https://www.santaisabel.cl/), [Jumbo](https://www.jumbo.cl/), [Tottus](https://tottus.falabella.com/tottus-cl?kid=se81to&gclid=Cj0KCQjwhY-aBhCUARIsALNIC06Icn1eNpbmfsOP3UEkCniB333rVUK1W047Y-7_9bShba64AWSH3nsaAkJfEALw_wcB), [Lider](https://www.lider.cl/supermercado/) (pronto). Con el objectivo de analisar los datos, identificar patrones, aplicar estadistica descriptiva y e inferencial 

## ETL (Extract Transform Load)
Esta primera parte se centra en extraer los datos de distintas fuentes (jumbo,santa isabel, lider). 

Luego hacer una transformación de la data 
- Validación y Data Cleaning 
    - Eliminar o llenar valores nulos 
    - Eliminar duplicados 
    - Convertir el texto a minúscula
    - Quitar símbolo de moneda
    - Convertir monedas en formato de string (cadena de texto) a formato numérico
    - Convertir fecha en formato de string (cadena de texto) a formato fecha
  
- Feature engineering or feature extraction(extraccion de caracteristicas).
    - Extraer el valor en gramos de una cadena de texto y guardarla una nueva columna llamada [weight_unit] 
    - Extraer la categoría de la url y guardarla en una nueva columna llamada categoría



y finalmente guardar los datos en una carpeta clean_data en un formato .csv  para su posterior analisis y visualizacion 

## instalación 
- Crear un ambiente virtual
 ```sh
python3 -m venv venv
 ```
- Activar el ambiente en bash
```sh
source venv/Scripts/activate  
```
- activar el ambiente con fish
```sh
source venv/bin/activate.fish 
```
- instalar los paquetes y librerías necesarias 
```sh
pip install requirements.txt 
```

## Implementando un web scrapper: Configuracion
Nos posicionamos en la carpeta contenedora de nuestro proyecto (./ETL) y ejecutamos la aplicación con el siguiente comando:
```sh
python main.py
```

Esto mostrará un  menú con las siguientes opciones 

```sh
 """
    ---------------------------------------------------
                        MENU
    ---------------------------------------------------
    -- 1 Scrapping PRESS 1 or s
    -- 2 transform the data PRESS 2 or t
    -- 3 transform all the data PRESS 3 or a
    -- 4 Quit PRESS 4 or q

"""
```

Donde 
1. La opción uno llama a la clase **supermarket-pages.py** que hace scrapping al los sitios web guardados en el archivo config  
 
      1.1 - las opciones disponibles permiten hacer scrapping a santaisabel y jumbo
2. La opción 2 muestra todos los archivos en formato csv como una lista. donde el usuario puede elegir qué archivo quiere preprocesar.


    **Nota**:la transformación de los dato permite.
    - Detectar y reemplazar faltantes.
    - Establecer el formateado de los datos.
    - Eliminar y limpiar los datos incorrectos y duplicados.
    
3. Finalmente la opción 3 hace lo mismo que la opción 2 excepto que lo hace a todos los datos 

## Screenshot 
coming soon
![Coming soon!](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9Spp6r0iD2tV1nF4H-FlnUF_sTJTGmS7gBg&usqp=CAU "Coming soon")

## Facturas Actualización
 - hacer que el script se ejecute de forma automática en una hora determinada (usando apache airflow)
 - agregar más sitios web
 - general un informe de eventos
 - desacoplar las clases y usar patrones de diseños. 

