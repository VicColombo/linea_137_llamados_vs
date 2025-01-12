# linea_137_llamados_vs

 ## Motivación

La línea telefónica nacional argentina 137 es un servicio público y gratuito para solicitar asistencia en casos de violencia familiar y/o sexual, nacida del programa Las Víctimas contra las Violencias.

En el marco del trabajo para la Especialización en Exploración de Datos de la Facultad de Ciencias Exactas de la UBA, analizo los llamados a la línea 137 para reportar violencia sexual entre 2017 y 2021 y propongo dos experimentos para entrenar clasificadores SVM que imputen los datos faltantes para la variable que codifica si la víctima convive o no con su agresor.

## Guía del repositorio

* [datasets/csv](/datasets/csv): contiene los llamados en crudo desde 01/2017 hasta 08/2021.
* [datasets/xlsx](/datasets/xlsx): carpeta para guardar algunos datasets generados por los distintos scripts.
* [code/scripts](/code/scripts): contiene ```limpieza_normalizacion.py``` donde unifico, normalizo y limpio los datos, y genero los datasets para los experimentos 1 y 2. Y contiene ```herramientas.py``` con funciones auxiliares para el script anterior.
* [code/notebooks](/code/notebooks): contiene una notebook de exploración, una para graficar nmds, y tres con los experimentos 1 y 2 de svm.
* [_latex](/_latex): contiene los archivos de Latex con el trabajo escrito.
