import streamlit as st
from functions.visualizations import (
    voos_por_companhias,
    voos_por_semana,
    qtd_atrasos,
    atraso_por_companhia,
    voos_atrasados_por_semana,
)
from PIL import Image
import pandas as pd

st.set_page_config(layout='wide')

# Carregar dados
@st.cache_data
def gerar_df():
    df = pd.read_csv('data/database_anp.csv')
    return df

dados = gerar_df()

# Sidebar
with st.sidebar:
    logo = Image.open('images/logo.png')
    st.image(logo, use_column_width=True)  # Exibe a imagem diretamente

    st.subheader('SELEÇÃO DE GRÁFICOS')
    option = st.selectbox('Escolha um gráfico:', 
                          ['Voos por Companhias', 
                           'Voos por Semana', 
                           'Quantidade de Atrasos', 
                           'Atrasos por Companhia', 
                           'Voos Atrasados por Semana'])

# Exibir gráfico baseado na seleção
if option == 'Voos por Companhias':
    voos_por_companhias(dados)
elif option == 'Voos por Semana':
    voos_por_semana(dados)
elif option == 'Quantidade de Atrasos':
    qtd_atrasos(dados)
elif option == 'Atrasos por Companhia':
    atraso_por_companhia(dados)
elif option == 'Voos Atrasados por Semana':
    voos_atrasados_por_semana(dados)
