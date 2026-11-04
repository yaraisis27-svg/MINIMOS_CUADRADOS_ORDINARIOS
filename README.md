# MINIMOS_CUADRADOS_ORDINARIOS 
Programar desde cero el modelo de mínimos cuadrados ordinarios para optimizar los parámetros de una regresión lineal. Presentar los resultados en  Streamlit.
# Aplicación Web Interactiva de Mínimos Cuadrados Ordinarios (MCO) desde Cero

## 1. Resumen
Este proyecto implementa una aplicación web interactiva desarrollada en Python utilizando Streamlit y álgebra matricial con NumPy. Su propósito principal es calcular y visualizar las estimaciones de un modelo de regresión lineal simple mediante el método de Mínimos Cuadrados Ordinarios (MCO) programado completamente desde cero, sin bibliotecas de caja negra. La herramienta permite analizar conjuntos de datos predeterminados o cargar archivos CSV personalizados para facilitar la toma de decisiones económicas y cuantitativas.

## 2. Introducción: Problema
En el análisis económico y de negocios, la estimación de relaciones lineales entre variables (como costos e ingresos, o ventas y gasto en publicidad) es fundamental. A menudo, los analistas dependen de software privativo o funciones automatizadas ("cajas negras") cuyo funcionamiento matemático interno no es transparente. Esto dificulta la comprensión rigurosa de cómo se minimizan los errores residuales y limita la flexibilidad para integrar estos cálculos en herramientas web a la medida.

## 3. Introducción: Objetivos
- **Objetivo General:** Desarrollar una aplicación web interactiva para calcular la línea de regresión de Mínimos Cuadrados Ordinarios utilizando estrictamente álgebra matricial desde cero.
- **Objetivos Específicos:**
  1. Implementar la fórmula analítica matricial $\beta = (X^T X)^{-1} X^T Y$ utilizando `numpy`.
  2. Construir una interfaz gráfica funcional en Streamlit que permita la carga de datos propios y la visualización dinámica.
  3. Evaluar el ajuste del modelo mediante el cálculo del coeficiente de determinación ($R^2$).

## 4. Solución y Evidencia
La solución se compone de un script modular en Python (`app.py`) que procesa los datos de entrada, construye la matriz de diseño agregando el término independiente (intercepto $\beta_0$), calcula los estimadores matriciales, y genera visualizaciones interactivas con `matplotlib`.

*(Aquí puedes insertar capturas de pantalla de tu aplicación corriendo en Streamlit mostrando los resultados y la gráfica)*

## 5. Conclusiones
### Conclusiones Generales
El desarrollo de este proyecto demuestra que es posible implementar herramientas econométricas eficientes y transparentes utilizando código abierto y librerías estándar de Python, eliminando la dependencia de software comercial costoso.

### Conclusiones Particulares
- La utilización de operaciones matriciales con `numpy` optimiza el cálculo analítico de $\beta_0$ y $\beta_1$, garantizando precisión matemática exacta.
- La integración con Streamlit convierte un modelo matemático estático en una herramienta analítica interactiva y accesible para cualquier tomador de decisiones.

## 6. Reproducibilidad
Instrucciones detalladas para ejecutar el proyecto en un entorno local:

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/yaraisis27-svg/MINIMOS_CUADRADOS_ORDINARIOS.git](https://github.com/yaraisis27-svg/MINIMOS_CUADRADOS_ORDINARIOS.git)
   cd mco-streamlit-app
