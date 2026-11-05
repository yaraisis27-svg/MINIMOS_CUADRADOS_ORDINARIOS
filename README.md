# MINIMOS_CUADRADOS_ORDINARIOS 
Programar desde cero el modelo de mínimos cuadrados ordinarios para optimizar los parámetros de una regresión lineal. Presentar los resultados en  Streamlit.
# Aplicación Web Interactiva de Mínimos Cuadrados Ordinarios (MCO) desde Cero

## 1. Introducción 
En este proyecto hicimos una aplicación web con Python, usando Streamlit para la interfaz y NumPy para el álgebra matricial. La app calcula una regresión lineal simple por Mínimos Cuadrados Ordinarios (MCO), pero programando el método desde cero con la fórmula β = (XᵀX)⁻¹XᵀY. Se puede trabajar con datos simulados, donde ya sabemos cuál es la relación real, o subir un CSV propio y elegir qué columnas usar como X y como Y. Además de la recta, la app muestra el R², el error cuadrático medio, las gráficas y la verificación de los resultados.

## 2. Problema a resolver 
En economía y negocios es muy común analizar cómo se relacionan dos variables, como costos e ingresos o ventas y gasto en publicidad. El problema es que muchas veces se usan programas de paga o funciones automáticas tipo “caja negra”, y no se entiende bien qué pasa por dentro ni cómo se minimizan los errores. Eso dificulta saber si el resultado es confiable y adaptar los cálculos a una herramienta propia.

## 3. Objetivos
El objetivo principal es hacer una aplicación web interactiva para calcular la recta de regresión por mínimos cuadrados, pero programando todo el cálculo con álgebra matricial desde cero. En cuanto a lo que vamos a hacer en concreto: primero, vamos a aplicar la fórmula matricial β = (XᵀX)⁻¹XᵀY usando NumPy, y para eso armamos la matriz de diseño poniendo una columna llena de unos para que también calcule bien el intercepto. Después, haremos la interfaz en Streamlit para que sea fácil de usar: ahí podrás elegir si quieres usar datos que el programa genera solos o subir tu propio archivo CSV, y ver todo en pantalla, tanto los números como las gráficas, sin complicaciones. También vamos a revisar qué tan bien funciona el modelo, usando el coeficiente R², el error cuadrático medio y viendo los residuos. Y por último, para estar seguros de que no nos equivocamos, compararemos lo que obtengamos con lo que da `np.polyfit` y así comprobamos que todo esté bien calculado.

## 4. Solución y evidencia
La solución consiste en un script llamado `app.py` que funciona de la siguiente manera: primero, le damos al usuario la opción de trabajar con datos generados de forma simulada, donde se parte de los valores β₀ = 5 y β₁ = 2.5 a los que se les añade ruido aleatorio, o bien cargar su propio archivo CSV, y luego elegir qué columnas serán la variable independiente X y cuál será la variable dependiente Y. Antes de seguir, el programa hace varias comprobaciones importantes: verifica que tengamos al menos tres registros válidos, que las columnas elegidas sean distintas y que la matriz producto de transponer X y multiplicarla por sí misma tenga matriz inversa, todo esto para evitar que el código falle al hacer los cálculos. Después de pasar esas revisiones, se arma la matriz de diseño y se calculan los coeficientes β₀ y β₁ usando operaciones matriciales tal como lo pide el método de mínimos cuadrados ordinarios. Una vez obtenidos los valores, se calculan medidas para evaluar qué tan bien funciona el modelo, como el coeficiente de determinación R² y el error cuadrático medio MSE, además de calcular los residuos y explicar de forma clara qué significa el valor de la pendiente que obtuvimos. Para confirmar que todo está bien, se incluye una tabla que compara nuestros resultados con los que da la función `np.polyfit`, calculando la diferencia entre ambos valores; es importante aclarar que usamos esa función solo como referencia para verificar que nuestro cálculo es correcto y no para obtener los coeficientes del modelo. Por último, el programa muestra dos gráficas: una con los puntos de los datos y la recta que se ajusta a ellos, y otra donde se representan los residuos frente a los valores que el modelo predice, lo que nos ayuda a darnos cuenta si usar una recta es realmente una buena opción para describir la relación entre las variables que estamos analizando.

Liga funcional al repositorio: https://github.com/yaraisis27-svg/MINIMOS_CUADRADOS_ORDINARIOS


## 5. Conclusiones
 #### Conclusiones generales: 
Con este proyecto vimos que sí se pueden hacer herramientas econométricas claras y confiables usando código abierto y librerías básicas de Python, sin depender de software comercial caro, y entendiendo paso a paso cómo se calculan los resultados.

 #### Conclusiones particulares:

En cuanto a cada integrante:
Con los datos simulados, la app recupera valores muy cercanos a los reales (β₀ = 5 y β₁ = 2.5). Eso muestra que el método funciona, y la diferencia que queda se debe al ruido aleatorio.
Los resultados de nuestro MCO coinciden con los de np.polyfit, lo que valida que la implementación matricial está bien hecha.
El R², el MSE y la gráfica de residuos nos ayudan a juzgar qué tan bueno es el ajuste, no solo a calcular una recta.
Streamlit convierte un modelo matemático que solo estaba en el código en una herramienta interactiva que cualquier persona puede usar con sus propios datos.

## 6. Reproducibilidad
Requisitos previos
Python 3.9 o superior ( lo puede revisar con python --version).
pip para instalar las librerías.
Los archivos del proyecto: app.py y requirements.txt.
Dependencias

El proyecto usa estas librerías:
numpy	Álgebra matricial para calcular β = (XᵀX)⁻¹XᵀY
pandas	Leer el CSV y manejar los datos en tabla
matplotlib	Gráficas de dispersión, recta y residuos
streamlit	Interfaz web interactiva

Para instalarlas más fácil, creamos un archivo requirements.txt con este contenido:
text
numpy
pandas
matplotlib
streamlit

Pasos de instalación
Descargar o clonar el proyecto y abrir una terminal dentro de la carpeta donde está app.py.
Una recomendación: Crear un entorno virtual para no mezclar librerías con otros proyectos:

   python -m venv venv

Activarlo:


   ### En Windows
   venv\Scripts\activate

   ### En Mac o Linux
   source venv/bin/activate
Instalar las dependencias:

   pip install -r requirements.txt
Pasos de ejecución
En la terminal, dentro de la carpeta del proyecto, correr:

   streamlit run app.py
Se abre automáticamente el navegador en http://localhost:8501. Si no se abre, se copia esa dirección en el navegador.
Usar la app desde la barra lateral:
Elegir Datos simulados, que ya traen una relación conocida, o Subir archivo CSV propio.
Si se sube un CSV, tiene que tener al menos dos columnas numéricas. Después se eligen cuáles serán X y Y.
Ver los resultados (β₀, β₁, R², MSE), la verificación contra np.polyfit y las gráficas.
Para cerrar la app, presionar Ctrl + C en la terminal.
¿Cómo comprobar que funciona bien?

Con los datos simulados se usa una semilla fija (np.random.seed(42)), así que cualquier persona que corra el proyecto debe obtener exactamente los mismos resultados. Además, la tabla de verificación debe mostrar el mensaje “Los resultados coinciden con np.polyfit”. Si aparece, la instalación y el cálculo están bien.