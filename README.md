# Cohend

Este repositorio contiene un script y un notebook para calcular el tamaño del efecto de Cohen d por grupo.

* **cohend_group.py**: función reutilizable.
* **cohend_group.ipynb**: la primera celda importa las librerías necesarias y la segunda permite subir un archivo `.dta` o `.xlsx` en Google Colab. La interfaz muestra únicamente las columnas numéricas como candidatas a variables y las columnas de texto para escoger el grupo. También permite definir el nombre del archivo y de la hoja donde se exportarán los resultados. Se añadió una opción para generar automáticamente el listado de variables cuando las preguntas siguen un mismo patrón numérico (por ejemplo `pre_p{n}` y `post_p{n}` para `n=1` a `10`).
* **cohend_group.py**: incluye la función `generar_varlist_rango` para crear fácilmente la lista de variables dada una expresión con `{n}` y un rango.
