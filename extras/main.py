# importamos todas las librerias que son necesarias para que nuestro código funcione. Estas librerías son las que hemos usado en las clases invertidas de ETL-II y ETL-III. 

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import mysql.connector

# lo primero que hicimos fue cargar los datos que habíamos descargado de la API del tiempo en la clase ETL-I.

df = pd.read_csv('datos/datos_actualizados.csv')

print("csv cargado")


# vamos a crearnos una serie de inputs para preguntarle al cliente sobre que ciudad quiere la información climática y que información quiere

ciudad = input("¿De qué ciudad quieres la información climática? ")
print("---------------------------------------------------------------")

latitud = float(input("Indica la latitud de la ciudad de la que quieres información "))
print("---------------------------------------------------------------")

longitud = float(input("Indica la longitud de la ciudad de la que quieres información "))
print("---------------------------------------------------------------")

producto = input("¿Indica el primer producto que quieres? ")
print("---------------------------------------------------------------")

producto2 = input("¿Indica el segundo producto que quieres? ")
print("---------------------------------------------------------------")

# En las lecciones anteriores lo que hicimos fue la creacion de la clase. Lo que tendremos que hacer es traernos la clase a nuestro `.py`. Este fichero debe estar lo más limpio posible, es decir, no deberemos incluir la clase en nuestro main.py
# para evitar esto lo que haremos será crearnos un archivo `.py` extra donde guardaremos la clase. En este caso es solo una clase, pero imaginad que tenemos muchísimas funciones. También lo podremos hacer. Podemos meter tantas clases y funciones como queramos. 
# En nuestro caso, el archivo "extra" se llama "soporte.py"
# Vale, pero ahora... como hacemos para "traernos" la clase a este archivo? 🤔. Tendremos que hacer un import como los que hacemos como las librerías. 

import soporte as sp # import ELNOMBREDELFICHERO y le ponemos un alias (igual que con Pandas o Numpy)

# Una vez importada, ya podemos llamar a la clase e iniciarla igual que hicimos en el jupyter. 
# Solo habrá una diferencia, al hacer el import le pusimos un alias. Tendremos que usarlo para llamar a la clase. Igual que hacemos con los métodos de Pandas

# iniciamos la clase
api = sp.Extraccion(latitud, longitud, ciudad)

# utilizamos el metodo de "llamada API" para obtener los datos de la API
print(f"Estamos haciendo la llamada a la API para la ciudad {ciudad} para el producto {producto}".format(ciudad = ciudad, producto = producto))
df_civil = api.llamada_API("civil")

print("-----------------------------------------")

# hacemos la llamada a la API para obtener los datos del segundo producto
print(f"Estamos haciendo la llamada a la API para la ciudad {ciudad} para el producto {producto2}".format(ciudad = ciudad, producto = producto))
df_astro = api.llamada_API("astro")


# el siguiente paso es limpiar los datos de los dataframes
print("-----------------------------------------")
print(f"Estamos limpiando los datos de los datos del producto {producto}")
df_civil = api.limpiar_civil(df_civil)
print(df_civil)
print("-----------------------------------------")


print("-----------------------------------------")
print(f"Estamos limpiando los datos de los datos del producto {producto2}")
df_astro = api.limpiar_astro(df_astro)


# juntamos los dataframes
print("-----------------------------------------")
print("Estamos juntando los dataframes")
df_completo = api.juntar_dfs(df, df_civil, df_astro)

# chqueamos los datos

print("-----------------------------------------")
print("Estamos revisando la estructura de los datos")
api.chequear_datos(df_completo)

# definimos las columnas que tienen nulos

columnas_con_nulos = ["seeing", "transparency", "fecha", "latitud", "longitud", 'ciudad_x', "ciudad_y"]

# limpiamos el dataframe 
df_final = api.limpiar_dataframe(df_completo, columnas_con_nulos)

print("El proceso ya ha termiando, tienes todos tus datos almacenados en tu ordenador")
