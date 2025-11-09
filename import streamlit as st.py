import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("📊 University Student Dashboard")
st.markdown("**Integrantes:** Alejandro Escorcia, Ashley Urueta")

@st.cache_data
def load_data():
    return pd.read_csv("university_student_data.csv")

df = load_data()

# ============================
# SIDEBAR – FILTROS
# ============================

st.sidebar.header("Filtros")

if "year" in df.columns:
    years = sorted(df["year"].unique())
    year_sel = st.sidebar.multiselect("Año", years, years)
else:
    year_sel = None

if "department" in df.columns:
    depts = sorted(df["department"].unique())
    dept_sel = st.sidebar.multiselect("Departamento", depts, depts)
else:
    dept_sel = None

if "term" in df.columns:
    terms = sorted(df["term"].unique())
    term_sel = st.sidebar.multiselect("Término", terms, terms)
else:
    term_sel = None

df_f = df.copy()
if year_sel is not None:
    df_f = df_f[df_f["year"].isin(year_sel)]
if dept_sel is not None and "department" in df.columns:
    df_f = df_f[df_f["department"].isin(dept_sel)]
if term_sel is not None and "term" in df.columns:
    df_f = df_f[df_f["term"].isin(term_sel)]

# ============================
# KPIs
# ============================

st.header("🔹 KPIs Principales")

col1, col2, col3 = st.columns(3)

with col1:
    if "enrolled" in df_f.columns:
        st.metric("Total Enrolled", int(df_f["enrolled"].sum()))
    else:
        st.metric("Registros", df_f.shape[0])

with col2:
    if {"retained", "enrolled"}.issubset(df_f.columns):
        rate = df_f["retained"].sum() / df_f["enrolled"].sum()
        st.metric("Retention Rate", f"{rate:.2%}")
    elif "retention_rate" in df_f.columns:
        st.metric("Retention Rate Promedio", f"{df_f['retention_rate'].mean():.2%}")
    else:
        st.metric("Retention Rate", "N/A")

with col3:
    if "satisfaction_score" in df_f.columns:
        st.metric("Satisfaction Avg", f"{df_f['satisfaction_score'].mean():.2f}")
    else:
        st.metric("Satisfaction", "N/A")

# ============================
# VISUALIZACIONES
# ============================

st.header("📈 Visualizaciones")

# Retention Trend
st.subheader("Tendencia del Retention Rate")
if "year" in df_f.columns:
    if "retention_rate" in df_f.columns:
        df_line = df_f.groupby("year")["retention_rate"].mean()
        st.line_chart(df_line)
    else:
        st.info("No existe 'retention_rate' en el dataset.")
else:
    st.info("No existe la columna 'year'.")

# Satisfaction per year
st.subheader("Satisfaction por Año")
if {"satisfaction_score", "year"}.issubset(df_f.columns):
    df_sat = df_f.groupby("year")["satisfaction_score"].mean()
    st.bar_chart(df_sat)
else:
    st.info("No hay satisfacción por año.")

# Term comparison
st.subheader("Comparación Spring vs Fall")
if "term" in df_f.columns:
    fig, ax = plt.subplots(figsize=(7,4))
    metric = "satisfaction_score" if "satisfaction_score" in df_f.columns else (
             "retention_rate" if "retention_rate" in df_f.columns else None)

    if metric:
        sns.boxplot(data=df_f, x="term", y=metric, ax=ax)
        st.pyplot(fig)
    else:
        st.info("No existe una métrica para comparar términos.")
else:
    st.info("No existe la columna term.")
