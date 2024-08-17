# librerías

import pandas as pd
import numpy as np
import os




from herramientas import seteo_agrupador,tipo_vinculo_llamante,conocido_no_conocido,genero_agresor,fam_nofam,tipo_hecho_lugar,provincias_red
from variables import orden_columnas

######################################################

# PREPROCESAMIENTO

# V1 --> unir los datasets

dataset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(''))), 'datasets')
#llamados_v2= pd.read_excel(os.path.join(dataset_dir, 'xlsx/llamados_v2.xlsx'), parse_dates=['llamado_fecha_hora'])

data_2017 =pd.read_csv(os.path.join(dataset_dir,'csv/llamados_atendidos_abuso_sexual_2017.csv'),  parse_dates=['llamado_fecha_hora'], engine= 'python')
data_2018 =pd.read_csv(os.path.join(dataset_dir,'csv/llamados_atendidos_abuso_sexual_2018.csv'),  parse_dates=['llamado_fecha_hora'], engine= 'python')
data_2019 =pd.read_csv(os.path.join(dataset_dir,'csv/llamados_atendidos_abuso_sexual_2019.csv'),  parse_dates=['llamado_fecha_hora'], encoding='latin-1')
data_2020 =pd.read_csv(os.path.join(dataset_dir,'csv/llamados_atendidos_abuso_sexual_2020.csv'),  parse_dates=['llamado_fecha_hora'], engine= 'python')
data_2021 =pd.read_csv(os.path.join(dataset_dir,'csv/llamados_atendidos_abuso_sexual_2021.csv'),  parse_dates=['llamado_fecha_hora'], engine= 'python')


## quitar caso_id

data_2019.drop('caso_id',
  axis='columns', inplace=True)
data_2020.drop('caso_id',
  axis='columns', inplace=True)
data_2021.drop('caso_id',
  axis='columns', inplace=True)

## quitar llamado_provincia_indec_id y llamado_provincia_id

data_2017.drop('llamado_provincia_indec_id',
  axis='columns', inplace=True)
data_2018.drop('llamado_provincia_indec_id',
  axis='columns', inplace=True)
data_2019.drop('llamado_provincia_indec_id',
  axis='columns', inplace=True)

data_2020.drop('llamado_provincia_id',
  axis='columns', inplace=True)
data_2021.drop('llamado_provincia_id',
  axis='columns', inplace=True)


# cambios de nombres de columnas

''' 2017 2018 llamante_quien_llama == llamante_vinculo

2017 2018 2019 llamado_provincia_indec_id == llamado_provincia_id'''


data_2017.rename(columns = {'llamante_quien_llama': 'llamante_vinculo', 'llamado_provincia_indec_id': 'llamado_provincia_id'}, inplace = True)
data_2018.rename(columns = {'llamante_quien_llama': 'llamante_vinculo', 'llamado_provincia_indec_id': 'llamado_provincia_id'}, inplace = True)
data_2019.rename(columns = {'llamado_provincia_indec_id': 'llamado_provincia_id'}, inplace = True)


# concateno

llamados = pd.concat([data_2017, data_2018, data_2019, data_2020, data_2021])


################################################################################

# V2 --> normalizaciones y limpieza

# re ordenar columnas

llamados = llamados[orden_columnas]


# valores numéricos: type integer
'''llamante edad as integer y sin datos = NA
victima edad as integer y sin datos = NA
provincia id as integer y sin datos = NA
'''

llamados['victima_edad'] = pd.to_numeric(llamados['victima_edad'], errors='coerce').convert_dtypes()
llamados['llamante_edad'] = pd.to_numeric(llamados['llamante_edad'], errors='coerce').convert_dtypes() 


# Normalizaciones de errores en carga de datos

'''
- en todo el dataset: Ns/Nc = NS/NC
- llamante_edad Sin dato pasar a N/A
- victima_genero N/A -> NS/NC
- llamante género: Masculino = Masculino Trans = Transgénero
- llamante vinculo Vecino = Vecina/o ' Madre' = 'Madre'
- caso judicializado 'NS/NS' = 'NS/NC' 'Sin datos' = 'NS/NC'
- victima_a_resguardo No = NO
- victima_genero Trans = Transgénero
- victima_vinculo_agresor 'Pareja de la vícitma' = 'Pareja de la víctima' 'Pareja ' = 'Pareja de la víctima' Ex pareja = Ex pareja de la víctima
- hecho_lugar Otro(Especificar en observaciones) = Otro
- llamado_provincia: 'Ciudad Autónoma de Buenos Aires' = 'CABA'
- llamado_provincia: 'Santa Fé' = 'Santa Fe' '''


llamados.loc[:, 'llamante_genero'] = llamados['llamante_genero'].replace({' Masculino': 'Masculino', 'Trans': 'Transgénero'})
llamados.loc[:, 'llamante_vinculo'] = llamados['llamante_vinculo'].replace({'Vecino': 'Vecina/o', ' Madre':'Madre'})

llamados.loc[:, 'victima_a_resguardo'] = llamados['victima_a_resguardo'].replace({'No': 'NO'})
llamados.loc[:, 'victima_genero'] = llamados['victima_genero'].replace({'Trans': 'Transgénero'})
llamados.loc[:, 'victima_vinculo_agresor'] = llamados['victima_vinculo_agresor'].replace({'Pareja de la vícitma': 'Pareja de la víctima', 'Pareja ': 'Pareja de la víctima','Pareja': 'Pareja de la víctima', 'Ex pareja': 'Ex pareja de la víctima'})
llamados.loc[:, 'hecho_lugar'] = llamados['hecho_lugar'].replace({'Otro(Especificar en observaciones)': 'Otro'})
llamados.loc[:, 'caso_judicializado'] = llamados['caso_judicializado'].replace({'NS/NS': 'NS/NC', 'Sin datos':'NS/NC'})
llamados.loc[:, 'llamado_provincia'] = llamados['llamado_provincia'].replace({'Ciudad Autónoma de Buenos Aires': 'CABA', 'Santa Fé': 'Santa Fe'})
llamados.replace('Ns/Nc', 'NS/NC', inplace=True)
llamados.loc[:, 'victima_genero'] = llamados['victima_genero'].fillna('NS/NC')


# Outliers de edad considerados error de carga



llamados.loc[llamados['llamante_edad'] >= 100, 'llamante_edad'] = None
llamados.loc[llamados['llamante_edad'] < 3, 'llamante_edad'] = None

llamados.loc[llamados['victima_edad'] >= 103, 'victima_edad'] = None
llamados.loc[llamados['victima_edad'] < 0, 'victima_edad'] = None



llamados.to_excel('/Users/vcolombo/Documents/tp especializacion/linea_137_llamados_vs/datasets/xlsx/llamados_v2.xlsx', index=False)
print('se guardó llamados v2')
#######################################################################################


# 

#V3--> construcción de variables


llamados['genero_agresor'] = \
    llamados.victima_vinculo_agresor.apply(genero_agresor)


llamados['agresor_conocido_no_conocido'] = \
    llamados.victima_vinculo_agresor.apply(conocido_no_conocido)

llamados['tipo_vinculo_llamante'] = \
    llamados.llamante_vinculo.apply(tipo_vinculo_llamante)

# hecho lugar


llamados['hecho_lugar_red'] = \
    llamados.hecho_lugar.apply(tipo_hecho_lugar)


# arma fin de semana

llamados['fin_de_semana'] = np.where(llamados['llamado_fecha_hora'].dt.day_of_week.isin([5,6]), 1,0)

# arma momento del día mañana, mediodía, tarde, noche, madrugada c la hora

def day_part(hour):
    if hour in [6,7,8,9,10,11]:
        return "mañana"
    elif hour in [12,13]:
        return "mediodía"
    elif hour in [14,15,16,17,18,19]:
        return "tarde"
    elif hour in [20,21,22,23,0]:
        return "noche"
    elif hour in [1,2,3,4,5]:
        return "madrugada"


llamados['momento_dia'] = (llamados['llamado_fecha_hora'].dt.hour).apply(day_part)


# arma estación del año

verano_empieza = pd.to_datetime("12-21", format="%m-%d").dayofyear
otoño_empieza = pd.to_datetime("03-21", format="%m-%d").dayofyear
invierno_empieza = pd.to_datetime("06-21", format="%m-%d").dayofyear
primavera_empieza = pd.to_datetime("09-21", format="%m-%d").dayofyear

for index, date in llamados["llamado_fecha_hora"].items():
    if (date.dayofyear >= verano_empieza) or (date.dayofyear < otoño_empieza):
        llamados.at[index, "estacion_del_año"] = "Verano"
    elif (date.dayofyear >= otoño_empieza) and (date.dayofyear < invierno_empieza):
        llamados.at[index, "estacion_del_año"] = "Otoño"
    elif (date.dayofyear >= invierno_empieza) and (date.dayofyear < primavera_empieza):
        llamados.at[index, "estacion_del_año"] = "Invierno"
    else:
        llamados.at[index, "estacion_del_año"] = "Primavera"

# arma variable llamados por región del país

llamados['llamado_provincia_red'] = \
    llamados.llamado_provincia.apply(provincias_red)

llamados.drop('llamado_provincia', axis=1, inplace=True)
llamados.drop('hecho_lugar', axis=1, inplace=True)
llamados.drop('llamante_vinculo', axis=1, inplace=True) 
llamados.drop('victima_vinculo_agresor', axis=1, inplace=True) 


llamados.to_excel('/Users/vcolombo/Documents/tp especializacion/linea_137_llamados_vs/datasets/xlsx/llamados_v3.xlsx', index=False)
print('se guardó llamados v3')
####################################################################

# V4 --> agrupar variables

### agrupar variables cualitativamente (por tipo de violencia)

'''print('ahora corre el agrupador de variables para lograr: \n\n 1) vs_explotacion_sexual_group: vs_explotacion_sexual, vs_explotacion_sexual_comercial, vs_explotacion_sexual_viajes_turismo,vs_sospecha_trata_personas_fines_sexuales\n\n',
	'2) vs_violacion_group: vs_violacion_via_vaginal, vs_violacion_via_anal, vs_violacion_via_oral\n\n',
	'3) ofv_uso_arma_group: ofv_uso_arma_blanca, ofv_uso_arma_fuego\n\n',
	'4) ofv_intento_violencia_fisica_group: ofv_intento_ahorcar, ofv_intento_quemar,ofv_intento_ahogar,ofv_intento_matar\n\n',
    '5)  vs_tentativa_group: vs_tentativa_violacion,vs_Intento_violación_tercera_persona\n\n')'''


'''print('1)\n')
seteo_agrupador(llamados)
print('2)\n')
seteo_agrupador(llamados)
print('3)\n')
seteo_agrupador(llamados)
print('4)\n')
seteo_agrupador(llamados)
print('5)\n')
seteo_agrupador(llamados)'''

columnas_agrupar_1 = ['vs_explotacion_sexual', 'vs_explotacion_sexual_comercial', 'vs_explotacion_sexual_viajes_turismo','vs_sospecha_trata_personas_fines_sexuales']
nueva_col_agrup_1 = 'vs_explotacion_sexual_group'
columnas_agrupar_2 = ['vs_violacion_via_vaginal', 'vs_violacion_via_anal', 'vs_violacion_via_oral']
nueva_col_agrup_2 = 'vs_violacion_group'
columnas_agrupar_3 = ['ofv_uso_arma_blanca', 'ofv_uso_arma_fuego']
nueva_col_agrup_3 = 'ofv_uso_arma_group'
columnas_agrupar_4 = ['ofv_intento_ahorcar', 'ofv_intento_quemar','ofv_intento_ahogar','ofv_intento_matar']
nueva_col_agrup_4 = 'ofv_intento_violencia_fisica_group'
columnas_agrupar_5 = ['vs_tentativa_violacion','vs_Intento_violación_tercera_persona']
nueva_col_agrup_5 = 'vs_tentativa_group'

#1
seteo_agrupador(llamados,columnas_agrupar_1, nueva_col_agrup_1)
#2
seteo_agrupador(llamados,columnas_agrupar_2, nueva_col_agrup_2)
#3
seteo_agrupador(llamados,columnas_agrupar_3, nueva_col_agrup_3)
#4
seteo_agrupador(llamados,columnas_agrupar_4, nueva_col_agrup_4)
#5
seteo_agrupador(llamados,columnas_agrupar_5, nueva_col_agrup_5)

llamados.drop(columnas_agrupar_1 + columnas_agrupar_2+columnas_agrupar_3+columnas_agrupar_4+columnas_agrupar_5,
  axis=1, inplace=True)

llamados.to_excel("/Users/vcolombo/Documents/tp especializacion/linea_137_llamados_vs/datasets/xlsx/llamados_v4.xlsx", index=False)

print('se guardó llamados_v4 como xlsx')

####################################################################

# V5 --> elimino variables con poca información

columnas_pocos_si = []
for i in llamados:
    if (llamados[i]== 'SI').sum() < 191:
        columnas_pocos_si.append(i)
    
vs = list(llamados.loc[:, llamados.columns.str.startswith('vs')].columns)
ofv = list(llamados.loc[:, llamados.columns.str.startswith('ofv')].columns)
borradas = []
for i in vs:
    if i in columnas_pocos_si:
        borradas.append(i)
        llamados.drop(i, axis=1, inplace=True)

for i in ofv:
    if i in columnas_pocos_si:
        borradas.append(i)
        llamados.drop(i, axis=1, inplace=True)   

print('Se eliminaron las columnas poco informativas: ', borradas)


llamados.to_excel("/Users/vcolombo/Documents/tp especializacion/linea_137_llamados_vs/datasets/xlsx/llamados_v5.xlsx", index=False)
print('se guardó llamados_v5 como xlsx')

###################################################################




