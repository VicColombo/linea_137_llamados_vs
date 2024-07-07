
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.manifold import MDS
#from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os

###########################################################################3


# 1 contar los si y los no, devolver "si" en el caso de que haya algún "si" en la selección

def hay_si(x):
    for s in x:
        if s == 'SI':
            return 'SI'
    return 'NO'


# 2 pedir los nombre de columnas a agrupar, chequear que existan en el df y si no volver a pedir.
# Devolver la lista de columnas a agrupar

def pedir_columnas(dataframe):
    faltantes = []
    correctas = []
    erroneas = []

    lista_columnas_agrupar = [s.strip() for s in (input ("Ingresá las columnas a agrupar en minúscula y separadas por coma: ").split(','))]

    for c in lista_columnas_agrupar: 

            # si existe, imprimo y pongo ok

            if c in list(dataframe):
                print(c, 'ok\n')
                correctas.append(c)

            # si no existe, imprimo que no existe
            elif c=='':
                print('No ingresaste ninguna columna')
                pedir_columnas(dataframe)
            
            else: # c not in list(dataframe) or 
                print(c, 'no está en el dataframe\n')

                erroneas.append(c)


    print('columnas erróneas: ',erroneas)
    print('columnas correctas: ',correctas)
    
    if len(erroneas)==0:
        return correctas
    else:
        return pedir_columnas(dataframe)





# 3 armar el agrupador pidiendo los nombres de columnas a agrupar, el nombre de la nueva col que las agrupa
# y devolviendo el df con la nueva columnas con los valores correctos

def seteo_agrupador(dataframe,columnas_agrupar, nueva_col_agrup):
    
    # estos pasos crean columnas_agrupar y nueva_col_group por input
    # 1
    
    #columnas_agrupar = pedir_columnas(dataframe)
    
    
    #nueva_col_agrup = input('\nIngresá el nombre de la nueva variable agrupadora para las columnas: ')
   
    # 2
    
    dataframe[nueva_col_agrup] = dataframe[columnas_agrupar].apply(hay_si, axis=1)
    
    return(dataframe)



####################################################################
palette_sino ={"SI": "#1E88E5", "NO": "#FFC107", "NS/NC": "#D81B60"}

def mapData(dist_matrix, X, y, metric, title, image_path,image_name):
    mds = MDS(metric=metric, dissimilarity='precomputed', random_state=0, normalized_stress=True) 
    # Get the embeddings
    pts = mds.fit_transform(dist_matrix)
    # Plot the embedding, colored according to the class of the points
    ax = plt.subplots(figsize=(15,10))
 
    # USAR AX PARA AGREGAR EL TEXTO LUEGO
    # pts[:, 0] pts in column 1 (first dimension),y=pts[:, 1] pts in column 2 (second dimension) 

    ax = sns.scatterplot(x=pts[:, 0], y=pts[:, 1], hue=y, palette=(palette_sino)) #hue_order=['NO', 'SI','NS/NC'])

    plt.title(title)
    plt.text(1.0121, 0.85, ('Stress: ' + str(round(mds.stress_,2))), fontsize=13, bbox = {'facecolor': 'white', 'alpha': 1.0, 'pad': 5},transform = ax.transAxes)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.savefig(os.path.join(image_path, image_name))
    #plt.show()



############################################################################

# funciones para construcción de variables

# reducción llamado provincia
    
lista_norte=['Jujuy', 'Salta', 'Tucumán', 'Catamarca', 'La Rioja', 'Santiago del Estero','Formosa', 'Chaco', 'Corrientes', 'Misiones']
lista_centro = ['San Luis', 'San Juan', 'Mendoza','Córdoba', 'Entre Ríos','La Pampa', 'Santa Fe']
lista_patagonia=['Chubut', 'Neuquén', 'Río Negro', 'Santa Cruz', 'Tierra del Fuego']

def provincias_red(x):
    if x == 'NS/NC':
        return x
    elif x == 'CABA':
        return x
    elif x=='Buenos Aires':
        return x
    elif x in lista_norte:
        return 'Región Norte'
    elif x in lista_centro:
        return 'Región Central'
    elif x in lista_patagonia:
        return 'Región Patagónica'
    else:
        return 'N/A'

# agresor conocido fam, conocido no fam

lista_familiar = ['Pareja de la víctima', 'Ex pareja de la víctima', 'Abuela', 'Abuelo', 'Hermana', 'Hermano', 'Madrastra', 'Madre', 'Otro pariente', 'Padrastro', 'Padre', 'Tío' ]
lista_no_familiar = ['Desconocido', 'Conocido no familiar (Amigo, vecino, entre otros)']


def fam_nofam (x):
    if x in lista_familiar:
        return 'Familiar'
    elif x in lista_no_familiar:
        return 'Conocido No Familiar'
    elif x == 'NS/NC':
        return x
    else:
        return 'N/A'

    

# genero agresor

# género dell agresor
lista_hombre = [ 'Abuelo', 'Hermano', 'Padrastro', 'Padre', 'Tío' ]
lista_mujer = [ 'Abuela','Hermana','Madrastra', 'Madre']
lista_no_especificado = ['Ex pareja de la víctima','Pareja de la víctima', 
                                   'Otro pariente','Conocido no familiar (Amigo, vecino, entre otros)', 'Desconocido']

def genero_agresor (x):
    if x in lista_mujer:
        return 'Femenino'
    elif x in lista_hombre:
        return 'Masculino'
    elif x in lista_no_especificado:
        return 'No especificado'
    elif x == 'NS/NC':
        return x
    else:
        return 'N/A'


#  conoce victima agresor

lista_conocido_familiar = ['Abuela', 'Abuelo','Pareja de la víctima', 'Ex pareja de la víctima', 'Hermana', 'Hermano', 'Madrastra', 'Madre', 'Otro pariente', 'Padrastro', 'Padre', 'Tío' ]
lista_no_declarado = ['NS/NC']

def conocido_no_conocido (x):
    if x in lista_conocido_familiar:
        return 'Agresor conocido (familiar))'
    elif x == 'Desconocido':
        return x
    elif x in lista_no_declarado:
        return 'NS/NC'
    elif x == 'Conocido no familiar (Amigo, vecino, entre otros)':
        return x
    else:
        return 'N/A'



# reduccion vinculo llamante

lista_institucion = ['Hospital', 'Comisaría', 'Escuela', 'Defensoría', 'Otra Institución', 'Otra institución']
lista_conocide = ['Madre', 'Vecina/o', 'Padre', 'Familiar', 'Otro conocido', 'Abuela/o','Hermana/o']


def tipo_vinculo_llamante (x):
    if x in lista_institucion:
        return 'Institución'
    elif x in lista_conocide:
        return 'Conocido (fam/no fam)'
    elif x == 'NS/NC':
        return x
    elif x == 'Víctima':
        return x
    elif x == 'Agresor/a':
        return x
    else:
        return 'N/A'

# reducción hecho lugar
lista_otro = ['Residencia turística','Otro','Obra en construcción', 'Taxi','Albergue transitorio','Automóvil','Comercio','Ámbito educativo','Vivienda de un familiar' ]
lista_espacio_publico = ['Subterráneo/Tren/Colectivo','Plaza','Descampado','Calle']


def tipo_hecho_lugar (x):
    if x in lista_otro:
        return 'Otro'
    elif x in lista_espacio_publico:
        return 'Espacio público'
    elif x == 'NS/NC':
        return x
    elif x == 'Vivienda de la Víctima':
        return x
    elif x == 'Vivienda del Agresor':
        return x
    elif x == 'Redes Sociales':
          return x
    else:
        return 'N/A'


def categoria_edad (x):
    if (x >= 0) and (x <= 11) :
        return 'Niñez'
    elif (x >= 12) and (x <=18):
        return 'Adolescencia'
    elif (x >= 19) and (x <=30):
        return 'Juventud'
    elif (x>=31) and (x<=65) :
        return 'Vejez'
    elif x>=66:
        return 'Vejez mayor'
    else:
        return 'NS/NC'