import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Título de la aplicación
st.title("Calculadora de Mínimos Cuadrados Ordinarios (MCO) desde Cero")
st.markdown("Proyecto desarrollado para la aplicación de Econometría / Economía Industrial.")

st.sidebar.header("Configuración de Datos")

# Opción para elegir tipo de datos
option = st.sidebar.selectbox(
    "Selecciona una fuente de datos:",
    ("Datos de ejemplo (Ventas vs Publicidad)", "Subir archivo CSV propio")
)

if option == "Datos de ejemplo (Ventas vs Publicidad)":
    # Datos simulados base
    np.random.seed(42)
    X_raw = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
    Y_raw = 2.5 * X_raw + np.random.normal(0, 1.5, len(X_raw)) + 5
    df = pd.DataFrame({'X': X_raw, 'Y': Y_raw})
else:
    uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV (debe tener columnas X e Y)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Por favor, sube un archivo CSV o cambia a los datos de ejemplo.")
        st.stop()

st.subheader("1. Vista previa de los datos")
st.dataframe(df)

# Asegurar variables X e Y
X_data = df.iloc[:, 0].values
Y_data = df.iloc[:, 1].values

# --- MATEMÁTICAS DESDE CERO (Álgebra Matricial) ---
# 1. Construir la matriz X con una columna de unos para el intercepto (beta_0)
X_matrix = np.vstack([np.ones(len(X_data)), X_data]).T
Y_matrix = Y_data.reshape(-1, 1)

# 2. Aplicar fórmula analítica MCO: beta = (X^T * X)^(-1) * X^T * Y
XT_X = np.dot(X_matrix.T, X_matrix)
XT_X_inv = np.linalg.inv(XT_X)
XT_Y = np.dot(X_matrix.T, Y_matrix)
beta = np.dot(XT_X_inv, XT_Y)

beta_0 = beta[0][0]
beta_1 = beta[1][0]

st.subheader("2. Resultados del Modelo MCO")
col1, col2, col3 = st.columns(3)
col1.metric("Intercepto ($\beta_0$)", round(beta_0, 4))
col2.metric("Pendiente ($\beta_1$)", round(beta_1, 4))
col3.metric("Ecuación estimada", f"Y = {round(beta_0, 2)} + {round(beta_1, 2)}X")

# 3. Predicciones y Coeficiente de Determinación R^2
Y_pred = np.dot(X_matrix, beta).flatten()

ss_total = np.sum((Y_data - np.mean(Y_data)) ** 2)
ss_residual = np.sum((Y_data - Y_pred) ** 2)
r_squared = 1 - (ss_residual / ss_total)

st.metric("Coeficiente de Determinación ($R^2$)", round(r_squared, 4))

# --- GRÁFICA DE DISPERSIÓN Y LÍNEA DE AJUSTE ---
st.subheader("3. Gráfica de Dispersión y Línea de Mínimos Cuadrados")
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(X_data, Y_data, color='blue', label='Datos reales', alpha=0.7)
ax.plot(X_data, Y_pred, color='red', linewidth=2, label=f'Línea MCO: Y = {beta_0:.2f} + {beta_1:.2f}X')
ax.set_xlabel('Variable Independiente (X)')
ax.set_ylabel('Variable Dependiente (Y)')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)