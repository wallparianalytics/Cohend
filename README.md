# Cohend

Este repositorio contiene un script y un notebook para calcular el tamaño del efecto de Cohen d por grupo.

* **cohend_group.py**: función reutilizable.
* **cohend_group.ipynb**: la primera celda importa las librerías necesarias y la segunda permite subir un archivo `.dta` o `.xlsx` en Google Colab. La interfaz ahora divide la selección de variables en dos listas (PRE y POST) para que sea más intuitivo escogerlas de forma paralela. Solo se muestran las columnas numéricas como candidatas a variables y las de texto para definir el grupo. Puede definirse el nombre del archivo y de la hoja de exportación y generar automáticamente la lista de variables cuando siguen un mismo patrón (por ejemplo `pre_p{n}` y `post_p{n}` para `n=1` a `10`).
* **cohend_group.py**: incluye la función `generar_varlist_rango` para crear fácilmente la lista de variables dada una expresión con `{n}` y un rango.
