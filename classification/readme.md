# El presente material son los resultados del proyecto BEIFI Ago-Dic 2019 del SIP20190257

## Algoritmo de procesamiento digital de imágenes
LemonMasks_gen.ipynb

### Objetivos 
1. Generar máscaras de limones a partir de una corrección de la base de datos de Lemonator.
2. Resaltar lesiones en las imágenes de limones.

### Resultados

### Conclusiones y recomendaciones
Al implementar filtros de tophat se ha mejorado la segmentación de los limones, eliminando mayormente la base del limon en la imagen. Se sugiere implementar el algoritmo de segmentación propuesto en el algoritmo previo desarrollado por Angel Hernandez. Adicionalmente, se sugiere adicional el algoritmo para resaltar lesiones y comprobar resultados en el análisis de CCI.


## Algoritmo para clasificación de limones
01Lemon_Diseases.ipynb 

### Objetivos
1. Generar labels de las imágenes.
2. Desarrollar y evaluar un modelo de aprendizaje supervisado.

### Resultados

### Conclusiones y recomendaciones
Aunque el desempeño del clasificador tiene un resultado adecuado, se identificó un sesgo en el criterio de referencia de la clasificación de limones, debido a que fue una clasificación subjetiva por el usuario. Por lo anterior, se sugiere corregir los labels de la base de datos con una clasificación por medio de valores de CCI (Citrus Colour Index), integrando la investigación de Angel Hernández en el mismo proyecto SIP. 
