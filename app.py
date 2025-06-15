# app.py (Análisis de Datos Médicos - Bilingüe con Pestañas)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. DICCIONARIO DE TEXTOS ---
TEXTS = {
    'es': {
        'page_title': "Análisis de Riesgo Cardiovascular",
        'page_icon': "🩺",
        'title': "Dashboard de Factores de Riesgo Cardiovascular 🩺",
        'tab1': "🔥 Correlaciones",
        'tab2': "📊 Grupos Categóricos",
        'tab3': "🎻 Grupos Numéricos",
        'corr_header': "Correlación entre Todas las Variables",
        'corr_desc': "Un mapa de calor para identificar rápidamente las relaciones lineales entre variables. Valores cercanos a +1 (rojo intenso) o -1 (azul intenso) indican una correlación fuerte.",
        'cat_header': "Análisis de Hábitos y Niveles de Salud",
        'cat_desc': "Comparación de la cantidad de pacientes (con y sin enfermedad) para categorías como colesterol, glucosa y hábitos de vida.",
        'cat_plot_title': "Comparación por Condición Cardiovascular",
        'cat_axis_x': "Valor de la Categoría",
        'cat_axis_y': "Conteo de Pacientes",
        'cat_legend_0': "Sin Enfermedad",
        'cat_legend_1': "Con Enfermedad",
        'num_header': "Distribución de Variables Numéricas por Condición",
        'num_desc': "Los gráficos de violín nos permiten ver la forma de la distribución y la densidad de las variables numéricas clave para ambos grupos de pacientes.",
        'num_plot_title': "Distribución de '{}' por Condición Cardiovascular",
        'num_axis_x': "Condición"
    },
    'en': {
        'page_title': "Cardiovascular Risk Analysis",
        'page_icon': "🩺",
        'title': "Cardiovascular Risk Factors Dashboard 🩺",
        'tab1': "🔥 Correlations",
        'tab2': "📊 Categorical Groups",
        'tab3': "🎻 Numerical Groups",
        'corr_header': "Correlation Between All Variables",
        'corr_desc': "A heatmap to quickly identify linear relationships between variables. Values close to +1 (deep red) or -1 (deep blue) indicate a strong correlation.",
        'cat_header': "Analysis of Habits and Health Levels",
        'cat_desc': "Comparison of the number of patients (with and without disease) for categories like cholesterol, glucose, and lifestyle habits.",
        'cat_plot_title': "Comparison by Cardiovascular Condition",
        'cat_axis_x': "Category Value",
        'cat_axis_y': "Patient Count",
        'cat_legend_0': "No Disease",
        'cat_legend_1': "With Disease",
        'num_header': "Distribution of Numerical Variables by Condition",
        'num_desc': "Violin plots allow us to see the shape of the distribution and density of key numerical variables for both patient groups.",
        'num_plot_title': "Distribution of '{}' by Cardiovascular Condition",
        'num_axis_x': "Condition"
    }
}

# --- LÓGICA DE LA APP ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
def toggle_language():
    st.session_state.lang = 'es' if st.session_state.lang == 'en' else 'en'
st.set_page_config(page_title=TEXTS[st.session_state.lang]['page_title'], page_icon="🩺", layout="wide")
texts = TEXTS[st.session_state.lang]

@st.cache_data
def load_data():
    df = pd.read_csv('cardio_train.csv', sep=';')
    df['age_years'] = (df['age'] / 365.25).round().astype(int)
    # Limpieza de datos atípicos de presión arterial que podrían ser errores de entrada
    df = df[(df['ap_hi'] >= 90) & (df['ap_hi'] <= 240)]
    df = df[(df['ap_lo'] >= 60) & (df['ap_lo'] <= 140)]
    df.drop(columns=['id', 'age'], inplace=True)
    return df
df = load_data()

# --- INTERFAZ ---
st.button('Español / English', on_click=toggle_language)
st.title(texts['title'])

# Creación de Pestañas (Tabs)
tab_keys = ['tab1', 'tab2', 'tab3']
tab_labels = [texts[key] for key in tab_keys]
tab1, tab2, tab3 = st.tabs(tab_labels)

with tab1:
    st.header(texts['corr_header'])
    st.write(texts['corr_desc'])
    correlation_matrix = df.corr()
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=.5, ax=ax)
    st.pyplot(fig)

with tab2:
    st.header(texts['cat_header'])
    st.write(texts['cat_desc'])
    cols_to_melt = ['cholesterol', 'gluc', 'smoke', 'alco', 'active']
    df_melted = pd.melt(df, id_vars='cardio', value_vars=cols_to_melt)
    
    cat_plot = sns.catplot(x='value', hue='cardio', col='variable', 
                           data=df_melted, kind='count', height=5, aspect=1, sharex=False)
    cat_plot.fig.suptitle(texts['cat_plot_title'], y=1.03, fontsize=16)
    cat_plot.set_axis_labels(texts['cat_axis_x'], texts['cat_axis_y'])
    cat_plot.set_titles("Variable: {col_name}")
    new_labels = [texts['cat_legend_0'], texts['cat_legend_1']]
    for t, l in zip(cat_plot._legend.texts, new_labels): t.set_text(l)
    st.pyplot(cat_plot)

with tab3:
    st.header(texts['num_header'])
    st.write(texts['num_desc'])
    numeric_vars = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo']
    
    for var in numeric_vars:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.violinplot(x='cardio', y=var, data=df, ax=ax, palette='pastel')
        ax.set_title(texts['num_plot_title'].format(var), fontsize=14)
        ax.set_xticklabels([texts['cat_legend_0'], texts['cat_legend_1']])
        ax.set_xlabel(texts['num_axis_x'], fontsize=12)
        ax.set_ylabel(var, fontsize=12)
        st.pyplot(fig)