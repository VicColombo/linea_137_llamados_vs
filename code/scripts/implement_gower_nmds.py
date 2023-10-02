
import pandas as pd
import numpy as np
import gower


from sklearn.manifold import MDS

from matplotlib import pyplot as plt
import seaborn as sns         
from matplotlib.offsetbox import OffsetImage, AnnotationBbox



llamados= pd.read_excel('llamados_group_I.xlsx')



# droppear las variables que están agrupadas en otras, fecha y hora separadas y provincia id

llamados.drop(['vs_explotacion_sexual','vs_explotacion_sexual_comercial','vs_explotacion_sexual_viajes_turismo',
              'vs_sospecha_trata_personas_fines_sexuales', 'vs_violacion_via_vaginal', 'vs_violacion_via_anal', 
               'vs_violacion_via_oral', 'ofv_uso_arma_blanca','ofv_uso_arma_fuego', 'ofv_intento_ahorcar', 
               'ofv_intento_quemar', 'ofv_intento_ahogar','ofv_intento_matar', 'llamado_fecha', 'llamado_hora',
              'llamado_provincia_id'], axis=1, inplace=True)



# corregir nombres de columnas (TO DO: pasar al pipeline de agrupación luego)

llamados.rename(columns={"ofv_uso_arma": "ofv_uso_arma_group", "ofv_intento_violencia_fisica": "ofv_intento_violencia_fisica_group"}, inplace=True)
#llamados.columns




llamados['victima_genero'] = llamados['victima_genero'].fillna('NS/NC')




cols = [col for col in llamados.columns if col not in ['llamante_edad', 'victima_edad']]
llamados_2 = llamados[cols]




del llamados



gower_data = gower.gower_matrix(llamados_2)
print("gower_data done")



def mapData(dist_matrix, X, y, metric, title):
    mds = MDS(metric=metric, dissimilarity='precomputed', random_state=0)
    # Get the embeddings
    pts = mds.fit_transform(dist_matrix)
    # Plot the embedding, colored according to the class of the points
    fig = plt.figure(2, (15,6))
    ax = fig.add_subplot(1,2,1) 
    
    # pts[:, 0] pts in column 1 (first dimension),y=pts[:, 1] pts in column 2 (second dimension) 

    ax = sns.scatterplot(x=pts[:, 0], y=pts[:, 1], hue=y, palette=['blue', 'red'], hue_order=['NO', 'SI'])



    plt.title(title)    
    plt.show()


# mapping SI/NO in "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in llamados_2['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')



mapData(gower_data, llamados_2, y_convive, False, 
        'Non-metric MDS with Gower')





