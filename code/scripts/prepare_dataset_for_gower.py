import pandas as pd
import numpy as np
from scripts.herramientas import seteo_agrupador

llamados= pd.read_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_group_I.xlsx')

# droppear las variables que están agrupadas en otras, fecha y hora separadas y provincia id

llamados.drop(['vs_explotacion_sexual','vs_explotacion_sexual_comercial','vs_explotacion_sexual_viajes_turismo',
              'vs_sospecha_trata_personas_fines_sexuales', 'vs_violacion_via_vaginal', 'vs_violacion_via_anal', 
               'vs_violacion_via_oral', 'ofv_uso_arma_blanca','ofv_uso_arma_fuego', 'ofv_intento_ahorcar', 
               'ofv_intento_quemar', 'ofv_intento_ahogar','ofv_intento_matar', 'llamado_fecha', 'llamado_hora',
              'llamado_provincia_id'], axis=1, inplace=True)


