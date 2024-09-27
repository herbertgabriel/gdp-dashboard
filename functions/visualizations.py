import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def voos_por_companhias(dados, dados_tratados):
    st.title("Número de Voos por Companhias Aéreas")

    st.subheader("Dados Originais")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Airline', data=dados)
    plt.title(
        'Quantidade de Voos por Companhias Aéreas (Dados Originais)', fontsize=16)
    plt.xlabel('Companhia Aérea', fontsize=14)
    plt.ylabel('Quantidade de Voos', fontsize=14)
    st.pyplot(plt)
    plt.close()

    st.subheader("Dados Tratados")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Airline', data=dados_tratados)
    plt.title(
        'Quantidade de Voos por Companhias Aéreas (Dados Tratados)', fontsize=16)
    plt.xlabel('Companhia Aérea', fontsize=14)
    plt.ylabel('Quantidade de Voos', fontsize=14)
    st.pyplot(plt)
    plt.close()


def voos_por_semana(dados, dados_tratados):
    st.title("Número de Voos por Dia da Semana")

    st.subheader("Dados Originais")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=dados, x='DayOfWeek')
    plt.title('Número de Voos por Dia da Semana (Dados Originais)', fontsize=16)
    plt.xlabel('Dia da Semana', fontsize=14)
    plt.ylabel('Número de Voos', fontsize=14)
    st.pyplot(plt)
    plt.close()

    st.subheader("Dados Tratados")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=dados_tratados, x='DayOfWeek')
    plt.title('Número de Voos por Dia da Semana (Dados Tratados)', fontsize=16)
    plt.xlabel('Dia da Semana', fontsize=14)
    plt.ylabel('Número de Voos', fontsize=14)
    st.pyplot(plt)
    plt.close()


def qtd_atrasos(dados, dados_tratados):
    st.title("Quantidade de Voos Atrasados")

    st.subheader("Dados Originais")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Delay', data=dados)
    plt.title('Gráfico de Atraso de Voos (Dados Originais)', fontsize=16)
    plt.xlabel('(0 = Não Atrasou, 1 = Atrasou)', fontsize=14)
    plt.ylabel('Quantidade de Voos', fontsize=14)
    st.pyplot(plt)
    plt.close()

    quantidade_atrasos = dados[dados['Delay'] == 1].shape[0]
    st.write(
        f"Quantidade de voos que se atrasaram (Dados Originais): **{quantidade_atrasos}**")

    st.subheader("Dados Tratados")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Delay', data=dados_tratados)
    plt.title('Gráfico de Atraso de Voos (Dados Tratados)', fontsize=16)
    plt.xlabel('(0 = Não Atrasou, 1 = Atrasou)', fontsize=14)
    plt.ylabel('Quantidade de Voos', fontsize=14)
    st.pyplot(plt)
    plt.close()

    quantidade_atrasos_tratados = dados_tratados[dados_tratados['Delay'] == 1].shape[0]
    st.write(
        f"Quantidade de voos que se atrasaram (Dados Tratados): **{quantidade_atrasos_tratados}**")


def atraso_por_companhia(dados, dados_tratados):
    st.title("Número de Atrasos por Companhia Aérea")

    st.subheader("Dados Originais")
    atrasos = dados[dados['Delay'] == 1]
    media_atrasos = atrasos['Airline'].value_counts().reset_index()
    media_atrasos.columns = ['Airline', 'Number of Delays']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Airline', y='Number of Delays', data=media_atrasos)
    plt.title('Número de Atrasos por Companhia Aérea (Dados Originais)', fontsize=16)
    plt.xlabel('Companhia Aérea', fontsize=14)
    plt.ylabel('Número de Atrasos', fontsize=14)
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.close()

    st.subheader("Dados Tratados")
    atrasos_tratados = dados_tratados[dados_tratados['Delay'] == 1]
    media_atrasos_tratados = atrasos_tratados['Airline'].value_counts(
    ).reset_index()
    media_atrasos_tratados.columns = ['Airline', 'Number of Delays']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Airline', y='Number of Delays', data=media_atrasos_tratados)
    plt.title('Número de Atrasos por Companhia Aérea (Dados Tratados)', fontsize=16)
    plt.xlabel('Companhia Aérea', fontsize=14)
    plt.ylabel('Número de Atrasos', fontsize=14)
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.close()


def voos_atrasados_por_semana(dados, dados_tratados):
    st.title("Número de Atrasos por Dia da Semana")

    st.subheader("Dados Originais")
    atrasos = dados[dados['Delay'] == 1]
    media_atrasos = atrasos['DayOfWeek'].value_counts().reset_index()
    media_atrasos.columns = ['DayOfWeek', 'NumberDelays']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='DayOfWeek', y='NumberDelays', data=media_atrasos)
    plt.title('Número de Atrasos por Dia da Semana (Dados Originais)', fontsize=16)
    plt.xlabel('Dia da Semana', fontsize=14)
    plt.ylabel('Número de Atrasos', fontsize=14)
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.close()

    # Mapeia os dias da semana para nomes
    dias_da_semana = {
        1: "Domingo",
        2: "Segunda",
        3: "Terça",
        4: "Quarta",
        5: "Quinta",
        6: "Sexta",
        7: "Sábado"
    }

    dia_mais_atrasado = media_atrasos.loc[media_atrasos['NumberDelays'].idxmax(
    )]
    dia_nome = dias_da_semana[dia_mais_atrasado['DayOfWeek']]
    st.write(
        f"Dia da semana com mais atrasos (Dados Originais): **{dia_nome}** com **{dia_mais_atrasado['NumberDelays']}** atrasos.")

    st.subheader("Dados Tratados")
    atrasos_tratados = dados_tratados[dados_tratados['Delay'] == 1]
    media_atrasos_tratados = atrasos_tratados['DayOfWeek'].value_counts(
    ).reset_index()
    media_atrasos_tratados.columns = ['DayOfWeek', 'NumberDelays']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='DayOfWeek', y='NumberDelays', data=media_atrasos_tratados)
    plt.title('Número de Atrasos por Dia da Semana (Dados Tratados)', fontsize=16)
    plt.xlabel('Dia da Semana', fontsize=14)
    plt.ylabel('Número de Atrasos', fontsize=14)
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.close()

    dia_mais_atrasado_tratado = media_atrasos_tratados.loc[media_atrasos_tratados['NumberDelays'].idxmax(
    )]
    dia_nome_tratado = dias_da_semana[dia_mais_atrasado_tratado['DayOfWeek']]
    st.write(
        f"Dia da semana com mais atrasos (Dados Tratados): **{dia_nome_tratado}** com **{dia_mais_atrasado_tratado['NumberDelays']}** atrasos.")
