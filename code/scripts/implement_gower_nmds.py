
import pandas as pd
import numpy as np
import gower


from sklearn.manifold import MDS

from matplotlib import pyplot as plt
import seaborn as sns         
from matplotlib.offsetbox import OffsetImage, AnnotationBbox



llamados= pd.read_excel('/home/vcolombo/Documents/Vic/linea_137_llamados_vs/datasets/xlsx/llamados_v5.xlsx')


cols = [col for col in llamados.columns if col not in ['llamante_edad', 'victima_edad','agresor_fam_no_fam', 'genero_agresor', 'agresor_conocido_no_conocido','tipo_vinculo_llamante']]
llamados_2 = llamados[cols]


del llamados

gower_data = gower.gower_matrix(llamados_2)
print("gower_data done")



def mapData(dist_matrix, X, y, metric, title):
    mds = MDS(metric=metric, n_init=6, dissimilarity='precomputed', random_state=0, normalized_stress=True)
    # Get the embeddings
    pts = mds.fit_transform(dist_matrix)

    stress = mds.stress_
    print(stress)
    
    # Plot the embedding, colored according to the class of the points
    fig = plt.figure(2, (15,6))
    ax = fig.add_subplot(1,2,1) 
    
    # pts[:, 0] pts in column 1 (first dimension),y=pts[:, 1] pts in column 2 (second dimension) 

    ax = sns.scatterplot(x=pts[:, 0], y=pts[:, 1], hue=y, palette=['blue', 'red', 'grey'], hue_order=['NO', 'SI', 'NS/NC'])



    plt.title(title)    
    plt.show()


# mapping SI/NO in "victima_convive_agresor" labels to 'y_convive'
y_convive = []
for value in llamados_2['victima_convive_agresor']:
    if value == 'SI':
        y_convive.append('SI')
    elif value == 'NO':
        y_convive.append('NO')
    else:
        y_convive.append('NS/NC')

#cambiar el título según la versión de llamados que uso
mapData(gower_data, llamados_2, y_convive, False, 
        'Non-metric MDS with Gower - llamados_v5')





