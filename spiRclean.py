'''This algorithm meant to give some order to the SPI file and 
out take the relevant data for the next computation.'''
import pandas as pd

import os 

#Stablishing files directory.
dir = '/home/oscar_amarilla/Pasantia/SPI_regression/SPI_enero/'

#Making a list of the files in the directory.
archivos = os.listdir(dir)

#Making a list only with csv files.
#Here, "aux" is an auxiliary variable.
aux = []

for archivo in archivos:

    if archivo.endswith(".csv"):

        aux.append(archivo)

archivos = aux

#Cleaning the dataset. The cleaning consist in giving to each file
#an appropriate format for the computations propurse, this is: 
#titles and the rows corresponding to the needed period.

    #The final year must be a year after the desired final year of the period.
anho_i = '1981'

anho_f = '2011'

for archivo in archivos:

    dir_archivo = dir + archivo

    dataset = pd.read_csv(dir_archivo)

    dataset.columns=['Año-Mes','SPI_1','SPI_2','SPI_3','SPI_4','SPI_5','SPI_6','SPI_7','SPI_8','SPI_9','SPI_10','SPI_11','SPI_12']
#Splitting the Año-Mes column into two columns.
    spi_aux = dataset.drop('Año-Mes', axis=1)

    aux = dataset['Año-Mes'].str.split(expand=True)

    aux.columns=['Año', 'Mes']

    dataset = pd.concat([aux,spi_aux], axis=1)

#Taking the indexes of the relevant rows.
    fila_i = dataset.index[dataset['Año'] == anho_i].tolist()[0]

    fila_f = dataset.index[dataset['Año'] == anho_f].tolist()[0]

    dataset = dataset[fila_i:fila_f]

#Saving the output into csv files in the SPI_81-10 directory.
    dir_salida = '/home/oscar_amarilla/Pasantia/SPI_regression/SPI_81-10/' + archivo

    dataset.to_csv(dir_salida, index=False)




