# librerías
import os
import pandas as pd
import gower
from sklearn.svm import SVC
from herramientas import categoria_edad
from sklearn.model_selection import  GridSearchCV, StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, classification_report
import gc
from sklearn.manifold import MDS



# directorios
dataset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(''))), 'datasets')
image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(''))), 'images')


# dataset a (edades categorizadas)

dataset_a= pd.read_excel(os.path.join(dataset_dir, 'xlsx/llamados_v2.xlsx'))

# categorizar edad en dataset a

dataset_a['victima_edad_cat'] = \
dataset_a.victima_edad.apply(categoria_edad)
dataset_a['llamante_edad_cat'] = \
dataset_a.llamante_edad.apply(categoria_edad)

# drop columnas sin usar

dataset_a.drop(['victima_edad', 'llamante_edad'], axis=1, inplace=True) 

# separar features de target
X = dataset_a.drop(['victima_convive_agresor'], axis=1)
y_previo = dataset_a['victima_convive_agresor']

# guardar los índices de casos NSNC (vacíos)
nsnc_indices = y_previo[y_previo == "NSNC"].index

# Remove "NSNC" rows from the target
y = y_previo.drop(nsnc_indices)

# gower de X
gower_X = gower.gower_matrix(X)
print("gower para dataset_a hecho")

# correr NMDS sobre el total del dataset
nmds = MDS(metric=False, dissimilarity='precomputed', random_state=0, normalized_stress=True) 
X_nmds = nmds.fit_transform(gower_X)

# crear el test final con lo que corresponde a target de X transformado 
test_final = X_nmds[nsnc_indices]


# quitar el test final 
X_nmds_clean = pd.DataFrame(X_nmds).drop(nsnc_indices)



sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=2)
for train_index, test_index in sss.split(X_nmds_clean, y):
    X_train, X_test = X_nmds_clean.iloc[train_index], X_nmds_clean.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

# Parámetros de gridsearch
param_grid = {
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto']
}


svm = SVC()

# GridSearchCV
grid_search = GridSearchCV(svm, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Mejor modelo
best_model = grid_search.best_estimator_

# Aplicar al test set
y_pred = best_model.predict(X_test)

# Evaluate the model
print("Best parameters found: ", grid_search.best_params_)
print("Best cross-validation accuracy: ", grid_search.best_score_)
print("Test set accuracy: ", accuracy_score(y_test, y_pred))
print("Classification report:\n", classification_report(y_test, y_pred))

## test final tiene que estar reducido?

# Apply the best model to the subset of the original dataset
#X_na = test_final.drop(columns=['victima_convive_agresor', 'llamante_edad_escalada', 'victima_edad_escalada'])
#na_predictions = best_model.predict(X_na)

# Add the predictions to the na_convive_df DataFrame
#test_final['victima_convive_agresor_pred'] = na_predictions

#print("\nPredictions for NA 'convive' values:")
#print(test_final)

########################################################


# dataset b (sin llamante_edad y con casos completos de victima_edad)

#llamados_v2= pd.read_excel(os.path.join(dataset_dir, 'xlsx/llamados_v2.xlsx'))

#llamados_v2.drop(['llamante_edad'], axis=1, inplace=True) 

#dataset_b = llamados_v2[~(llamados_v2['victima_edad'].isnull())]