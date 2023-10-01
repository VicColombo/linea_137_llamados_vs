import pandas as pd





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

def seteo_agrupador(dataframe):
    
    # 1
    
    columnas_agrupar = pedir_columnas(dataframe)
    
    nueva_col_agrup = input('\nIngresá el nombre de la nueva variable agrupadora para las columnas: ')
   
    # 2
    
    dataframe[nueva_col_agrup] = dataframe[columnas_agrupar].apply(hay_si, axis=1)
    
    return(dataframe)






def mapData(dist_matrix, X, y, metric, title):
    mds = MDS(metric=metric, dissimilarity='precomputed', random_state=0)
    # Get the embeddings
    pts = mds.fit_transform(dist_matrix)
    # Plot the embedding, colored according to the class of the points
    fig = plt.figure(2, (15,6))
    ax = fig.add_subplot(1,2,1) 
    
    # pts[:, 0] pts in column 1 (first dimension),y=pts[:, 1] pts in column 2 (second dimension) 

    ax = sns.scatterplot(x=pts[:, 0], y=pts[:, 1], hue=y, palette=['blue', 'red'], hue_order=['NO', 'YES'])



    # Add the second plot
    ax = fig.add_subplot(1,2,2)
    # Plot the points again
    plt.scatter(pts[:, 0], pts[:, 1])
    
    # Annotate each point by its corresponding face image
    for x, ind in zip(X, range(pts.shape[0])):
        im = x.reshape(64,64)
        imagebox = OffsetImage(im, zoom=0.3, cmap=plt.cm.gray)
        i = pts[ind, 0]
        j = pts[ind, 1]
        ab = AnnotationBbox(imagebox, (i, j), frameon=False)
        ax.add_artist(ab)
    plt.title(title)    
    plt.show()
