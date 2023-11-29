
import pandas as pd
import gower


#from sklearn.manifold import MDS

#from matplotlib import pyplot as plt
#import seaborn as sns         
#from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from herramientas import mapData
#import os



image_path = '/home/vcolombo/Documents/Vic/linea_137_llamados_vs/images'
image_name_v2 = 'nmds_v2.png'
image_name_v4 = 'nmds_v4.png'
image_name_v5 = 'nmds_v5.png'
image_name_v2_edad_v = 'nmds_v2_edad_v.png'
image_name_v2_edad_l= 'image_name_v2_edad_l.png'
image_name_v2_edad_com = 'image_name_v2_edad_com.png'


## llamados V2

llamados_v2= pd.read_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v2.xlsx')

# mapping SI/NO in "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in llamados_v2['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')
    else:
        y_convive.append('NS/NC')


cols = [col for col in llamados_v2.columns if col not in ['llamante_edad', 'victima_edad']]
llamados_2 = llamados_v2[cols]




del llamados_v2

gower_data_v2 = gower.gower_matrix(llamados_2)
print("gower_data done")


#cambiar el título según la versión de llamados que uso
mapData(gower_data_v2, llamados_2, y_convive, False, 'Exploración de "víctima convive con el agresor" con NMDS y dist. de Gower. V2. ', image_path,image_name_v2)

del y_convive
del llamados_2
del gower_data_v2



'''## llamados V4

llamados_v4= pd.read_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v4.xlsx')

# mapping SI/NO in "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in llamados_v4['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')
    else:
        y_convive.append('NS/NC')


cols = [col for col in llamados_v4.columns if col not in ['agresor_fam_no_fam','genero_agresor','agresor_conocido_no_conocido','tipo_vinculo_llamante','llamante_edad', 'victima_edad']]
llamados_2 = llamados_v4[cols]


del llamados_v4

gower_data_v4 = gower.gower_matrix(llamados_2)
print("gower_data done")


#cambiar el título según la versión de llamados que uso
mapData(gower_data_v4, llamados_2, y_convive, False, 
        'Exploración de "víctima convive con el agresor" con NMDS y dist. de Gower. V4.', image_path,image_name_v4)

del y_convive
del llamados_2
del gower_data_v4


## llamados v5


llamados_v5= pd.read_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v5.xlsx')

# mapping SI/NO in "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in llamados_v5['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')
    else:
        y_convive.append('NS/NC')


cols = [col for col in llamados_v5.columns if col not in ['agresor_fam_no_fam','genero_agresor','agresor_conocido_no_conocido','tipo_vinculo_llamante','llamante_edad', 'victima_edad']]
llamados_2 = llamados_v5[cols]


del llamados_v5

gower_data_v5 = gower.gower_matrix(llamados_2)
print("gower_data done")


#cambiar el título según la versión de llamados que uso
mapData(gower_data_v5, llamados_2, y_convive, False, 
        'Exploración de "víctima convive con el agresor" con NMDS y dist. de Gower. V5.', image_path,image_name_v5)


del y_convive
del llamados_2
del gower_data_v5


## llamados V2 pero con edades completas

llamados_v2= pd.read_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v2.xlsx')


# completo_victima_edad
completo_victima_edad = llamados_v2[~(llamados_v2['victima_edad'].isnull())]

del llamados_v2

# mapping SI/NO in "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in completo_victima_edad['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')
    else:
        y_convive.append('NS/NC')


cols = [col for col in completo_victima_edad.columns if col not in ['llamante_edad']]
llamados_2 = completo_victima_edad[cols]




del completo_victima_edad

gower_data_v2 = gower.gower_matrix(llamados_2)
print("gower_data done")


#cambiar el título según la versión de llamados que uso
mapData(gower_data_v2, llamados_2, y_convive, False, 
        'Exploración de "víctima convive con el agresor" con NMDS y dist. de Gower. Datos completos edad de la víctima.', image_path,image_name_v2_edad_v)

del y_convive
del llamados_2
del gower_data_v2



## llamados v2 completo llamante edad

llamados_v2= pd.read_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v2.xlsx')


# completo_llamante_edad
completo_llamante_edad = llamados_v2[~(llamados_v2['llamante_edad'].isnull())]

del llamados_v2

# mapping SI/NO in "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in completo_llamante_edad['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')
    else:
        y_convive.append('NS/NC')


cols = [col for col in completo_llamante_edad.columns if col not in ['victima_edad']]
llamados_2 = completo_llamante_edad[cols]




del completo_llamante_edad

gower_data_v2 = gower.gower_matrix(llamados_2)
print("gower_data done")


#cambiar el título según la versión de llamados que uso
mapData(gower_data_v2, llamados_2, y_convive, False, 
        'Exploración de "víctima convive con el agresor" con NMDS y dist. de Gower. Datos completos de edad de quien llama', image_path,image_name_v2_edad_l)

del y_convive
del llamados_2
del gower_data_v2


## llamados v2 completo edades

llamados_v2= pd.read_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v2.xlsx')


# completo_llamante_edad
completo_edades = llamados_v2[~(llamados_v2['victima_edad'].isnull()) & ~(llamados_v2['llamante_edad'].isnull())]


del llamados_v2

# mapping SI/NO in "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in completo_edades['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')
    else:
        y_convive.append('NS/NC')


gower_data_v2 = gower.gower_matrix(completo_edades)
print("gower_data done")


#cambiar el título según la versión de llamados que uso
mapData(gower_data_v2, completo_edades, y_convive, False, 
        'Exploración de "víctima convive con el agresor" con NMDS y dist. de Gower. Datos completos de edades', image_path,image_name_v2_edad_com)

del y_convive
del completo_edades

del gower_data_v2'''
