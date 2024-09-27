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
    df = pd.read_csv('data/database_anp.csv', index_col='id')
    return df


dados = gerar_df()

# Tratamento de dados
# Remove os valores zero da coluna Length antes de remover os outliers
dados_no_zero = dados[dados['Length'] != 0]

# Calcula o primeiro quartil (Q1) e o terceiro quartil (Q3)
Q1 = dados_no_zero['Length'].quantile(0.25)
Q3 = dados_no_zero['Length'].quantile(0.75)

# Calcula o intervalo interquartil (IQR)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filtra os dados removendo os outliers
dados_cleaned = dados_no_zero[(dados_no_zero['Length'] >= lower_bound) & (
    dados_no_zero['Length'] <= upper_bound)]

# Balanceamento de classes
class_maj = dados_cleaned[dados_cleaned['Delay'] == 0]
class_min = dados_cleaned[dados_cleaned['Delay'] == 1]

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
    st.title("Análise exploratória - Já pode voar?")
    st.subheader("Resumo:")
    st.write('O conjunto de dados "Airlines Dataset to Predict a Delay" oferece informações sobre voos, permitindo a análise e previsão de atrasos. A base contém nove colunas, incluindo identificadores de voos, companhias aéreas, aeroportos de origem e destino, dia da semana, horário do voo, duração e um indicador de atraso (0 para sem atraso e 1 para com atraso).')
    st.write("Durante a análise exploratória, foram identificadas algumas limitações e desafios. A ausência de informações sobre a duração do atraso impede a identificação de padrões mais detalhados. A categorização binária da coluna Delay pode restringir as técnicas estatísticas aplicáveis, levando a interpretações equivocadas ao tratar pequenos e grandes atrasos como iguais. A coluna Length gerou confusão inicial sobre se se referia ao tempo de atraso ou à duração do voo; no entanto, a maioria dos voos com delay igual a 0 apresenta valores diferentes de zero, sugerindo que a coluna realmente representa a duração do voo.")
    st.write("Foram observadas ocorrências atípicas, com apenas quatro registros mostrando Length igual a zero, indicando que esses casos são exceções. A alta diversidade nas colunas AirportFrom, AirportTo e Flight dificultou a análise e interpretação dos resultados, tornando os padrões menos evidentes. A subamostragem de companhias aéreas com mais de 10.000 registros foi necessária para garantir a integridade dos dados e evitar distorções nos resultados.")
    st.write('Além disso, notou-se um desbalanceamento nas ocorrências das companhias aéreas, onde algumas têm muitos mais registros do que outras. Isso pode distorcer as análises e previsões, justificando a necessidade de balanceamento. O desbalanceamento também foi encontrado na coluna Delay, com 55% dos voos sem atraso e 45% com atraso. Para melhorar o desempenho do modelo preditivo, é importante balancear as classes.')
    st.write('Em resumo, a análise exploratória destacou a complexidade da previsão de atrasos de voos, revelando desafios como a ambiguidade de algumas colunas, a presença de outliers e a necessidade de balanceamento nas classes de dados. O próximo passo envolve a aplicação de técnicas de modelagem que considerem essas questões para melhorar a precisão das previsões de atraso nos voos.')
    st.write(
        'Aqui está o link para o conjunto de dados no Kaggle: https://www.kaggle.com/datasets/jimschacko/airlines-dataset-to-predict-a-delay')
    st.title("Conhecendo a base de dados")
    st.write(dados.head())

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Número de linhas e colunas'):
            st.session_state['button_clicked'] = 'Número de linhas e colunas'

    with col2:
        if st.button('Estrutura do DataFrame'):
            st.session_state['button_clicked'] = 'Estrutura do DataFrame'

    with col3:
        if st.button('Tipos de dados de cada coluna'):
            st.session_state['button_clicked'] = 'Tipos de dados de cada coluna'

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button('Verificar linhas duplicadas'):
            st.session_state['button_clicked'] = 'Verificar linhas duplicadas'

    with col5:
        if st.button('Estatísticas das colunas'):
            st.session_state['button_clicked'] = 'Estatísticas das colunas'

    with col6:
        if st.button('Balanceamento de classe'):
            st.session_state['button_clicked'] = 'Balanceamento de classe'

    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button('Resumos estatísticos Length e Time'):
            st.session_state['button_clicked'] = 'Resumos estatísticos Length e Time'

    with col8:
        if st.button('Verificar valores zero na coluna Length'):
            st.session_state['button_clicked'] = 'Verificar valores zero na coluna Length'

    with col9:
        if st.button('Mostrar tratamento de dados'):
            st.session_state['button_clicked'] = 'Mostrar tratamento de dados'

    # Container para exibir o conteúdo dos botões
    with st.container():
        if 'button_clicked' in st.session_state:
            if st.session_state['button_clicked'] == 'Número de linhas e colunas':
                st.write(f"Número de linhas e colunas: {dados.shape}")

            elif st.session_state['button_clicked'] == 'Estrutura do DataFrame':
                buffer = io.StringIO()
                dados.info(buf=buffer)
                s = buffer.getvalue()
                st.text(s)

            elif st.session_state['button_clicked'] == 'Tipos de dados de cada coluna':
                st.write("Tipos de dados de cada coluna:")
                st.write(dados.dtypes)

            elif st.session_state['button_clicked'] == 'Verificar linhas duplicadas':
                st.write("Não há dados redundantes (linhas duplicadas).")

            elif st.session_state['button_clicked'] == 'Estatísticas das colunas':
                st.write("Quantidade de companhias aéreas distintas:",
                         len(dados['Airline'].unique()))
                st.write("Quantidade de modelos de aviões distintos:",
                         len(dados['Flight'].unique()))
                st.write("Quantidade de aeroportos distintos (origem):",
                         len(dados['AirportFrom'].unique()))
                st.write("Quantidade de aeroportos distintos (destino):",
                         len(dados['AirportTo'].unique()))
                st.write("Quantidade total de voos:", len(dados))

            elif st.session_state['button_clicked'] == 'Balanceamento de classe':
                for col in ['Airline', 'Flight', 'AirportFrom', 'AirportTo', 'DayOfWeek', 'Time', 'Length', 'Delay']:
                    st.write(f"Value counts for {col}:")
                    st.write(dados[col].value_counts())
                    st.write("\n")

            elif st.session_state['button_clicked'] == 'Resumos estatísticos Length e Time':
                st.write("Resumos estatísticos:")
                st.write(dados[['Time', 'Length']].describe())
                st.write("Medianas inferiores à média indicam que a média foi distorcida por alguns valores elevados, conhecidos como valores atípicos ou 'outliers'")
                st.write("O campo length representa o tempo de voo que o avião permaneceu no ar. Portanto, não faz sentido que esse valor seja zero, já que todos os voos, por definição, envolvem algum tempo de deslocamento. Um valor zero pode indicar dados inválidos ou incorretos. Para garantir a integridade dos dados, os valores de length devem ser maiores que zero, refletindo o tempo real que o avião esteve em voo.")
            elif st.session_state['button_clicked'] == 'Verificar valores zero na coluna Length':
                zero_length = dados[dados['Length'] == 0]
                if not zero_length.empty:
                    st.write("A coluna Length contém valores iguais a zero:")
                    st.write(zero_length)
                else:
                    st.write("A coluna Length não contém valores iguais a zero.")

            elif st.session_state['button_clicked'] == 'Mostrar tratamento de dados':
                st.write("Tratamento de dados realizado:")
                st.write("1. Remoção de valores inreais na coluna Length.")
                st.write("2. Balanceamento de classes.")
                st.write("Resumos estatísticos após tratamento:")
                st.write(dados_cleaned[['Time', 'Length']].describe())
                st.write("O valor mínimo da segunda variável foi corrigido de 0 para 23, o que faz mais sentido para o tempo de voo. Além disso, a média e o desvio padrão da segunda variável diminuíram, indicando menos outliers e uma distribuição mais concentrada. A primeira variável manteve-se praticamente igual, sugerindo que já estava equilibrada.")
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
