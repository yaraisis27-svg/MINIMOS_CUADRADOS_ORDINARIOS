import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

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
    st.sidebar.caption("Valores verdaderos usados para simular: β₀ = 5 y β₁ = 2.5")
else:
    uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])
    if uploaded_file is None:
        st.warning("Sube un archivo CSV o cambia a los datos simulados.")
        st.stop()
    df = pd.read_csv(uploaded_file)


df_num = df.select_dtypes(include="number")
if df_num.shape[1] < 2:
    st.error("El archivo necesita al menos dos columnas numéricas.")
    st.stop()


col_x = st.sidebar.selectbox("Variable independiente (X)", df_num.columns, index=0)
col_y = st.sidebar.selectbox("Variable dependiente (Y)", df_num.columns, index=1)
if col_x == col_y:
    st.error("X e Y deben ser columnas distintas.")
    st.stop()


datos = df_num[[col_x, col_y]].dropna()
if len(datos) < 3:
    st.error("Se necesitan al menos 3 datos válidos para ajustar la recta.")
    st.stop()

st.subheader("1. Vista previa de los datos")
st.dataframe(datos)
st.caption(f"Datos usados: {len(datos)} filas")

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
if np.allclose([beta_0, beta_1], [inter_np, pend_np]):
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
st.pyplot(fig)
plt.close(fig)

st.subheader("5. Residuos (errores)")
fig2, ax2 = plt.subplots(figsize=(8, 3.5))
ax2.scatter(Y_pred, residuos, color="purple", alpha=0.7)
ax2.axhline(0, color="black", linewidth=1)
ax2.set_xlabel("Valor predicho")
ax2.set_ylabel("Residuo")
ax2.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig2)
plt.close(fig2)
st.caption("Si los residuos se ven al azar alrededor de 0, una recta es un buen modelo. "
           "Si forman una curva, la relación probablemente no es lineal.")
