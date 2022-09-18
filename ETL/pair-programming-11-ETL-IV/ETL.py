import pandas as pd
import numpy as np
import requests
import ast 
from datetime import datetime, timedelta
import mysql.connector


class Extraccion: 

    def __init__(self, paises):


        self.paises = paises

    def cargar_ataques(self, ruta_archivo):

        self.ruta_archivo = ruta_archivo

        df_ataques = pd.read_csv(ruta_archivo, index_col=0)

        lista_paises = []
        
        for k in self.paises.keys():

            lista_paises.append(k.lower())

        df_ataques = df_ataques[df_ataques['country'].isin(lista_paises)]

        return df_ataques


    
    def llamada_API(self, producto):

        self.producto = producto

        df_final = pd.DataFrame()

        for key, value in self.paises.items():
        
            url = f'http://www.7timer.info/bin/api.pl?lon=-{value[1]}&lat={value[0]}&product={producto}&output=json'

            response = requests.get(url=url)
            codigo_estado = response.status_code
            razon_estado = response.reason
            if codigo_estado == 200:
                print('La peticion se ha realizado correctamente, se ha devuelto el código de estado:',codigo_estado,' y como razón del código de estado: ',razon_estado)
            elif codigo_estado == 402:
                print('No se ha podido autorizar usario, se ha devuelto el código de estado:', codigo_estado,' y como razón del código de estado: ',razon_estado)
            elif codigo_estado == 404:
                print('Algo ha salido mal, el recurso no se ha encontrado,se ha devuelto el código de estado:', codigo_estado,' y como razón del código de estado: ',razon_estado)
            else:
                print('Algo inesperado ha ocurrido, se ha devuelto el código de estado:', codigo_estado,' y como razón del código de estado: ',razon_estado)
            
            df = pd.json_normalize(response.json()["dataseries"])
            df['latitud'] = value[0]
            df['longitud'] = value[1]
            df['pais'] = key
            df_final = pd.concat([df_final,df], axis=0, ignore_index=True) 
         
        return df_final
    
    def limpiar_columnas_meteo(self, df_meteo):

        x = df_meteo['wind_profile'].apply(pd.Series)

        for i in range(len(x.columns)): 

            nombre = 'windspeed_' + str(x[i].apply(pd.Series)['layer'][0])

            valores = list(x[i].apply(pd.Series)["speed"] )

            df_meteo.insert(i, nombre, valores)

        x = df_meteo['rh_profile'].apply(pd.Series)

        for i in range(len(x.columns)): 

            nombre = 'rh_' + str(x[i].apply(pd.Series)['layer'][0] )
            valores = list(x[i].apply(pd.Series)["rh"] )

            df_meteo.insert(i, nombre, valores)

        return df_meteo

    def meteo_medias_fecha(self, df_meteo):

        df_meteo_medias = df_meteo.groupby('pais').apply(lambda x: x.mean())

        df_meteo_medias.reset_index(inplace=True)

        df_meteo_medias['pais'] = df_meteo_medias['pais'].apply(lambda x: x.lower())

        hoy = datetime.now()
        
        hoy = datetime.strftime(hoy, '%Y-%m-%d')
        
        df_meteo_medias["fecha_descarga"] = hoy

        df_meteo_medias.to_csv('../../datos/meteo_medias.csv')
        df_meteo_medias.to_csv('../../datos/meteo_medias.pkl')

        
        return df_meteo_medias 


    def juntar_dfs(self, df_meteo_medias, df_ataques): 

        df_ataques_meteo =  pd.merge(left = df_ataques, right= df_meteo_medias, how= "left", left_on= "country", right_on= "pais")
        
        #eliminamos columna duplicada
        df_ataques_meteo.drop(columns='pais', axis=1, inplace=True)

        # guardamos los datos
        df_ataques_meteo.to_pickle('../../datos/attacks_meteo.pkl')
        df_ataques_meteo.to_csv('../../datos/attacks_meteo.csv')

        return df_ataques_meteo
    

    def chequear_datos(self, df_ataques_meteo): 
    
        print("Las columnas son:", "\n")
        print(list(df_ataques_meteo.columns))
        print("-----------------------------------------")

        print("Los tipos de datos que tenemos son:", "\n")
        print(df_ataques_meteo.dtypes)
        print("-----------------------------------------")

        print("El porcentaje de nulos:", "\n")
        print((df_ataques_meteo.isnull().sum() / df_ataques_meteo.shape[0]) *  100)


class Cargar:
    
        def __init__(self, nombre_bbdd, contraseña):
            
            self.nombre_bbdd = nombre_bbdd
            self.contraseña = contraseña

        # método para crear la BBDD 
        def crear_bbdd(self):

            mydb = mysql.connector.connect(host="127.0.0.1",
                                        user="root",
                                        password=f'{self.contraseña}') 
            mycursor = mydb.cursor()
            print("Conexión realizada con éxito")

            try:
                mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.nombre_bbdd};")
                print(mycursor)
                
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg) 
                    
        # método para crear tablas  e insertar datos en ellas   
        def crear_insertar_tabla(self, query):
            
            mydb = mysql.connector.connect(host="127.0.0.1",
                                        user="root",
                                        password=f'{self.contraseña}', 
                                        database=f"{self.nombre_bbdd}") 
            mycursor = mydb.cursor()
            
            try:
                mycursor.execute(query)
                mydb.commit()
            
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)