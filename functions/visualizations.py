import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def voos_por_companhias(dados):
    st.title("Número de Voos por Companhias Aéreas")
    st.subheader("Este gráfico mostra a quantidade de voos por companhia aérea. "
                  "Você pode observar quais companhias têm mais operações e como se "
                  "comparam entre si.")

    plt.figure(figsize=(10, 6))
    sns.countplot(x='Airline', data=dados)
    plt.title('Quantidade de Voos por Companhias Aéreas', fontsize=16)
    plt.xlabel('Companhia Aérea', fontsize=14)
    plt.ylabel('Quantidade de Voos', fontsize=14)
    
    st.pyplot(plt)
    plt.close()  # Fecha a figura

def voos_por_semana(dados):
    st.title("Número de Voos por Dia da Semana")
    st.subheader("Este gráfico ilustra o número total de voos realizados em cada dia da semana.")

    plt.figure(figsize=(10, 6))
    sns.countplot(data=dados, x='DayOfWeek')
    plt.title('Número de Voos por Dia da Semana', fontsize=16)
    plt.xlabel('Dia da Semana', fontsize=14)
    plt.ylabel('Número de Voos', fontsize=14)
    
    st.pyplot(plt)
    plt.close()  # Fecha a figura

def qtd_atrasos(dados):
    st.title("Quantidade de Voos Atrasados")
    st.subheader("Este gráfico mostra a quantidade de voos que se atrasaram e os que não se atrasaram.")

    plt.figure(figsize=(10, 6))
    sns.countplot(x='Delay', data=dados)
    plt.title('Gráfico de Atraso de Voos', fontsize=16)
    plt.xlabel('(0 = Não Atrasou, 1 = Atrasou)', fontsize=14)
    plt.ylabel('Quantidade de Voos', fontsize=14)
    
    st.pyplot(plt)
    plt.close()  # Fecha a figura

    quantidade_atrasos = dados[dados['Delay'] == 1].shape[0]
    st.write(f"Quantidade de voos que se atrasaram: **{quantidade_atrasos}**")

def atraso_por_companhia(dados):
    st.title("Número de Atrasos por Companhia Aérea")
    st.subheader("Este gráfico mostra quantos atrasos ocorreram em cada companhia aérea.")

    atrasos = dados[dados['Delay'] == 1]
    media_atrasos = atrasos['Airline'].value_counts().reset_index()
    media_atrasos.columns = ['Airline', 'Number of Delays']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Airline', y='Number of Delays', data=media_atrasos)
    plt.title('Número de Atrasos por Companhia Aérea', fontsize=16)
    plt.xlabel('Companhia Aérea', fontsize=14)
    plt.ylabel('Número de Atrasos', fontsize=14)
    plt.xticks(rotation=45)
    
    st.pyplot(plt)
    plt.close()  # Fecha a figura

def voos_atrasados_por_semana(dados):
    st.title("Número de Atrasos por Dia da Semana")
    st.subheader("Este gráfico ilustra a quantidade de atrasos por dia da semana.")

    atrasos = dados[dados['Delay'] == 1]
    media_atrasos = atrasos['DayOfWeek'].value_counts().reset_index()
    media_atrasos.columns = ['DayOfWeek', 'NumberDelays']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='DayOfWeek', y='NumberDelays', data=media_atrasos)
    plt.title('Número de Atrasos por Dia da Semana', fontsize=16)
    plt.xlabel('Dia da Semana', fontsize=14)
    plt.ylabel('Número de Atrasos', fontsize=14)
    plt.xticks(rotation=45)
    
    st.pyplot(plt)
    plt.close()  # Fecha a figura

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

    dia_mais_atrasado = media_atrasos.loc[media_atrasos['NumberDelays'].idxmax()]
    dia_nome = dias_da_semana[dia_mais_atrasado['DayOfWeek']]
    st.write(f"Dia da semana com mais atrasos: **{dia_nome}** com **{dia_mais_atrasado['NumberDelays']}** atrasos.")
