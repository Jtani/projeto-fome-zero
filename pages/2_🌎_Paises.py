# ===============================
# Imports
# ===============================
import pandas as pd
import plotly.express as px
from datetime import datetime
import folium
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image
import utils.funcoes_fornecidas as func


# ===============================
# Import do Dataset
# ===============================
df = pd.read_csv('dados/zomato.csv')

# ===============================
# Limpeza dos dados
# ===============================
df1 = func.clean_code(df)

# ===============================
# Barra Lateral no Streamlit
# ===============================

st.set_page_config(
    page_title = 'País',
    page_icon="🌎",
    layout='wide'
)

image_path = 'img/logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")

paises = df1.country.unique()
country_options = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    paises,
    default= ['India', 'United States of America', 'England', 'South Africa', 'United Arab Emirates', 'Brazil', 'New Zealand'])

# Filtro de países
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""---""")
st.sidebar.markdown('### by Jooji Tani')


# ===============================
# Layout no Streamlit
# ===============================

st.markdown('# 🌎Visão - Países')
st.markdown('## Análise com foco nos países')

with st.container():
    # st.markdown('Quantidade de Restaurantes Registrados por País')
    df_group = df1.groupby('country')['restaurant_id'].count().sort_values(ascending=False).reset_index()
    fig = px.bar(df_group, x= 'country', y= 'restaurant_id', title='Quantidade de Restaurantes Registrados por País', labels={"country": "Paises", "restaurant_id": "Quantidade de Restaurantes"})
    st.plotly_chart(fig, use_container_width=True)
 

with st.container():
    # st.markdown('Quantidade de cidades registrados por país')
    df_group = df1.groupby('country')['city'].nunique().sort_values(ascending=False).reset_index()
    fig = px.bar(df_group, x= 'country', y= 'city', title='Quantidade de Cidades Registrados por País', labels={"country": "Paises", "city": "Quantidade de Cidades"})
    st.plotly_chart(fig, use_container_width=True)

    

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # st.markdown('Média de Avaliações feitas por País')
        df_group = df1[['votes','country']].groupby('country').mean().sort_values('votes', ascending=False).reset_index()
        fig = px.bar(df_group, x= 'country', y= 'votes', title='Média de Avaliações feitas por País', labels={"country": "Paises", "votes": "Quantidade de Avaliações"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # st.markdown('Média de Preço de um prato para duas pessoas por país')
        df_group = df1[['average_cost_for_two', 'country']].groupby('country').mean().sort_values('average_cost_for_two', ascending=False).reset_index()
        fig = px.bar(df_group, x= 'country', y= 'average_cost_for_two',
                      title='Média de Preço de um prato para duas pessoas por país', 
                      labels={"country": "Paises", "average_cost_for_two": "Preço de prato para duas pessoas"})
        st.plotly_chart(fig, use_container_width=True)



