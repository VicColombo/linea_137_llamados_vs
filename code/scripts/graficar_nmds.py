# librerías
import os
import pandas as pd
import gower
from herramientas import mapData




# directorios
#dataset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(''))), 'datasets')
image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(''))), 'images')

# imágenes a guardar
image_dataset_a = 'nmds_a.png'
image_dataset_b = 'nmds_b.png'

##############

# dataset a (edades categorizadas)

dataset_a= pd.read_excel('/Users/vcolombo/Documents/tp especializacion/linea_137_llamados_vs/datasets/xlsx/llamados_dataset_a.xlsx')

# Mapeo de SI/NO/NSNC de "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in dataset_a['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')
    else:
        y_convive.append('NS/NC')

# Gower
gower_data_a = gower.gower_matrix(dataset_a)
print("gower para dataset_a hecho")


#cambiar el título según la versión de llamados que uso
mapData(gower_data_a, dataset_a, y_convive, False, ' ', image_path,image_dataset_a)

del y_convive
del dataset_a
del gower_data_a

###################

# dataset b (sin llamante_edad y con casos completos de victima_edad)

dataset_b= pd.read_excel('/Users/vcolombo/Documents/tp especializacion/linea_137_llamados_vs/datasets/xlsx/llamados_dataset_b.xlsx')

# Mapeo de SI/NO/NSNC de "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in dataset_b['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')
    else:
        y_convive.append('NS/NC')

# Gower
gower_data_b = gower.gower_matrix(dataset_b)
print("gower para dataset_b hecho")

#cambiar el título según la versión de llamados que uso
mapData(gower_data_b, dataset_b, y_convive, False, ' ', image_path,image_dataset_b)

del y_convive
del dataset_b
del gower_data_b