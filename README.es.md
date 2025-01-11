# linea_137_llamados_vs

 ## Motivación

La línea telefónica nacional argentina 137 es un servicio público y gratuito para solicitar asistencia en casos de violencia familiar y/o sexual, nacida del programa Las Víctimas contra las Violencias.

En el marco del trabajo para la Especialización en Exploración de Datos de la Facultad de Ciencias Exactas de la UBA, analizo los llamados a la línea 137 para reportar violencia sexual entre 2017 y 2021 y propongo dos experimentos para entrenar clasificadores SVM que imputen los datos faltantes para la variable que codifica si la víctima convive o no con su agresor.

## Guía del repositorio

* [datasets/csv](/datasets/csv) con los llamados en crudo desde 01/2017 hasta 08/2021,
* [scripts](/code/scripts): contiene limpieza_normalizacion.py donde unifico, normalizo y limpio los datos, y genero los datasets llamados_V2 para el experimento 1 con SVM y llamados_V3 para el experimento 2. Y contiene herramientas.py con funciones auxiliares para el script anterior.
* [notebooks](/code/notebooks):



