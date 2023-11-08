# librerías

import pandas as pd

#import os




from herramientas import seteo_agrupador,tipo_vinculo_llamante,conocido_no_conocido,genero_agresor,fam_nofam
from variables import orden_columnas

######################################################

# V1 --> unir los datasets

data_2017 = pd.read_csv('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2017.csv',  engine= 'python')
data_2018 = pd.read_csv('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2018.csv', engine= 'python')
data_2019 =pd.read_csv('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2019.csv', encoding='latin-1')
data_2020 =pd.read_csv('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2020.csv', engine= 'python')
data_2021 =pd.read_csv('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/csv/llamados_atendidos_abuso_sexual_2021.csv', engine= 'python')


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
llamados['victima_genero'] = llamados['victima_genero'].fillna('NS/NC')

# Outliers de edad considerados error de carga

llamados['llamante_edad'].loc[(llamados['llamante_edad'] >= 100)] = None
llamados['llamante_edad'].loc[(llamados['llamante_edad'] < 3)] = None

llamados['victima_edad'].loc[(llamados['victima_edad'] >= 103)] = None
llamados['victima_edad'].loc[(llamados['victima_edad'] < 0)] = None


llamados.to_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v2.xlsx', index=False)
print('se guardó llamados v2')
#######################################################################################

#V3--> construcción de variables

llamados['agresor_fam_no_fam'] = \
    llamados.victima_vinculo_agresor.apply(fam_nofam)


llamados['genero_agresor'] = \
    llamados.victima_vinculo_agresor.apply(genero_agresor)


llamados['agresor_conocido_no_conocido'] = \
    llamados.victima_vinculo_agresor.apply(conocido_no_conocido)

llamados['tipo_vinculo_llamante'] = \
    llamados.llamante_vinculo.apply(tipo_vinculo_llamante)


llamados.to_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v3.xlsx', index=False)
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

llamados.to_excel("/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v4.xlsx", index=False)

print('se guardó llamados_v4 como xlsx')

####################################################################

# V5 --> elimino variables con poca información

columnas_pocos_si = []
for i in llamados:
    if (llamados[i]== 'SI').sum() < 191:
        columnas_pocos_si.append(i)
    
vs = list(llamados.loc[:, llamados.columns.str.startswith('vs')].columns)
ofv = list(llamados.loc[:, llamados.columns.str.startswith('ofv')].columns)

for i in vs:
    if i in columnas_pocos_si:
        llamados.drop(i, axis=1, inplace=True)

for i in ofv:
    if i in columnas_pocos_si:
        llamados.drop(i, axis=1, inplace=True)   


llamados.to_excel("/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v5.xlsx", index=False)
print('se guardó llamados_v5 como xlsx')

###################################################################
