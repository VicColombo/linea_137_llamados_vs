# librerías

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import gower
from sklearn.manifold import MDS

from matplotlib import pyplot as plt
import seaborn as sns         
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from herramientas import seteo_agrupador, mapData


data_2017 = pd.read_csv('/home/magickmichelle/Documentos/maestria2020_2021/taller_tesis/137/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2017.csv',  engine= 'python')
data_2018 = pd.read_csv('/home/magickmichelle/Documentos/maestria2020_2021/taller_tesis/137/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2018.csv', engine= 'python')
data_2019 =pd.read_csv('/home/magickmichelle/Documentos/maestria2020_2021/taller_tesis/137/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2019.csv', encoding='latin-1')
data_2020 =pd.read_csv('/home/magickmichelle/Documentos/maestria2020_2021/taller_tesis/137/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2020.csv', engine= 'python')
data_2021 =pd.read_csv('/home/magickmichelle/Documentos/maestria2020_2021/taller_tesis/137/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2021.csv', engine= 'python')


## quitar caso_id

data_2019.drop('caso_id',
  axis='columns', inplace=True)
data_2020.drop('caso_id',
  axis='columns', inplace=True)
data_2021.drop('caso_id',
  axis='columns', inplace=True)


# cambios de nombres de columnas

''' 2017 2018 llamante_quien_llama == llamante_vinculo

2017 2018 2019 llamado_provincia_indec_id == llamado_provincia_id'''


data_2017.rename(columns = {'llamante_quien_llama': 'llamante_vinculo', 'llamado_provincia_indec_id': 'llamado_provincia_id'}, inplace = True)
data_2018.rename(columns = {'llamante_quien_llama': 'llamante_vinculo', 'llamado_provincia_indec_id': 'llamado_provincia_id'}, inplace = True)
data_2019.rename(columns = {'llamado_provincia_indec_id': 'llamado_provincia_id'}, inplace = True)


# concateno

llamados = pd.concat([data_2017, data_2018, data_2019, data_2020, data_2021])


# re ordenar columnas

llamados = llamados[['llamado_fecha_hora',  
                                   'llamado_provincia', 
                                   'llamado_provincia_id',
                                   'llamante_edad',
                                   'llamante_genero', 
                                   'llamante_vinculo', 
                                   'caso_judicializado',
                                   'hecho_lugar', 
                                   'victima_a_resguardo', 
                                   'victima_edad', 
                                   'victima_genero',
       'victima_nacionalidad', 'victima_vinculo_agresor',
       'victima_discapacidad', 'victima_convive_agresor',
       'vs_violacion_via_vaginal', 'vs_violacion_via_anal',
       'vs_violacion_via_oral', 'vs_tentativa_violacion',
       'vs_tocamiento_sexual', 'vs_intento_tocamiento',
       'vs_Intento_violación_tercera_persona', 'vs_grooming',
       'vs_exhibicionismo', 'vs_amenazas_verbales_contenido_sexual',
       'vs_explotacion_sexual', 'vs_explotacion_sexual_comercial',
       'vs_explotacion_sexual_viajes_turismo',
       'vs_sospecha_trata_personas_fines_sexuales',
       'vs_existencia_facilitador_corrupcion_nnya',
       'vs_obligacion_sacarse_fotos_pornograficas',
       'vs_eyaculacion_partes_cuerpo', 'vs_acoso_sexual',
       'vs_iniciacion_sexual_forzada_inducida',
       'vs_otra_forma_violencia_sexual', 'vs_no_sabe_no_contesta',
       'ofv_sentimiento_amenaza', 'ofv_amenaza_explicita',
       'ofv_violencia_fisica', 'ofv_intento_ahorcar', 'ofv_intento_quemar',
       'ofv_intento_ahogar', 'ofv_amenaza_muerte',
       'ofv_uso_sustancias_psicoactivas', 'ofv_intento_privacion_libertad',
       'ofv_privacion_libertad', 'ofv_uso_arma_blanca', 'ofv_uso_arma_fuego',
       'ofv_enganio_seduccion', 'ofv_intento_matar',
       'ofv_uso_animal_victimizar', 'ofv_grooming', 'ofv_otra_forma_violencia',
       'ofv_no_sabe_no_contesta']]


# valores numéricos: type integer
'''llamante edad as integer y sin datos = NA
victima edad as integer y sin datos = NA
provincia id as integer y sin datos = NA
'''

llamados['victima_edad'] = pd.to_numeric(llamados['victima_edad'], errors='coerce').convert_dtypes()
llamados['llamante_edad'] = pd.to_numeric(llamados['llamante_edad'], errors='coerce').convert_dtypes() 


# Normalizaciones de errores en carga de datos

'''ver todas las cat: llamado_provincia, llamante_vinculo, hecho_lugar, victima_nacionalidad, victima_vinculo_agresor

en todo el dataset Ns/Nc = NS/NC

llamante_edad Sin dato pasar a N/A

llamante género: Masculino = Masculino Trans = Transgénero

llamante vinculo Vecino = Vecina/o ' Madre' = 'Madre'

caso judicializado 'NS/NS' = 'NS/NC' 'Sin datos' = 'NS/NC'

victima_a_resguardo No = NO

victima_genero Trans = Transgénero

victima_vinculo_agresor 'Pareja de la vícitma' = 'Pareja de la víctima' 'Pareja ' = 'Pareja de la víctima' Ex pareja = Ex pareja de la víctima

hecho_lugar Otro(Especificar en observaciones) = Otro

llamado_provincia: 'Ciudad Autónoma de Buenos Aires' = 'CABA'

llamado_provincia: 'Santa Fé' = 'Santa Fe' '''



llamados.llamante_genero.replace({' Masculino':'Masculino', 'Trans':'Transgénero'}, inplace = True)
llamados.llamante_vinculo.replace({'Vecino': 'Vecina/o', ' Madre':'Madre'}, inplace = True)
llamados.victima_a_resguardo.replace({'No': 'NO'}, inplace = True)
llamados.victima_genero.replace({'Trans': 'Transgénero'}, inplace = True)
llamados.victima_vinculo_agresor.replace({'Pareja de la vícitma': 'Pareja de la víctima', 'Pareja ': 'Pareja de la víctima','Pareja': 'Pareja de la víctima', 'Ex pareja': 'Ex pareja de la víctima'}, inplace = True)
llamados.hecho_lugar.replace({'Otro(Especificar en observaciones)': 'Otro' }, inplace = True)
llamados.caso_judicializado.replace({'NS/NS': 'NS/NC', 'Sin datos':'NS/NC'}, inplace = True)
llamados.llamado_provincia.replace({'Ciudad Autónoma de Buenos Aires': 'CABA'}, inplace = True)
llamados.llamado_provincia.replace({'Santa Fé': 'Santa Fe'}, inplace = True)
llamados.replace('Ns/Nc', 'NS/NC', inplace=True)


# victima_genero N/A -> NS/NC
llamados['victima_genero'] = llamados['victima_genero'].fillna('NS/NC')

# Outliers de edad considerados error de carga

llamados['llamante_edad'].loc[(llamados['llamante_edad'] >= 100)] = None
llamados['llamante_edad'].loc[(llamados['llamante_edad'] < 3)] = None

llamados['victima_edad'].loc[(llamados['victima_edad'] >= 103)] = None
llamados['victima_edad'].loc[(llamados['victima_edad'] < 0)] = None


# saco llamado_provincia_id
llamados.drop('llamado_provincia_id',
  axis='columns', inplace=True)

# funciones para construcción de variables

# agresor_fam_no_fam

lista_familiar = ['Abuela', 'Abuelo', 'Hermana', 'Hermano', 'Madrastra', 'Madre', 'Otro pariente', 'Padrastro', 'Padre', 'Tío' ]
lista_no_familiar = ['Desconocido', 'Conocido no familiar (Amigo, vecino, entre otros)']
lista_pareja_exp = ['Pareja de la víctima', 'Ex pareja de la víctima']

def columna_fam_nofam (x):
    if x in lista_familiar:
        return 'Familiar'
    elif x in lista_no_familiar:
        return 'No Familiar'
    elif x in lista_pareja_exp:
        return 'Pareja/Ex'
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

def columna_genero_agresor (x):
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

lista_conocido = ['Abuela', 'Abuelo','Pareja de la víctima', 'Ex pareja de la víctima', 'Conocido no familiar (Amigo, vecino, entre otros)', 'Hermana', 'Hermano', 'Madrastra', 'Madre', 'Otro pariente', 'Padrastro', 'Padre', 'Tío' ]
lista_no_conocido = ['Desconocido', ]
lista_no_declarado = ['NS/NC']

def columna_conocido_no_conocido (x):
    if x in lista_conocido:
        return 'Agresor conocido por víctima'
    elif x in lista_no_conocido:
        return 'Agresor no conocido por víctima'
    elif x in lista_no_declarado:
        return 'NS/NC'
    else:
        return 'N/A'



# reduccion vinculo llamante

lista_institucion = ['Hospital', 'Comisaría', 'Escuela', 'Defensoría', 'Otra Institución', 'Otra institución']
lista_conocide = ['Madre', 'Vecina/o', 'Padre', 'Familiar', 'Otro conocido', 'Abuela/o','Hermana/o']


def columna_tipo_vinculo_llamante (x):
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
    


llamados['agresor_fam_no_fam'] = \
    llamados.victima_vinculo_agresor.apply(columna_fam_nofam)


llamados['genero_agresor'] = \
    llamados.victima_vinculo_agresor.apply(columna_genero_agresor)


llamados['agresor_conocido_no_conocido'] = \
    llamados.victima_vinculo_agresor.apply(columna_conocido_no_conocido)

llamados['tipo_vinculo_llamante'] = \
    llamados.llamante_vinculo.apply(columna_tipo_vinculo_llamante)



### agrupar variables cualitativamente (por tipo de violencia)

'''Nombres de las nuevas variables:
vs_explotacion_sexual_group (vs_explotacion_sexual, vs_explotacion_sexual_comercial, vs_explotacion_sexual_viajes_turismo,vs_sospecha_trata_personas_fines_sexuales)

vs_violacion_group (vs_violacion_via_vaginal, vs_violacion_via_anal, vs_violacion_via_oral)

ofv_uso_arma (ofv_uso_arma_blanca, ofv_uso_arma_fuego)

ofv_intento_violencia_fisica (ofv_intento_ahorcar, ofv_intento_quemar,ofv_intento_ahogar,ofv_intento_matar)'''

llamados_group = llamados.copy(deep=True)



print('ahora corre el agrupador de variables para lograr: \n\n 1) vs_explotacion_sexual_group: vs_explotacion_sexual, vs_explotacion_sexual_comercial, vs_explotacion_sexual_viajes_turismo,vs_sospecha_trata_personas_fines_sexuales\n\n',
	'2) vs_violacion_group: vs_violacion_via_vaginal, vs_violacion_via_anal, vs_violacion_via_oral\n\n',
	'3) ofv_uso_arma: ofv_uso_arma_blanca, ofv_uso_arma_fuego\n\n',
	'4) ofv_intento_violencia_fisica: ofv_intento_ahorcar, ofv_intento_quemar,ofv_intento_ahogar,ofv_intento_matar\n\n')



print('1)\n')
seteo_agrupador(llamados_group)
print('2)\n')
seteo_agrupador(llamados_group)
print('3)\n')
seteo_agrupador(llamados_group)
print('4)\n')

llamados_group.to_excel("llamados_group.xlsx", index=False)

print('se guardó una copia de llamados_group como xlsx')

del llamados

gower_data = gower.gower_matrix(llamados_group)



# mapping SI/NO in "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in llamados_2['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')

mapData(gower_data, llamados_2, y_convive, False, 
        'Non-metric MDS with Gower')