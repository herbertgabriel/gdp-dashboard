import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import io  # Adicionando a importação do módulo io

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

# Tratamento de dados
# Balanceamento de classes
class_maj = dados[dados['Delay'] == 0]
class_min = dados[dados['Delay'] == 1]

class_maj_subamostrada = class_maj.sample(len(class_min), random_state=42)
dados_balanceados = pd.concat([class_maj_subamostrada, class_min])
dados_balanceados = dados_balanceados.sample(
    frac=1, random_state=42).reset_index(drop=True)

# Limite máximo para subamostragem
max_samples = 10000


def subamostrar_airlines(dados, col_name, max_samples):
    # Subamostrar companhias com mais de 'max_samples' registros
    major_airlines = dados[col_name].value_counts()[
        lambda x: x > max_samples].index

    # Subamostragem
    dados_major = dados[dados[col_name].isin(major_airlines)].groupby(
        col_name).sample(n=max_samples, random_state=42)

    # Mantendo as companhias que já estão abaixo do limite
    dados_other = dados[~dados[col_name].isin(major_airlines)]

    # Concatenando os dados
    return pd.concat([dados_major, dados_other]).reset_index(drop=True)


# Aplicando a subamostragem para 'Airline'
dados_balanceados = subamostrar_airlines(
    dados_balanceados, 'Airline', max_samples)

# Sidebar
with st.sidebar:
    logo = Image.open('images/logo.png')
    st.image(logo, use_column_width=True)  # Exibe a imagem diretamente

    st.subheader('SELEÇÃO DE GRÁFICOS')
    option = st.selectbox('Escolha um gráfico:', [
        'Inicio',
        'Voos por Companhias',
        'Voos por Semana',
        'Quantidade de Atrasos',
        'Atrasos por Companhia',
        'Voos Atrasados por Semana'
    ])


def inicio():
    st.title("Já pode voar")
    st.subheader("Prever atrasos de voos usando um conjunto de dados de companhias aéreas é uma tarefa complexa que envolve a análise de diversos fatores que podem influenciar o tempo de chegada e partida das aeronaves.")
    st.title("Conhecendo a base de dados")
    st.write(dados.head())

    if st.button('Número de linhas e colunas'):
        st.write(f"Número de linhas e colunas: {dados.shape}")

    if st.button('Estrutura do DataFrame'):
        buffer = io.StringIO()
        dados.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

    if st.button('Tipos de dados de cada coluna'):
        st.write("Tipos de dados de cada coluna:")
        st.write(dados.dtypes)

    if st.button('Verificar linhas duplicadas'):
        duplicatas = dados.duplicated()
        if duplicatas.any():
            st.write("Há dados redundantes (linhas duplicadas):")
            st.write(dados[duplicatas])
            # Limpeza de dados Redundantes
            dados.drop_duplicates(inplace=True)
        else:
            st.write("Não há dados redundantes (linhas duplicadas).")

    if st.button('Estatísticas das colunas'):
        st.write("Quantidade de companhias aéreas distintas:",
                 len(dados['Airline'].unique()))
        st.write("Quantidade de modelos de aviões distintos:",
                 len(dados['Flight'].unique()))
        st.write("Quantidade de aeroportos distintos (origem):",
                 len(dados['AirportFrom'].unique()))
        st.write("Quantidade de aeroportos distintos (destino):",
                 len(dados['AirportTo'].unique()))
        st.write("Quantidade total de voos:", len(dados))

    if st.button('Balanceamento de classe'):
        for col in ['Airline', 'Flight', 'AirportFrom', 'AirportTo', 'DayOfWeek', 'Time', 'Length', 'Delay']:
            st.write(f"Value counts for {col}:")
            st.write(dados[col].value_counts())
            st.write("\n")

    if st.button('Resumos estatísticos'):
        st.write("Resumos estatísticos:")
        st.write(dados[['Time', 'Length']].describe())

    if st.button('Verificar valores zero na coluna Length'):
        zero_length = dados[dados['Length'] == 0]
        if not zero_length.empty:
            st.write("A coluna Length contém valores iguais a zero:")
            st.write(zero_length)
        else:
            st.write("A coluna Length não contém valores iguais a zero.")

    if st.button('Mostrar tratamento de dados'):
        st.write("Balanceamento de classes:")
        st.write(dados_balanceados['Delay'].value_counts())
        st.write("Verificando o balanceamento após subamostragem:")
        st.write(dados_balanceados['Airline'].value_counts())


if option == 'Inicio':
    inicio()
elif option == 'Voos por Companhias':
    voos_por_companhias(dados, dados_balanceados)
elif option == 'Voos por Semana':
    voos_por_semana(dados, dados_balanceados)
elif option == 'Quantidade de Atrasos':
    qtd_atrasos(dados, dados_balanceados)
elif option == 'Atrasos por Companhia':
    atraso_por_companhia(dados, dados_balanceados)
elif option == 'Voos Atrasados por Semana':
    voos_atrasados_por_semana(dados, dados_balanceados)
