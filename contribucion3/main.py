# Se importan la librerías necesarias
from argparse import ArgumentParser
from comparacion_contaminantes_egresos import comparacion_contaminantes_egresos

# Función cli
def cli(args: list, bolnombrescies: bool):
    '''
    En está función se crea el CLI que ayudará a interactuar con la función generadora de gráficas
    comparacion_contaminantes_egresos.
    Recibe como parámetros una lista con los argumentos necesarios para llamar a la función generadora de gráficas
    y una variable boleana que indica si el usuario determinó que CIEs desea generar o si desea que las seleccione el programa.
    '''
    # Se declara el objeto 'parser' el cual servira para realizar el CLI
    parser = ArgumentParser(
        description= '''Bienvenido.
    Esta app genera una gráfica donde se ve la comparación entre la evolución del contaminante proporcionando y las CIEs durante el año proporcionado.
    Se requiere tener tener en la carpeta una base de datos llamada "EGRESO_"año".csv', donde "año" es el año proporcionado.
    También se requier tener la base de datos "filled.csv".
    ''')
    # Se declara el argumento contaminante
	contaminante = parser.add_argument(
        'contaminante',
        choices='CO,NO,NO2,NOX,O3,PM10,PM2_5'.split(','),
        type = str,
        help='De las opciones mostradas, se debe ingresar el contaminante del cuál se desean generar gráficas.'
        )
	# Se declara el argumento año
    año = parser.add_argument(
        'año',
        choices='2010,2011,2012,2013,2014,2015,2016,2017,2018'.split(','),
        type = str,
        help='De los años mostrados, se debe ingresar de que año se desean generar gráficas.'
        )
	# Se declaran los argumentos necesarios para el caso de que el usuario quiera teclear los nombres de las cies
    if bolnombrescies:
        cies = parser.add_argument(
            'cies',
            type = list,
            help='''Se deben ingresar las CIEs de las cuales se desean generar gráficas.
                    Se puede ingresar nombres de la CIEs (ejemplo: O809)
                    y letras de la A a la Z (ejemplo: O).'''
            )
		# Se leen los argumentos tecleados en consola
        arguments = parser.parse_args(args)
		# Se inicia la función comparacion_contaminantes_egresos que genera las gráficas
        comparacion_contaminantes_egresos(arguments.contaminante, arguments.año, bolnombrescies, arguments.cies, 0, 0)
	# Se declaran los argumentos necesarios para el caso de que el usuario no quiera teclear los nombres de las cies
    else:
        numciesindividuales = parser.add_argument(
            'numero_cies_individuales',
            type = int,
            help='''Se debe colocar el numero de CIEs individuales de las cuales se desea
                    generar gráficas. Las CIEs están ordenadas de la que estuvo presente
                    en la mayor cantidad de egresos a la que estuvo en la menor.'''
            )
        numciesagrupadas = parser.add_argument(
            'numero_cies_agrupadas',
            type = int,
            help='''Se debe colocar el numero de CIEs agrupadas por la primera letra de su nombre
                         de las cuales se desea generar gráficas. Se ordenan de la A a la Z.'''
            )
		# Se leen los argumentos tecleados en consola
        arguments = parser.parse_args(args)
		# Se inicia la función comparacion_contaminantes_egresos que genera las gráficas
        comparacion_contaminantes_egresos(arguments.contaminante, arguments.año, bolnombrescies, None, arguments.numero_cies_agrupadas, arguments.numero_cies_agrupadas)


# Inicio del programa principal
print('''\n Bienvenido.
Esta app genera una gráfica donde se ve la comparación entre la evolución del contaminante proporcionando y las CIEs durante el año proporcionado.
Se requiere tener tener en la carpeta una base de datos llamada "EGRESO_"año"".csv', donde "año" es el año proporcionado.
También se requier tener la base de datos "filled.csv"''')
# Se le pregunta al usuario si desea iniciar el programa u obtener más información
ayuda = input('\n¿Deseas obtener más información?(S/N)\nIngresa N para continuar con la generación de gráficas o S para obtener más información: ')
# Se inicializa la lista 'parametros' en la cual se guardaran los parametros tecleados en consola
parametros = []
# Se inicializa la variable que guarda si el usuario desea teclear los nombres de las cies
bol = False
# Proceso que se ejecuta si el usuario no indicó que quería más información
if (ayuda=='N'):
	# Se le pide al usuario ingresar el contaminante y se agrega a la lista de parametros
    contaminante = input('\nIngresa el contaminante (Ejemplo: PM10): ')
    # Se guarda en parametros el contaminante
	parametros.append(contaminante)
    # Se le pide al usuario ingresar el año y se agrega a la lista de parametros
	año = int(input('\nIngresa con número el año, este debe ser entre el 2010 y 2018 (Ejemplo: 2010): '))
    año = str(año)
	# Se guarda en parametros el año
    parametros.append(año)
    # Se le pide al usuario ingresar si desea teclear los nombres de las CIES o que los seleccione el programa
	bolnombrescies = input('\n¿Deseas ingresar los nombres de las CIEs?(S/N)\nIngresa S si deseas escribir los nombres de las CIEs o N si quieres que las seleccione el programa: ')
    # Proceso al que se entra si el usuario desea ingresar los nombres de las CIES
	if(bolnombrescies=='S'):
		# Se guarda en la variable booleana bol la selección anterior del usuario
		bol = True
        # Se declara la lista 'nombrescies' donde se guardan los nombres de las CIES tecleadas por el usuario
		nombrescies=[]
        # Se le pide al usuario ingresar el numero de CIEs que desea teclear
		n = int(input('Teclea con número la cantidad de CIEs que deseas ingresar (Ejemplo: 5): '))
        # Se le pide al usuario ingresar los nombres de las CIES
		for i in range(n):
			nombre = input('Ingresa el nombre de la CIE ' + str(i+1) + ': ')
            nombrescies.append(nombre)
        # Se guarda en parametros los nombres de las cies tecleadas por el usuario
		parametros.append(nombrescies)
	# Proceso al que se entra si el usuario no desea ingresar los nombres de las CIES
    else:
        # Se le pide al usuario ingresar el numero de CIEs individuales que desea que seleccione el programa
		nciesindividuales = int(input('Teclea con n-úmero la cantidad de gráficas de CIEs individuales que deseas que se generen (Ejemplo: 5): '))
        # Se guarda en parametros el numero de cies individuales
		nciesindividuales = str(nciesindividuales)
        parametros.append(nciesindividuales)
        # Se le pide al usuario ingresar el numero de CIEs agrupadas que desea que seleccione el programa
		nciesagrupadas = int(input('Teclea con número la cantidad de gráficas de CIEs agrupadas que deseas que se generen (Ejemplo: 5): '))
		# Se guarda en parametros el numero de cies agrupadas
        nciesagrupadas = str(nciesagrupadas)
else:
	# Se le pregunta al usuario de que modalidad del programa desea obtener mas información
	bolnombrescies = input('''\nEsta app tiene dos modalidades. 
	¿Deseas obtener más información de la modalidad donde se ingresan los nombres de las CIEs?(S/N)
	Ingresa S si deseas obtener más información sobre la modalidad donde se deben escribir los nombres de las CIEs 
	o N si quieres obtener información de la modalidad donde las selecciona el programa: ''')
	# Se guarda en la variable booleana 'bol' la eleccion anterior del usuario
    if(bolnombrescies=='S'):
        bol = True
    # Se guarda en parametros el comando necesario para que se imprima en pantalla más información del programa
	parametros.append('--help')

# Se ejecuta la función cli la cual sirve para el funcionamiento del programa
cli(parametros, bol)
