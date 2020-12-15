# Se importan las librerias necesarias
import pandas as pd
from epiweeks import Week, date
from sklearn import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt
import string

def comparacion_contaminantes_egresos(contaminante:str, año:str, bolnombrescies:bool, nombrescies:list, numciesindividuales:int, numciesagrupadas:int) -> None:

    '''
    Esta función recibe como parametros el contaminante y el año,
    dichas variables se guardan en una variable de tipo str,
    y la función genera una gráfica donde se ve la comparación entre
    la evolución del contaminante proporcionado y las CIEs
    durante el año proporcionado.
    Las gráficas generadas se guardan en formato .jpg en la PC en la carpeta donde se encuentra
    la función ejecutada.
    '''

    # Se declaran las columnas a extraer de la base de datos
    columns = ['timestamp', contaminante]
    # Se lee el archivo y los datos recuperados se guardan en 'dataframecontaminante'
    dataframecontaminante = pd.read_csv('filled.csv', usecols=columns).dropna()
    # Se convierten los strings a objeto datetime
    strfdt = '%d-%b-%y %H'
    dataframecontaminante['timestamp'] = pd.to_datetime(dataframecontaminante['timestamp'], errors = 'coerce', format=strfdt)
    # Se eliminan los espacios vacios
    dataframecontaminante = dataframecontaminante.dropna()
    # Se acomoda el indice empezando en 0 con un incremento de 1
    dataframecontaminante = dataframecontaminante.reset_index(drop=True)
    
    # Los datos de la columna 'timestamp' se vuelven a convertir a strings
    dataframecontaminante['timestamp'] = dataframecontaminante['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H'))
    # Se guardan los datos de 'año' en 'dataframecontaminanteaño'
    dataframecontaminanteaño = dataframecontaminante.loc[dataframecontaminante['timestamp'].str.startswith(año)]
    dataframecontaminanteaño = dataframecontaminanteaño.reset_index(drop=True)

    # Se convierten los strings a objeto datetime
    strfdt = '%Y-%m-%d %H'
    dataframecontaminanteaño['timestamp'] = pd.to_datetime(dataframecontaminanteaño['timestamp'], errors = 'coerce', format=strfdt)

    # Se agrega una nueva columna con los numeros de semana
    dataframecontaminanteaño['sem'] = dataframecontaminanteaño['timestamp'].apply(lambda x: date(x.year, x.month, x.day))
    dataframecontaminanteaño['sem'] = dataframecontaminanteaño['sem'].apply(lambda x: Week.fromdate(x))
    dataframecontaminanteaño['sem'] = dataframecontaminanteaño['sem'].apply(lambda x: x.week)

    # Se cargan los datos de la base de datos 'EGRESO_'año'.csv'
    colums = ['EGRESO', 'DIAG_INI']
    csvegresos = 'EGRESO_' + año + '.csv'

    if (año=='2010' or año=='2011' or año=='2012' or año=='2013'):
        dataframeegresosaño = pd.read_csv(csvegresos, usecols=colums).dropna()
        # Se convierten los string a objetos datetime en 'dataframe'
        strfdtoriginal = '%d/%m/%Y'
    elif año=='2014':
        dataframeegresosaño = pd.read_csv(csvegresos, usecols=colums).dropna()
        # Se convierten los string a objetos datetime en 'dataframe'
        strfdtoriginal = '%Y-%m-%d %H:%M:%S'
    elif año=='2015':
        dataframeegresosaño = pd.read_csv(csvegresos, usecols=colums, nrows=2500000).dropna()
        # Se convierten los string a objetos datetime en 'dataframe'
        strfdtoriginal = '%Y-%m-%d %H:%M:%S'
    elif año=='2016':
        dataframeegresosaño = pd.read_csv(csvegresos, usecols=colums).dropna()
        # Se convierten los string a objetos datetime en 'dataframe'
        strfdtoriginal = '%m/%d/%Y %H:%M'
    elif año=='2017':
        dataframeegresosaño = pd.read_csv(csvegresos, sep='|', usecols=colums, nrows=1500000).dropna()
        # Se convierten los string a objetos datetime en 'dataframe'
        strfdtoriginal = '%Y-%m-%d %H:%M:%S'
    elif año=='2018':
        dataframeegresosaño = pd.read_csv(csvegresos, usecols=colums, nrows=1000000).dropna()
        # Se convierten los string a objetos datetime en 'dataframe'
        strfdtoriginal = '%Y-%m-%d %H:%M:%S.000'
    
    dataframeegresosaño['EGRESO'] = pd.to_datetime(dataframeegresosaño['EGRESO'], errors = 'coerce', format=strfdtoriginal)
    dataframeegresosaño = dataframeegresosaño.dropna()
    dataframeegresosaño = dataframeegresosaño.reset_index(drop=True)
    numaño = int(año) 
    # Se agrega una columna con los numeros de semana
    dataframeegresosaño['sem'] = dataframeegresosaño['EGRESO'].apply(lambda x: date(x.year, x.month, x.day))
    dataframeegresosaño['sem'] = dataframeegresosaño['sem'].apply(lambda x: Week.fromdate(x))
    dataframeegresosaño['sem'] = dataframeegresosaño['sem'].apply(lambda x: x.week)
    dataframeegresosaño['EGRESO'] = dataframeegresosaño['EGRESO'].apply(lambda x: x if(x.year==numaño) else pd.NaT)   
    dataframeegresosaño = dataframeegresosaño.dropna()
    dataframeegresosaño = dataframeegresosaño.reset_index(drop=True)

    # Se forma el nuevo dataframe 'semanas' con el numero de semana del año y la cantidad de egresos en cada semana
    semanas = dataframeegresosaño['sem'].value_counts()
    semanas = semanas.sort_index()

    # Se pasa a un nuevo dataframe
    dataframesemanascontaminanteaño = pd.DataFrame()
    dataframesemanascontaminanteaño['sem'] = semanas.index
    dataframesemanascontaminanteaño[contaminante] = ''
    n = len(semanas.index)
    for i in range (n):
        registrossem = dataframecontaminanteaño.loc[dataframecontaminanteaño['sem'] == i+1]
        # Se calcula el promedio por semana de las lecturas del contaminante registradas 
        promediocontaminanteañosem = registrossem[contaminante].mean()
        dataframesemanascontaminanteaño[contaminante][i] = promediocontaminanteañosem
    
    # Se crea el dataframe 'diagnosticosaño' con los nombres de los diferentes diagnosticos sin repeticion
    diagnosticosaño = dataframeegresosaño['DIAG_INI'].value_counts()
    # Se ordena del diagnostico con mayor numero de egresos al diagnostico con menor numero de egresos
    diagnosticosaño = diagnosticosaño.sort_values(ascending = False)
    # Se crea el dataframe 'cies2010' con los nombres de los diagnosticos, los numeros de las semanas, 
    # y la cantidad de diagnosticos de dicha enfermedad en cada semana
    ciesaño = dataframeegresosaño.groupby(['DIAG_INI', 'sem']).count()
    s_scaler = preprocessing.StandardScaler()
    # Se crea la lista 'ind' con los indices de las semanas empezando con el 1
    ind = []
    n = len(semanas.index)
    for i in range (n):
        ind.append(i+1)
        
    # Proceso al que se entra si se proporcionaron los nombres de las CIEs
    if nombrescies:
        ciesindividuales=[]
        ciesagrupadas=[]
        for name in nombrescies:
            if(len(name)>1):
                ciesindividuales.append(name)
            elif(len(name)==1):
                ciesagrupadas.append(name)
                
        # Proceso de generación de las figuras
        print('\n' + año)
        # Generación de las gráficas para las CIEs individuales
        for name in ciesindividuales:
            dataframegraficoañocontaminantecie = pd.DataFrame()
            dataframegraficoañocontaminantecie[contaminante] = dataframesemanascontaminanteaño[contaminante]
            dataframegraficoañocontaminantecie = dataframegraficoañocontaminantecie.reindex(ind)
            dataframegraficoañocontaminantecie[name] = ciesaño['EGRESO'][name]
            for i in range (n):
                dataframegraficoañocontaminantecie[contaminante][i+1] = dataframesemanascontaminanteaño[contaminante][i]
            col_names = [contaminante, name]    
            df_s = s_scaler.fit_transform(dataframegraficoañocontaminantecie)
            df_s = pd.DataFrame(df_s, columns=col_names)
            fig, ax = plt.subplots(ncols=1, figsize=(20, 8))
            print('\n' + col_names[0] + ' & ' + col_names[1])
            ax.set_title('Contaminante ' + col_names[0] + ' & CIE ' + col_names[1])
            ax.set_xlabel('Semana del año ' + año)
            sns.kdeplot(df_s[col_names[0]])
            sns.kdeplot(df_s[col_names[1]])
            plt.savefig(col_names[0] + '&' + col_names[1] + '_' + año + '.jpg', format='jpg')
            plt.show()
        # Generación de las gráficas para las CIEs agrupadas
        for nameg in ciesagrupadas:
            dataframegraficoañocontaminantecie = pd.DataFrame()
            dataframegraficoañocontaminantecie[contaminante] = dataframesemanascontaminanteaño[contaminante]
            dataframegraficoañocontaminantecie = dataframegraficoañocontaminantecie.reindex(ind)
            ciesagrupadas = dataframeegresosaño.loc[dataframeegresosaño['DIAG_INI'].str.startswith(nameg)]
            ciesagrupadas = ciesagrupadas['sem'].value_counts()
            dataframegraficoañocontaminantecie[nameg] = ciesagrupadas
            for i in range (n):
                dataframegraficoañocontaminantecie[contaminante][i+1] = dataframesemanascontaminanteaño[contaminante][i]
            col_names = [contaminante, nameg]
            df_s = s_scaler.fit_transform(dataframegraficoañocontaminantecie)
            df_s = pd.DataFrame(df_s, columns=col_names)
            fig, ax = plt.subplots(ncols=1, figsize=(20, 8))
            print('\n' + col_names[0] + ' & ' + col_names[1])
            ax.set_title('Contaminante ' + col_names[0] + ' & CIE ' + col_names[1])
            ax.set_xlabel('Semana del año ' + año)
            sns.kdeplot(df_s[col_names[0]])
            sns.kdeplot(df_s[col_names[1]])
            plt.savefig(col_names[0] + '&' + col_names[1] + '_' + año + '.jpg', format='jpg')
            plt.show()
            
    # Proceso al que se entra si no se proporcionaron los nombres de las CIEs
    else:
        # Se guardan las letras del abdcedario en mayusculas en la lista 'letras' para la agrupación de CIEs
        letras = []
        for letra in string.ascii_uppercase:
            letras.append(str(letra))
        # Se inicia un contador para controlar la cantidad de graficos a generar
        cont = 0
        mindividuales = numciesindividuales
        magrupadas = numciesagrupadas
        
        # Proceso de generación de las figuras
        print('\n' + año)
        # Se generan las gráficas para las CIEs individuales
        for name in diagnosticosaño.index:
            if cont < mindividuales:
                dataframegraficoañocontaminantecie = pd.DataFrame()
                dataframegraficoañocontaminantecie[contaminante] = dataframesemanascontaminanteaño[contaminante]
                dataframegraficoañocontaminantecie = dataframegraficoañocontaminantecie.reindex(ind)
                dataframegraficoañocontaminantecie[name] = ciesaño['EGRESO'][name]
                for i in range (n):
                    dataframegraficoañocontaminantecie[contaminante][i+1] = dataframesemanascontaminanteaño[contaminante][i]
                col_names = [contaminante, name]    
                df_s = s_scaler.fit_transform(dataframegraficoañocontaminantecie)
                df_s = pd.DataFrame(df_s, columns=col_names)
                fig, ax = plt.subplots(ncols=1, figsize=(20, 8))
                print('\n' + col_names[0] + ' & ' + col_names[1])
                ax.set_title('Contaminante ' + col_names[0] + ' & CIE ' + col_names[1])
                ax.set_xlabel('Semana del año ' + año)
                sns.kdeplot(df_s[col_names[0]])
                sns.kdeplot(df_s[col_names[1]])
                plt.savefig(col_names[0] + '&' + col_names[1] + '_' + año + '.jpg', format='jpg')
                plt.show()
            cont = cont+1
        # Se reinicia el contador para las CIEs agrupadas
        cont = 0
        # Se generan las gráficas para las CIEs agrupadas
        for name in diagnosticosaño.index:
            if cont < magrupadas:
                dataframegraficoañocontaminantecie = pd.DataFrame()
                dataframegraficoañocontaminantecie[contaminante] = dataframesemanascontaminanteaño[contaminante]
                dataframegraficoañocontaminantecie = dataframegraficoañocontaminantecie.reindex(ind)
                nameg =  letras[cont]
                ciesagrupadas = dataframeegresosaño.loc[dataframeegresosaño['DIAG_INI'].str.startswith(nameg)]
                ciesagrupadas = ciesagrupadas['sem'].value_counts()
                dataframegraficoañocontaminantecie[nameg] = ciesagrupadas
                for i in range (n):
                    dataframegraficoañocontaminantecie[contaminante][i+1] = dataframesemanascontaminanteaño[contaminante][i]
                col_names = [contaminante, nameg]
                df_s = s_scaler.fit_transform(dataframegraficoañocontaminantecie)
                df_s = pd.DataFrame(df_s, columns=col_names)
                fig, ax = plt.subplots(ncols=1, figsize=(20, 8))
                print('\n' + col_names[0] + ' & ' + col_names[1])
                ax.set_title('Contaminante ' + col_names[0] + ' & CIE ' + col_names[1])
                ax.set_xlabel('Semana del año ' + año)
                sns.kdeplot(df_s[col_names[0]])
                sns.kdeplot(df_s[col_names[1]])
                plt.savefig(col_names[0] + '&' + col_names[1] + '_' + año + '.jpg', format='jpg')
                plt.show()
            cont = cont+1                    

# comparacion_contaminantes_egresos('PM10', '2010', True, ['O', 'O809'], 0, 0)
