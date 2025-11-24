import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64 as bs64
import re

df = pd.read_csv("champs.csv")

st.markdown("""
<style>
* {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.write("""
# champions league
## temporada 2014/2015
""")


def fondo(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = bs64.b64encode(data).decode()

    css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)

fondo("UEFA.webp") 

def fondo_sidebar(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = bs64.b64encode(data).decode()

    css = f"""
    <style>
    /* Fondo para TODO el sidebar */
    [data-testid="stSidebar"] > div:first-child {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    return css

st.markdown(fondo_sidebar("blue.jpg"), unsafe_allow_html=True)


def split_goals(x):
    if isinstance(x, str):
        x = re.sub(r"[^\d\-]", "", x)

        if "-" in x:
            try:
                a, b = x.split("-")
                return int(a), int(b)
            except:
                return None, None

    return None, None


df["g1"], df["g2"] = zip(*df["FT"].apply(split_goals))
df["total_goals"] = df["g1"] + df["g2"]

def get_year(x):
    if isinstance(x, str):
        for part in x.split():
            if part.isdigit() and len(part) == 4:
                return int(part)
    return None

df["year"] = df["Date"].apply(get_year)

with st.sidebar:
    st.write("# Opciones")

    years = ["Todos"] + sorted(df["year"].dropna().unique())
    selected_year = st.selectbox("Selecciona el año:", years)

    bins = st.slider("Número de bins para el histograma:", 1, 20, 10)
    st.write("Bins seleccionados:", bins)


filtered = df.copy()
if selected_year != "Todos":
    filtered = filtered[filtered["year"] == selected_year]


st.markdown("## Gráficos basados en Champions League")


fig, ax = plt.subplots(1, 2, figsize=(12, 4))


ax[0].hist(filtered["total_goals"].dropna(), bins=bins)
ax[0].set_xlabel("Goles Totales")
ax[0].set_ylabel("Frecuencia")
ax[0].set_title("Histograma de goles por partido")

partidos_por_año = df.groupby("year")["FT"].count()

ax[1].bar(partidos_por_año.index, partidos_por_año.values, color="skyblue")
ax[1].set_xlabel("Año")
ax[1].set_ylabel("Partidos")
ax[1].set_title("Cantidad de partidos por año")

st.pyplot(fig)

st.write("## Top 10 equipos con más goles")

g1 = df.groupby("Team 1")["g1"].sum()
g2 = df.groupby("Team 2")["g2"].sum()
g_total = g1.add(g2, fill_value=0).sort_values(ascending=False).head(10)

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(g_total.index, g_total.values, color="orange")
ax2.set_xticklabels(g_total.index, rotation=90)
ax2.set_title("Top 10 equipos por goles")
st.pyplot(fig2)

st.write("## Muestra de datos cargados (primeras filas)")
st.table(df.head())

