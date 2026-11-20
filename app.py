import re
from io import BytesIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
import streamlit as st


NIVEL_SIGNIFICANCIA = 0.05


def _csv_bytes(df: pd.DataFrame) -> bytes:
    """Convierte una tabla en CSV UTF-8 con BOM para que Excel lea los acentos."""
    return df.to_csv(index=False).encode("utf-8-sig")


def _excel_bytes(hojas: dict[str, pd.DataFrame]) -> bytes:
    """Crea un archivo Excel en memoria con una hoja por cada tabla."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for nombre_hoja, tabla in hojas.items():
            tabla.to_excel(writer, sheet_name=nombre_hoja, index=False)
    return buffer.getvalue()


def _png_bytes(fig) -> bytes:
    """Guarda una figura de matplotlib como PNG en memoria."""
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    return buffer.getvalue()


def _r2_texto(r_squared: float) -> str:
    """Presenta el R² y explica el caso en que no está definido."""
    if np.isnan(r_squared):
        return "No definido (Y constante)"
    return f"{r_squared:.6f}"


def _formato_estadistico(valor: float) -> str:
    """Muestra un estadístico con seis decimales o indica si no es calculable."""
    if not np.isfinite(valor):
        return "No calculable"
    return f"{valor:.6f}"


def _formato_p(valor_p: float) -> str:
    """Muestra el valor p sin convertirlo visualmente en un cero exacto."""
    if not np.isfinite(valor_p):
        return "No calculable"
    if valor_p < 1e-6:
        return f"{valor_p:.3e}" if valor_p > 0 else "< 1e-300"
    return f"{valor_p:.6f}"


def _significancia_texto(valor_p: float) -> str:
    """Resume la decisión al nivel de significancia definido."""
    if not np.isfinite(valor_p):
        return "No calculable"
    return "Sí" if valor_p < NIVEL_SIGNIFICANCIA else "No"


def _detectar_columna_periodo(df: pd.DataFrame, col_x, col_y):
    """Busca una columna de periodo o fecha para conservarla en las descargas."""
    palabras_clave = {
        "periodo",
        "period",
        "fecha",
        "date",
        "time",
        "tiempo",
        "mes",
        "month",
        "trimestre",
        "quarter",
        "año",
        "anio",
        "year",
        "semana",
        "week",
        "día",
        "dia",
        "day",
    }

    # Cualquier columna con tipo fecha se conserva aunque su nombre no sea obvio.
    for columna in df.columns:
        if columna not in (col_x, col_y) and pd.api.types.is_datetime64_any_dtype(df[columna]):
            return columna

    for columna in df.columns:
        if columna in (col_x, col_y):
            continue
        partes = re.split(r"[^0-9a-záéíóúüñ]+", str(columna).strip().lower())
        if any(parte in palabras_clave for parte in partes if parte):
            return columna

    return None


def _reporte_texto(
    fuente_datos: str,
    col_x,
    col_y,
    n_filas: int,
    beta_0: float,
    beta_1: float,
    r_squared: float,
    mse: float,
    inter_np: float,
    pend_np: float,
    coincide_polyfit: bool,
    errores_estandar: np.ndarray,
    t_estadisticos: np.ndarray,
    p_valores: np.ndarray,
    dw: float,
) -> str:
    """Construye un reporte legible con los resultados del ajuste MCO."""
    lineas = [
        "Reporte de la regresión por Mínimos Cuadrados Ordinarios (MCO)",
        "=" * 66,
        f"Fuente de datos: {fuente_datos}",
        f"Variable independiente (X): {col_x}",
        f"Variable dependiente (Y): {col_y}",
        f"Filas usadas: {n_filas}",
        "",
        "Ecuación estimada:",
        f"Y = {beta_0:.6f} + {beta_1:.6f} * X",
        "",
        "Métricas del modelo:",
        f"  Intercepto (β₀): {beta_0:.6f}",
        f"  Pendiente (β₁): {beta_1:.6f}",
        f"  R²: {_r2_texto(r_squared)}",
        f"  MSE: {mse:.6f}",
        f"  Durbin-Watson: {_formato_estadistico(dw)}",
        "",
        "Significancia estadística (prueba t bilateral):",
        f"  Nivel de significancia: {NIVEL_SIGNIFICANCIA:.2f} (5 %)",
        f"  Grados de libertad: n - 2 = {n_filas - 2}",
        (
            f"  β₀ (intercepto): error estándar={_formato_estadistico(errores_estandar[0])} | "
            f"t={_formato_estadistico(t_estadisticos[0])} | "
            f"p={_formato_p(p_valores[0])} | "
            f"significativo={_significancia_texto(p_valores[0])}"
        ),
        (
            f"  β₁ (pendiente): error estándar={_formato_estadistico(errores_estandar[1])} | "
            f"t={_formato_estadistico(t_estadisticos[1])} | "
            f"p={_formato_p(p_valores[1])} | "
            f"significativo={_significancia_texto(p_valores[1])}"
        ),
        "  Un valor p menor que 0.05 indica evidencia estadística contra β = 0;",
        "  no demuestra causalidad ni sustituye el análisis económico.",
        "",
        "Interpretación:",
        (
            f"  Por cada unidad que aumenta {col_x}, {col_y} cambia en promedio "
            f"{beta_1:.6f} unidades."
        ),
        "",
        "Durbin-Watson:",
        "  Valores cercanos a 2 no sugieren autocorrelación de primer orden.",
        "  Solo detecta ese tipo de autocorrelación y no es una prueba definitiva;",
        "  los valores críticos dependen del número de observaciones y regresores.",
        "",
        "Verificación contra np.polyfit:",
        (
            f"  Intercepto MCO: {beta_0:.6f} | np.polyfit: {inter_np:.6f} | "
            f"Diferencia: {abs(beta_0 - inter_np):.6e}"
        ),
        (
            f"  Pendiente MCO: {beta_1:.6f} | np.polyfit: {pend_np:.6f} | "
            f"Diferencia: {abs(beta_1 - pend_np):.6e}"
        ),
        f"  Resultado: {'Coinciden' if coincide_polyfit else 'No coinciden'}",
        "",
        "Generado con la calculadora MCO en Streamlit.",
    ]
    return "\n".join(lineas)


st.title("Calculadora de Mínimos Cuadrados Ordinarios (MCO) desde cero")
st.markdown("Regresión lineal simple calculada con álgebra matricial: β = (XᵀX)⁻¹ XᵀY")


st.sidebar.header("Configuración de datos")
option = st.sidebar.selectbox(
    "Selecciona una fuente de datos:",
    ("Datos simulados (relación conocida)", "Subir archivo CSV propio"),
)

if option == "Datos simulados (relación conocida)":
    np.random.seed(42)
    X_raw = np.arange(1, 11, dtype=float)
    # Verdad conocida: intercepto = 5, pendiente = 2.5, más ruido aleatorio
    Y_raw = 5 + 2.5 * X_raw + np.random.normal(0, 1.5, len(X_raw))
    df = pd.DataFrame({"X": X_raw, "Y": Y_raw})
    fuente_datos = "Datos simulados (relación conocida)"
    st.sidebar.caption("Valores verdaderos usados para simular: β₀ = 5 y β₁ = 2.5")
else:
    uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])
    if uploaded_file is None:
        st.warning("Sube un archivo CSV o cambia a los datos simulados.")
        st.stop()
    df = pd.read_csv(uploaded_file)
    fuente_datos = uploaded_file.name


df_num = df.select_dtypes(include="number")
if df_num.shape[1] < 2:
    st.error("El archivo necesita al menos dos columnas numéricas.")
    st.stop()


col_x = st.sidebar.selectbox("Variable independiente (X)", df_num.columns, index=0)
col_y = st.sidebar.selectbox("Variable dependiente (Y)", df_num.columns, index=1)
if col_x == col_y:
    st.error("X e Y deben ser columnas distintas.")
    st.stop()


col_periodo = _detectar_columna_periodo(df, col_x, col_y)
columnas_datos = [col_x, col_y]
if col_periodo is not None:
    columnas_datos.append(col_periodo)

# Se eliminan solo las filas sin X o sin Y; la columna de periodo no condiciona el ajuste.
datos = df[columnas_datos].dropna(subset=[col_x, col_y])
if len(datos) < 3:
    st.error("Se necesitan al menos 3 datos válidos para ajustar la recta.")
    st.stop()

st.subheader("1. Vista previa de los datos")
st.dataframe(datos)
st.caption(f"Datos usados: {len(datos)} filas")
if col_periodo is not None:
    st.caption(f"Columna de periodo/fecha conservada en las descargas: **{col_periodo}**")

X_data = datos[col_x].to_numpy(dtype=float)
Y_data = datos[col_y].to_numpy(dtype=float)


X_matrix = np.column_stack([np.ones(len(X_data)), X_data])  # columna de unos + X
Y_matrix = Y_data.reshape(-1, 1)

XT_X = X_matrix.T @ X_matrix
if np.isclose(np.linalg.det(XT_X), 0):
    st.error("No se puede calcular: XᵀX no tiene inversa (¿todos los valores de X son iguales?).")
    st.stop()

beta = np.linalg.inv(XT_X) @ X_matrix.T @ Y_matrix
beta_0 = beta[0, 0]
beta_1 = beta[1, 0]


Y_pred = (X_matrix @ beta).flatten()
residuos = Y_data - Y_pred
ss_total = np.sum((Y_data - Y_data.mean()) ** 2)
ss_residual = np.sum(residuos ** 2)
r_squared = 1 - ss_residual / ss_total if ss_total != 0 else float("nan")
mse = ss_residual / len(Y_data)

# La inferencia requiere n - 2 grados de libertad en una regresión simple con intercepto.
grados_libertad = len(Y_data) - 2
tolerancia_ajuste_perfecto = np.finfo(float).eps * max(1.0, float(ss_total)) * 100
ajuste_perfecto = bool(ss_residual <= tolerancia_ajuste_perfecto)

if ajuste_perfecto:
    # Si los residuos son cero, los errores estándar y los valores p no están definidos.
    errores_estandar = np.array([np.nan, np.nan])
    t_estadisticos = np.array([np.nan, np.nan])
    p_valores = np.array([np.nan, np.nan])
    dw = float("nan")
    coincide_statsmodels = True
else:
    # statsmodels complementa la inferencia; los coeficientes siguen siendo los del cálculo matricial.
    modelo_ols = sm.OLS(Y_data, X_matrix).fit()
    errores_estandar = np.asarray(modelo_ols.bse, dtype=float)
    t_estadisticos = np.asarray(modelo_ols.tvalues, dtype=float)
    p_valores = np.asarray(modelo_ols.pvalues, dtype=float)
    dw = float(durbin_watson(residuos))
    coincide_statsmodels = bool(
        np.allclose(modelo_ols.params, beta.flatten(), rtol=1e-7, atol=1e-9)
    )

ajuste_casi_perfecto = (
    not ajuste_perfecto
    and np.isfinite(r_squared)
    and r_squared >= 1 - 1e-8
)

st.subheader("2. Resultados del modelo MCO")
c1, c2, c3 = st.columns(3)
c1.metric("Intercepto (β₀)", f"{beta_0:.4f}")
c2.metric("Pendiente (β₁)", f"{beta_1:.4f}")
c3.metric("R²", f"{r_squared:.4f}")
st.latex(rf"\hat{{Y}} = {beta_0:.4f} + {beta_1:.4f}\,X")
st.write(f"Error cuadrático medio (MSE): **{mse:.4f}**")
st.info(
    f"Interpretación: por cada unidad que aumenta **{col_x}**, "
    f"**{col_y}** cambia en promedio **{beta_1:.4f}** unidades."
)

st.markdown("#### Significancia estadística de los coeficientes")
tabla_inferencia = pd.DataFrame(
    {
        "Parámetro": ["β₀ (intercepto)", "β₁ (pendiente)"],
        "Coeficiente estimado": [f"{beta_0:.6f}", f"{beta_1:.6f}"],
        "Error estándar": [
            _formato_estadistico(errores_estandar[0]),
            _formato_estadistico(errores_estandar[1]),
        ],
        "Estadístico t": [
            _formato_estadistico(t_estadisticos[0]),
            _formato_estadistico(t_estadisticos[1]),
        ],
        "Valor p bilateral": [
            _formato_p(p_valores[0]),
            _formato_p(p_valores[1]),
        ],
        "Significativo al 5 %": [
            _significancia_texto(p_valores[0]),
            _significancia_texto(p_valores[1]),
        ],
    }
)
st.table(tabla_inferencia)
st.caption(
    "Sí = p < 0.05; No = p ≥ 0.05. Los errores estándar, estadísticos t y valores p "
    "se calcularon con statsmodels (OLS) usando la misma matriz X, bajo los supuestos "
    "convencionales de MCO. "
    f"Grados de libertad: n - 2 = {grados_libertad}."
)
st.markdown(
    "El **valor p bilateral** indica qué tan probable sería observar un estadístico t "
    "al menos tan extremo si el coeficiente poblacional fuera cero. Si p < 0.05, "
    "se rechaza esa hipótesis nula al 5 %; si p ≥ 0.05, no hay evidencia suficiente "
    "para rechazarla. Un valor p pequeño **no demuestra causalidad** y un valor p "
    "grande no demuestra que el efecto sea exactamente cero."
)

if ajuste_perfecto:
    st.warning(
        "El ajuste es perfecto (residuos prácticamente cero). En este caso los errores "
        "estándar, los estadísticos t, los valores p y Durbin-Watson no están bien definidos."
    )
elif ajuste_casi_perfecto:
    st.warning(
        "El ajuste es casi perfecto. Los errores estándar y los valores p pueden ser "
        "inestables; interpreta la significancia con cautela."
    )

if not coincide_statsmodels:
    st.warning(
        "Los coeficientes de statsmodels no coinciden exactamente con el cálculo matricial. "
        "Revisa los datos antes de usar los valores p."
    )

st.markdown("#### Durbin-Watson")
st.metric("Estadístico Durbin-Watson", _formato_estadistico(dw))
st.caption(
    "Un valor cercano a 2 no sugiere autocorrelación de primer orden; por debajo de 2 "
    "puede indicar autocorrelación positiva y por encima de 2, negativa. Es solo un "
    "indicio: no es una prueba definitiva, solo detecta autocorrelación lineal de primer "
    "orden y sus valores críticos dependen del número de observaciones y de regresores. "
    "Si se aleja de 2, los errores estándar y valores p convencionales deben interpretarse "
    "con cautela."
)


st.subheader("3. Verificación contra una biblioteca")
pend_np, inter_np = np.polyfit(X_data, Y_data, 1)
verif = pd.DataFrame(
    {
        "Parámetro": ["Intercepto", "Pendiente"],
        "Nuestro MCO": [beta_0, beta_1],
        "np.polyfit": [inter_np, pend_np],
    }
)
verif["Diferencia"] = (verif["Nuestro MCO"] - verif["np.polyfit"]).abs()
st.table(verif)
coincide_polyfit = bool(np.allclose([beta_0, beta_1], [inter_np, pend_np]))
if coincide_polyfit:
    st.success("Los resultados coinciden con np.polyfit.")
else:
    st.warning("Los resultados difieren de np.polyfit; revisa los datos.")


st.subheader("4. Dispersión y recta de mínimos cuadrados")
orden = np.argsort(X_data)
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(X_data, Y_data, color="blue", label="Datos de entrada", alpha=0.7)
ax.plot(X_data[orden], Y_pred[orden], color="red", linewidth=2,
        label=f"MCO: Y = {beta_0:.2f} + {beta_1:.2f}X")
ax.set_xlabel(col_x)
ax.set_ylabel(col_y)
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
dispersion_png = _png_bytes(fig)
st.pyplot(fig)
plt.close(fig)

st.subheader("5. Residuos (errores)")
fig2, ax2 = plt.subplots(figsize=(8, 3.5))
ax2.scatter(Y_pred, residuos, color="purple", alpha=0.7)
ax2.axhline(0, color="black", linewidth=1)
ax2.set_xlabel("Valor predicho")
ax2.set_ylabel("Residuo")
ax2.grid(True, linestyle="--", alpha=0.5)
residuos_png = _png_bytes(fig2)
st.pyplot(fig2)
plt.close(fig2)
st.caption("Si los residuos se ven al azar alrededor de 0, una recta es un buen modelo. "
           "Si forman una curva, la relación probablemente no es lineal.")


st.subheader("6. Descargar resultados")
st.caption(
    "Descarga el resumen estadístico, los datos usados, un Excel con varias hojas, "
    "el reporte o las gráficas en alta resolución. Los archivos corresponden a las "
    "variables y observaciones seleccionadas."
)
if col_periodo is not None:
    st.caption(
        f"La columna de periodo/fecha **{col_periodo}** se incluye en el CSV de datos "
        "y en el Excel."
    )

resumen = pd.DataFrame(
    {
        "Métrica": [
            "Fuente de datos",
            "Variable independiente (X)",
            "Variable dependiente (Y)",
            "Columna de periodo/fecha",
            "Número de observaciones",
            "Intercepto (β₀)",
            "Pendiente (β₁)",
            "R²",
            "MSE",
            "Error estándar β₀",
            "Error estándar β₁",
            "Estadístico t β₀",
            "Estadístico t β₁",
            "Valor p β₀ (bilateral)",
            "Valor p β₁ (bilateral)",
            "Significativo al 5 % β₀",
            "Significativo al 5 % β₁",
            "Nivel de significancia",
            "Durbin-Watson",
            "Verificación con np.polyfit",
        ],
        "Valor": [
            fuente_datos,
            str(col_x),
            str(col_y),
            str(col_periodo) if col_periodo is not None else "No incluida",
            len(datos),
            beta_0,
            beta_1,
            _r2_texto(r_squared),
            mse,
            _formato_estadistico(errores_estandar[0]),
            _formato_estadistico(errores_estandar[1]),
            _formato_estadistico(t_estadisticos[0]),
            _formato_estadistico(t_estadisticos[1]),
            _formato_p(p_valores[0]),
            _formato_p(p_valores[1]),
            _significancia_texto(p_valores[0]),
            _significancia_texto(p_valores[1]),
            NIVEL_SIGNIFICANCIA,
            _formato_estadistico(dw),
            "Coinciden" if coincide_polyfit else "No coinciden",
        ],
    }
)

detalle = datos.reset_index(drop=True).copy()
detalle["Predicción MCO"] = Y_pred
detalle["Residuo"] = residuos

columnas_periodo = [col_periodo] if col_periodo is not None else []
columnas_detalle = columnas_periodo + [col_x, col_y, "Predicción MCO", "Residuo"]
detalle = detalle[columnas_detalle]

hojas_excel = {
    "Resumen estadístico": resumen,
    "Datos y predicciones": detalle.drop(columns=["Residuo"]),
    "Residuos": detalle,
}

reporte = _reporte_texto(
    fuente_datos,
    col_x,
    col_y,
    len(datos),
    beta_0,
    beta_1,
    r_squared,
    mse,
    inter_np,
    pend_np,
    coincide_polyfit,
    errores_estandar,
    t_estadisticos,
    p_valores,
    dw,
)

descarga_1, descarga_2, descarga_3 = st.columns(3)
with descarga_1:
    st.download_button(
        "Descargar resumen estadístico (CSV)",
        data=_csv_bytes(resumen),
        file_name="resumen_mco.csv",
        mime="text/csv",
        key="descargar_resumen_csv",
    )
with descarga_2:
    st.download_button(
        "Descargar datos de la regresión (CSV)",
        data=_csv_bytes(detalle),
        file_name="datos_regresion.csv",
        mime="text/csv",
        key="descargar_datos_csv",
    )
with descarga_3:
    st.download_button(
        "Descargar Excel completo (.xlsx)",
        data=_excel_bytes(hojas_excel),
        file_name="resultados_mco.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="descargar_excel",
    )

descarga_4, descarga_5, descarga_6 = st.columns(3)
with descarga_4:
    st.download_button(
        "Descargar reporte (TXT)",
        data=reporte.encode("utf-8"),
        file_name="reporte_mco.txt",
        mime="text/plain",
        key="descargar_reporte_txt",
    )
with descarga_5:
    st.download_button(
        "Descargar gráfico de dispersión (PNG)",
        data=dispersion_png,
        file_name="dispersion_mco.png",
        mime="image/png",
        key="descargar_dispersion_png",
    )
with descarga_6:
    st.download_button(
        "Descargar gráfico de residuos (PNG)",
        data=residuos_png,
        file_name="residuos_mco.png",
        mime="image/png",
        key="descargar_residuos_png",
    )
