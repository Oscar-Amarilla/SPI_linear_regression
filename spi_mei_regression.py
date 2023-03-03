'''This algorithm return two list of dataframes for each station. The first contains dataframes with SPI values, one dataframe per SPI kind (monthly, bimonthly, quaterly, and so on); the second contains dataframe with the multiple linear regression coefficients.'''

import pandas as pd

import numpy as np

import os 

from sklearn import preprocessing

from sklearn.linear_model import LinearRegression

from sklearn.model_selection import train_test_split

from sklearn.metrics import r2_score

#Getting the MEI index data.
X_data = pd.read_csv('MEI.csv')

#Taking the headers of the MEI file, it contains the month of each MEI computation.
bimestrales = list(X_data)[1:]

#Taking just the data and not the date information.
X = X_data[bimestrales]

#This list will contain the MEI data.
mei = []

for i in range(0, 12):

    header = bimestrales[i+1:] + bimestrales[:i+1]

    aux = pd.DataFrame(columns=header)

    contador = 0

    for j in range(0, len(X)-1):
    
        valor = np.concatenate((X[bimestrales[i+1:]].iloc[j-1], X[bimestrales[:i+1]].iloc[j]))
    
        aux.loc[contador] = valor
    
        contador += 1

    mei.append(aux)

#Getting the SPIs data.
dir = '/home/oscar_amarilla/Pasantia/SPI_81-10/'

#Getting the list of files in the directory.
archivos = os.listdir(dir)

#Here the indexes of each month will be storaged.
spi_indexes = []

aux = pd.read_csv('SPI_81-10/' + archivos[1])

for mes in range(1,13):
    
    spi_indexes.append(aux.index[aux['Mes'] == mes].to_list())

#Getting the header of the SPI file. It contains the SPI type.
header = list(aux)[2:]

#Months of the year.
meses = ['E','F','M','A','M','J','J','A','S','O','N','D']

for archivo in archivos:

#In this list all the SPI data will be stored.
    dataset =[]

#Reading the file.
    Y_data = pd.read_csv('SPI_81-10/' + archivo)

    for spi_i in header:

        aux = pd.DataFrame()

        for mes in range(0,12):

            data = Y_data.iloc[spi_indexes[mes]][spi_i]

            aux[meses[mes]] =data.reset_index(drop=True) 

        dataset.append(aux)

#All the SPI of a station will bw storaged in a list with the same name.
    estacion = archivo.split("_")[0]

    vars()[estacion] = dataset

#A list of dataframes containing the coeffients of the regressions.
    regr_dataset = []

#Going through spi indexes
    for spi_i in range(12):

#Inintializing a dataframe that will contatin the i-th SPI of each month.        
        regr_dataframe = pd.DataFrame()

        for mes in range(12):

            Y = dataset[spi_i][meses[mes]]

            X = mei[mes]

            X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.3, random_state=0)

            lr = LinearRegression()

            lr.fit(X_train, Y_train)

            Y_predic = lr.predict(X_test)

            r2 = r2_score(Y_test, Y_predic)

            datos_regr = {'a_1': lr.coef_[0], 'a_2': lr.coef_[1], 'a_3': lr.coef_[2], 'a_4': lr.coef_[3], 'a_5': lr.coef_[4], 'a_6': lr.coef_[5], 'a_7': lr.coef_[6], 'a_8': lr.coef_[7], 'a_9': lr.coef_[8], 'a_10': lr.coef_[9], 'a_11': lr.coef_[10], 'a_12': lr.coef_[11], 'b': lr.intercept_, 'r2':r2}
            
            regr_dataframe = regr_dataframe.append(datos_regr, ignore_index=True)

        regr_dataset.append(regr_dataframe)

    estacion = estacion + '_Regr'

    vars()[estacion] = regr_dataset








