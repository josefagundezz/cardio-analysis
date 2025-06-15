# app.py (Análisis de Datos Médicos - Versión Final Interactiva)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. DICCIONARIO DE TEXTOS (MUCHO MÁS DETALLADO) ---
TEXTS = {
    'es': {
        'page_title': "Análisis de Riesgo Cardiovascular", 'page_icon': "🩺",
        'title': "Dashboard Interactivo de Factores de Riesgo Cardiovascular 🩺",
        'lang_button': "English",
        'tab1': "🔥 Correlaciones", 'tab2': "📊 Análisis Categórico", 'tab3': "🎻 Análisis Numérico",
        
        'corr_header': "Correlación entre Variables",
        'corr_desc': "Un mapa de calor para identificar relaciones lineales. Valores cercanos a +1 (rojo) o -1 (azul) indican una correlación fuerte.",
        'dict_header': "📖 Diccionario de Datos",
        'var_names': {
            'age_years': "Edad (años)", 'height': "Altura (cm)", 'weight': "Peso (kg)", 'bmi': "Índice de Masa Corporal (IMC)",
            'ap_hi': "Presión Arterial Sistólica", 'ap_lo': "Presión Arterial Diastólica",
            'cholesterol': "Nivel de Colesterol", 'gluc': "Nivel de Glucosa", 'smoke': "Hábito de Fumar",
            'alco': "Hábito de Beber Alcohol", 'active': "Actividad Física", 'cardio': "Presencia de Enfermedad Cardiovascular"
        },
        'cholesterol_labels': {1: 'Normal', 2: 'Elevado', 3: 'Muy Elevado'},
        'gluc_labels': {1: 'Normal', 2: 'Elevado', 3: 'Muy Elevado'},
        'binary_labels': {0: 'No', 1: 'Sí'},
        
        'cat_header': "Análisis Interactivo de Variables Categóricas",
        'cat_desc': "Selecciona una variable para comparar la cantidad de pacientes (con y sin enfermedad) en cada categoría.",
        'cat_select': "Selecciona una variable categórica:",
        'cat_plot_title': "Distribución por Condición Cardiovascular",
        'cat_axis_y': "Conteo de Pacientes",
        
        'num_header': "Análisis Interactivo de Variables Numéricas",
        'num_desc': "Selecciona una variable para comparar su distribución (edad, peso, presión arterial) entre pacientes sanos y enfermos.",
        'num_select': "Selecciona una variable numérica:",
        
        'legend_no_disease': "Sin Enfermedad", 'legend_with_disease': "Con Enfermedad",
    },
    'en': {
        'page_title': "Cardiovascular Risk Analysis", 'page_icon': "🩺",
        'title': "Interactive Dashboard of Cardiovascular Risk Factors 🩺",
        'lang_button': "Español",
        'tab1': "🔥 Correlations", 'tab2': "📊 Categorical Analysis", 'tab3': "🎻 Numerical Analysis",
        
        'corr_header': "Correlation Between Variables",
        'corr_desc': "A heatmap to quickly identify linear relationships. Values close to +1 (red) or -1 (blue) indicate a strong correlation.",
        'dict_header': "📖 Data Dictionary",
        'var_names': {
            'age_years': "Age (years)", 'height': "Height (cm)", 'weight': "Weight (kg)", 'bmi': "Body Mass Index (BMI)",
            'ap_hi': "Systolic Blood Pressure", 'ap_lo': "Diastolic Blood Pressure",
            'cholesterol': "Cholesterol Level", 'gluc': "Glucose Level", 'smoke': "Smoking Habit",
            'alco': "Alcohol Intake", 'active': "Physical Activity", 'cardio': "Presence of Cardiovascular Disease"
        },
        'cholesterol_labels': {1: 'Normal', 2: 'Above Normal', 3: 'Well Above Normal'},
        'gluc_labels': {1: 'Normal', 2: 'Above Normal', 3: 'Well Above Normal'},
        'binary_labels': {0: 'No', 1: 'Yes'},

        'cat_header': "Interactive Analysis of Categorical Variables",
        'cat_desc': "Select a variable to compare the number of patients (with and without disease) in each category.",
        'cat_select': "Select a categorical variable:",
        'cat_plot_title': "Distribution by Cardiovascular Condition",
        'cat_axis_y': "Patient Count",
        
        'num_header': "Interactive Analysis of Numerical Variables",
        'num_desc': "Select a variable to compare its distribution (age, weight, blood pressure) between healthy and sick patients.",
        'num_select': "Select a numerical variable:",

        'legend_no_disease': "No Disease", 'legend_with_disease': "With Disease",
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
    df = df[(df['ap_hi'] >= 90) & (df['ap_hi'] <= 240) & (df['ap_lo'] >= 60) & (df['ap_lo'] <= 140)]
    df.drop(columns=['id', 'age'], inplace=True)
    return df
df = load_data()

# --- INTERFAZ ---
st.button(texts['lang_button'], on_click=toggle_language)
st.title(texts['title'])

tab1, tab2, tab3 = st.tabs([texts['tab1'], texts['tab2'], texts['tab3']])

with tab1:
    st.header(texts['corr_header'])
    st.write(texts['corr_desc'])
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    with st.expander(texts['dict_header']):
        for var, desc in texts['var_names'].items():
            st.markdown(f"**{var}:** {desc}")

with tab2:
    st.header(texts['cat_header'])
    st.write(texts['cat_desc'])
    
    cat_vars_keys = ['cholesterol', 'gluc', 'smoke', 'alco', 'active']
    # Usamos el diccionario de nombres para el menú desplegable
    selected_cat_var = st.selectbox(
        texts['cat_select'],
        options=cat_vars_keys,
        format_func=lambda var: texts['var_names'][var]
    )

    if selected_cat_var:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x=selected_cat_var, hue='cardio', data=df, ax=ax, palette='pastel')
        
        ax.set_title(f"{texts['cat_plot_title']}: {texts['var_names'][selected_cat_var]}", fontsize=14)
        ax.set_xlabel(texts['var_names'][selected_cat_var], fontsize=12)
        ax.set_ylabel(texts['cat_axis_y'], fontsize=12)
        
        # Poner etiquetas descriptivas en el eje X
        if selected_cat_var == 'cholesterol':
            ax.set_xticklabels([texts['cholesterol_labels'][i] for i in sorted(df[selected_cat_var].unique())])
        elif selected_cat_var == 'gluc':
            ax.set_xticklabels([texts['gluc_labels'][i] for i in sorted(df[selected_cat_var].unique())])
        else:
            ax.set_xticklabels([texts['binary_labels'][i] for i in sorted(df[selected_cat_var].unique())])
            
        # Poner leyenda descriptiva
        handles, _ = ax.get_legend_handles_labels()
        ax.legend(handles, [texts['legend_no_disease'], texts['legend_with_disease']], title='Condición')
        st.pyplot(fig)

with tab3:
    st.header(texts['num_header'])
    st.write(texts['num_desc'])

    num_vars_keys = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo']
    selected_num_var = st.selectbox(
        texts['num_select'],
        options=num_vars_keys,
        format_func=lambda var: texts['var_names'][var]
    )

    if selected_num_var:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.violinplot(x='cardio', y=selected_num_var, data=df, ax=ax, palette='pastel')
        ax.set_title(f"{texts['num_plot_title'].format(texts['var_names'][selected_num_var])}", fontsize=14)
        ax.set_xticklabels([texts['legend_no_disease'], texts['legend_with_disease']])
        ax.set_xlabel(None)
        ax.set_ylabel(texts['var_names'][selected_num_var], fontsize=12)
        st.pyplot(fig)