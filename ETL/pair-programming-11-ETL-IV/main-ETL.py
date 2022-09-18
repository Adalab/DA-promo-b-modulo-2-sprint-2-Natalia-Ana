# importamos todas las librerias que son necesarias para que nuestro código funcione. 

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import mysql.connector


# Creamos los inputs para preguntar al cliente sobre que pais quiere recibir la información

pais = {}

paises = input("¿De qué pais quieres la información climática? ")
print("---------------------------------------------------------------")

latitud = float(input("Indica la latitud del pais del que quieres información "))
print("---------------------------------------------------------------")

longitud = float(input("Indica la longitud del pais del que quieres información "))
print("---------------------------------------------------------------")

producto = input("¿Indica el primer producto que quieres? ")
print("---------------------------------------------------------------")

ruta_ataques = input("Indica la ruta de tu archivo de ataques de tiburones")

pais[paises] = [latitud, longitud]

# Importamos nuestro archivo ETL.py con toda la información de nuestras clases

import ETL as etl 


# iniciamos la clase de extracción
api = etl.Extraccion(pais)

# utilizamos el metodo de "llamada API" para obtener los datos de la API
print(f"Estamos haciendo la llamada a la API para el país {pais} para el producto {producto}".format(pais = pais, producto = producto))
df_meteo = api.llamada_API(producto)

print("-----------------------------------------")

#Limpiamos nuestro dataframe de datos meteo
print(f'Estamos limpiando nuestro data frame para el producto {producto} y el/los pais/es {paises.keys()}')
df_meteo = api.limpiar_columnas_meteo(df_meteo)

print("-----------------------------------------")

# Calculamos las medias para nuestro data frame meteo

print(f'Estamos extrayendo un data frame con sólo la media de la información climática')
df_meteo_medias = api.meteo_medias_fecha(df_meteo)

print("-----------------------------------------")

# el siguiente paso es cargar nuestro archivo de ataques 

print('Cargamos el archivo con la información de los ataques de tiburones')
df_ataques = api.cargar_ataques(ruta_ataques)

print("-----------------------------------------")


# juntamos los dataframes
print("-----------------------------------------")
print("Estamos juntando los dataframes")
df_ataques_meteo = api.juntar_dfs(df_meteo_medias, df_ataques)

# chequeamos los datos

print("-----------------------------------------")
print("Estamos revisando la estructura de los datos")
api.chequear_datos(df_ataques_meteo)

print("-----------------------------------------")


print('Ahora crearemos la base de datos')

contraseña = input('Ingresa la contraseña de tu servidor')

nombre_bbdd = input('Ingresa el nombre para tu Base de Datos')

# iniciamos la clase Cargar

cargar_meteo = etl.Cargar(nombre_bbdd, contraseña)

# creamos nuestra bbdd

print('Estamos creando nuestra base de datos')
cargar_meteo.crear_bbdd()

# creamos nuestras tablas

print("-----------------------------------------")


print('Estamos creando nuestras tablas')

tabla_ataques = ''' CREATE TABLE IF NOT EXISTS `ataques` (
    `id_ataques` INT NOT NULL AUTO_INCREMENT, 
    `case_number` VARCHAR(50) NOT NULL,
    `year` INT NOT NULL, 
    `mes` VARCHAR(20) NOT NULL,
    `type` VARCHAR(50) NOT NULL, 
    `country` VARCHAR(50) NOT NULL,  
    `age` FLOAT NOT NULL,
    `species` VARCHAR(50)  NOT NULL,
    `fatal` VARCHAR (20) NOT NULL,
    `sex` VARCHAR (20) NOT NULL,
    PRIMARY KEY (`id_ataques`))
    
    ENGINE = InnoDB;
    '''

cargar_meteo.crear_insertar_tabla(tabla_ataques)

tabla_clima = ''' CREATE TABLE IF NOT EXISTS `clima` (
    `id_clima` INT NOT NULL AUTO_INCREMENT, 
    `country` VARCHAR (50) NOT NULL,
    `rh_950mb` FLOAT NOT NULL, 
    `rh_900mb` FLOAT NOT NULL, 
    `rh_850mb` FLOAT NOT NULL, 
    `rh_800mb` FLOAT NOT NULL, 
    `rh_750mb` FLOAT NOT NULL, 
    `rh_700mb` FLOAT NOT NULL,
    `rh_650mb` FLOAT NOT NULL, 
    `rh_600mb` FLOAT NOT NULL, 
    `rh_550mb` FLOAT NOT NULL, 
    `rh_500mb` FLOAT NOT NULL, 
    `rh_450mb` FLOAT NOT NULL, 
    `rh_400mb` FLOAT NOT NULL,
    `rh_350mb` FLOAT NOT NULL, 
    `rh_300mb` FLOAT NOT NULL, 
    `rh_250mb` FLOAT NOT NULL, 
    `rh_200mb` FLOAT NOT NULL, 
    `windspeed_950mb` FLOAT NOT NULL,
    `windspeed_900mb` FLOAT NOT NULL, 
    `windspeed_850mb` FLOAT NOT NULL, 
    `windspeed_800mb` FLOAT NOT NULL,
    `windspeed_750mb` FLOAT NOT NULL, 
    `windspeed_700mb` FLOAT NOT NULL, 
    `windspeed_650mb` FLOAT NOT NULL,
    `windspeed_600mb` FLOAT NOT NULL, 
    `windspeed_550mb` FLOAT NOT NULL, 
    `windspeed_500mb` FLOAT NOT NULL,
    `windspeed_450mb` FLOAT NOT NULL, 
    `windspeed_400mb` FLOAT NOT NULL, 
    `windspeed_350mb` FLOAT NOT NULL,
    `windspeed_300mb` FLOAT NOT NULL, 
    `windspeed_250mb` FLOAT NOT NULL, 
    `windspeed_200mb` FLOAT NOT NULL, 
    `timepoint` FLOAT NOT NULL,
    `cloudcover` FLOAT NOT NULL, 
    `highcloud` FLOAT NOT NULL, 
    `midcloud` FLOAT NOT NULL, 
    `lowcloud` FLOAT NOT NULL, 
    `temp2m` FLOAT NOT NULL, 
    `lifted_index` FLOAT NOT NULL, 
    `rh2m` FLOAT NOT NULL, 
    `msl_pressure` FLOAT NOT NULL,
    `prec_amount` FLOAT NOT NULL, 
    `snow_depth` FLOAT NOT NULL, 
    `wind10m.direction` REAL DEFAULT NULL,
    `wind10m.speed` FLOAT DEFAULT NULL, 
    `latitud` FLOAT NOT NULL, 
    `longitud` FLOAT NOT NULL, 
    `fecha_descarga` VARCHAR (20) NOT NULL,
    PRIMARY KEY (`id_clima`))
    
    ENGINE = InnoDB;
    '''

cargar_meteo.crear_insertar_tabla(tabla_clima)

print("-----------------------------------------")





print("El proceso ya ha termiando, tienes todos tus datos almacenados en tu ordenador")



