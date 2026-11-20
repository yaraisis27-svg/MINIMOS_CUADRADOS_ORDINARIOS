# Calculadora MCO con Streamlit, valores P y descargas.

Aplicación web para estimar una regresión lineal simple por **Mínimos Cuadrados Ordinarios (MCO)**. Los coeficientes se calculan desde cero con álgebra matricial y NumPy; `statsmodels` se usa como complemento para la inferencia estadística.

La aplicación sirve como calculadora general y también puede usarse con datos de la **Ley de Okun** para México.

## Funcionalidades

- Datos simulados con una relación conocida.
- Carga de un archivo CSV propio.
- Selección de las variables X e Y.
- Cálculo matricial de β₀ y β₁ con β = (XᵀX)⁻¹XᵀY.
- R², error cuadrático medio (MSE) y residuos.
- Errores estándar, estadísticos t y **valores p bilaterales** con n − 2 grados de libertad.
- Tabla de significancia estadística al 5 %.
- Estadístico **Durbin-Watson** con una explicación de sus limitaciones.
- Verificación de coeficientes contra `np.polyfit`.
- Gráficas de dispersión y de residuos.
- Descarga de resultados en CSV, Excel, TXT y PNG.
- Conservación automática de una columna de periodo o fecha en las descargas.

## Archivos del repositorio

| Archivo | Para qué sirve |
|---|---|
| `app.py` | Aplicación principal de Streamlit |
| `requirements.txt` | Librerías que necesita la aplicación |
| `README.md` | Instrucciones y documentación |
| `.gitignore` | Evita subir el entorno virtual y archivos temporales |

No necesitas subir `.venv`, `__pycache__` ni archivos de descarga locales.

## Ejecutar localmente

Requisitos:

- Python 3.11 o superior.
- Git y una cuenta de GitHub para publicar el proyecto.
- Conexión a internet la primera vez, para instalar las dependencias.

### 1. Abrir una terminal en la carpeta del proyecto

```powershell
cd ruta\donde\estan\los\archivos
```

### 2. Crear y activar un entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```powershell
python -m streamlit run app.py
```

Se abrirá una página en el navegador, normalmente en:

```text
http://localhost:8501
```

> Importante: no ejecutes `python app.py`. La forma correcta de iniciar una aplicación de Streamlit es con `streamlit run app.py` o `python -m streamlit run app.py`.

## Publicar el proyecto en GitHub

La opción más sencilla es usar la página web de GitHub:

1. Entra a GitHub y crea un repositorio nuevo.
2. Ponle un nombre, por ejemplo `mco-okun-streamlit`.
3. Déjalo como repositorio público si quieres desplegarlo gratis en Streamlit Community Cloud.
4. No marques la opción de añadir un README ni un `.gitignore` si vas a subir los archivos de esta carpeta.
5. Dentro del repositorio, usa **Add file → Upload files**.
6. Sube `app.py`, `requirements.txt`, `README.md` y `.gitignore`.
7. Haz clic en **Commit changes**.

Los archivos deben quedar en la raíz del repositorio, no dentro de otra carpeta.

### Opción con terminal y Git

Si Git está instalado:

```powershell
cd ruta\donde\estan\los\archivos
git init
git add .
git commit -m "Aplicacion MCO con valores p y descargas"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
git push -u origin main
```

Cambia `TU-USUARIO` y `TU-REPOSITORIO` por los datos reales.

## Desplegar en Streamlit Community Cloud

1. Entra a <https://share.streamlit.io> e inicia sesión con GitHub.
2. Autoriza el acceso a tus repositorios.
3. Haz clic en **Create app** o **New app**.
4. Selecciona el repositorio que acabas de crear.
5. Selecciona la rama `main`.
6. En **Main file path**, escribe:

   ```text
   app.py
   ```

7. En la configuración avanzada, elige una versión de Python compatible, por ejemplo 3.12 o 3.13.
8. Haz clic en **Deploy**.

Streamlit instalará automáticamente las librerías de `requirements.txt`. La aplicación no necesita archivos del servidor ni variables secretas: las descargas se generan en memoria y el CSV se sube desde el navegador.

Si cambias archivos en GitHub, Streamlit normalmente vuelve a desplegar la app. Si no lo hace, entra al panel de la app y usa **Reboot app**.

## Cómo usar la aplicación

1. Elige **Datos simulados** para probar el funcionamiento sin subir archivos.
2. Para usar tus datos, elige **Subir archivo CSV propio** y selecciona tu archivo.
3. Selecciona la variable independiente X y la variable dependiente Y.
4. Revisa:
   - La tabla de coeficientes.
   - La tabla de significancia con errores estándar, t y valores p.
   - R² y MSE.
   - Durbin-Watson.
   - Las gráficas.
5. Ve a **6. Descargar resultados** y descarga el formato que necesites.

## Uso con la Ley de Okun

Sube tu archivo CSV y selecciona:

- X: `igae_variacion_mensual_pct`
- Y: `tasa_desocupacion_nacional_desestacionalizada_pct`

Con la base de 44 observaciones de enero de 2023 a agosto de 2026, los resultados de referencia son aproximadamente:

- β₀ = 2.705160
- β₁ = -0.005130
- R² = 0.001042
- MSE = 0.009591
- Valor p de la pendiente = 0.835214
- Durbin-Watson = 1.454162

La pendiente no es estadísticamente significativa al 5 % en esa muestra.

El archivo CSV no se incluye por defecto en este repositorio. Puedes subirlo directamente desde la aplicación o agregarlo al repositorio si quieres conservarlo como dato de ejemplo.

## Archivos que se pueden descargar

| Archivo | Contenido |
|---|---|
| `resumen_mco.csv` | Resumen del modelo, coeficientes, errores estándar, t, valores p, significancia, R², MSE y Durbin-Watson |
| `datos_regresion.csv` | Periodo/fecha si existe, X, Y, predicción y residuo por observación |
| `resultados_mco.xlsx` | Excel con las hojas **Resumen estadístico**, **Datos y predicciones** y **Residuos** |
| `reporte_mco.txt` | Reporte completo en texto |
| `dispersion_mco.png` | Gráfica de dispersión con la recta de regresión |
| `residuos_mco.png` | Gráfica de residuos |

## Notas metodológicas

- Los coeficientes se calculan con la fórmula matricial original, no con `statsmodels`.
- Los errores estándar, los estadísticos t y los valores p se obtienen con `statsmodels` y usan n − 2 grados de libertad.
- Las pruebas t son bilaterales y suponen los supuestos convencionales de MCO: errores homocedásticos y sin autocorrelación.
- Un valor p pequeño no demuestra causalidad. Un valor p grande no demuestra que el efecto sea exactamente cero.
- Durbin-Watson es un indicio de autocorrelación lineal de primer orden; no es una prueba definitiva y sus valores críticos dependen del tamaño de muestra y del número de regresores.
- Si el ajuste es perfecto, la aplicación avisa que los errores estándar, los valores p y Durbin-Watson no están bien definidos.

## Problemas comunes

**`ModuleNotFoundError: No module named 'statsmodels'`**

Activa el entorno virtual e instala las dependencias:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**La app no abre al ejecutar `python app.py`**

Ejecuta:

```powershell
python -m streamlit run app.py
```

**Streamlit Cloud muestra un error de dependencias**

Revisa que `requirements.txt` esté en la raíz del repositorio y usa **Reboot app** en el panel de Streamlit Cloud.
