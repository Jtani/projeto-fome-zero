# ===============================
# Imports
# ===============================
import pandas as pd
import plotly.express as px
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
    page_title = 'Cidades',
    page_icon="🏙️",
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

st.markdown('# 🏙️Visão - Cidades')
st.markdown('## Análise com foco nas cidades')

with st.container():
    # st.markdown('Top 10 Cidades com mais Restaurantes na Base de Dados')
    df_group = df1[['city', 'restaurant_id', 'country']].groupby(['city', 'country']).count().sort_values('restaurant_id', ascending=False).head(10).reset_index()
    fig = px.bar(df_group, x= 'city', y= 'restaurant_id', color = 'country', title='Top 10 Cidades com mais Restaurantes na Base de Dados', 
                 labels={"city": "Cidades", "restaurant_id": "Quantidade de Restaurantes"}
                 )
    st.plotly_chart(fig, use_container_width=True)
 

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # st.markdown('Top 7 Cidades com Restaurantes com média de avaliação acima de 4')
        df_group = df1[(df1.aggregate_rating >= 4)].groupby(['city', 'country'])['restaurant_id'].count().sort_values(ascending=False).head(7).reset_index()
        fig = px.bar(df_group, x= 'city', y= 'restaurant_id', color = 'country', title='Top 7 Cidades com Restaurantes com média de avaliação acima de 4',
                      labels={"city": "Cidades", "restaurant_id": "Quantidade de Avaliações"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # st.markdown('Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5')
        df_group = df1[(df1.aggregate_rating <= 2.5)].groupby(['city', 'country'])['restaurant_id'].count().sort_values(ascending=False).head(7).reset_index()
        fig = px.bar(df_group, x= 'city', y= 'restaurant_id', color = 'country',
                      title='Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5', 
                      labels={"city": "Cidades", "restaurant_id": "Quantidade de Avaliações"})
        st.plotly_chart(fig, use_container_width=True)


with st.container():
    # st.markdown('Top 10 Cidades com mais restaurantes com tipos culinários distintos')
    df_group = df1.groupby(['city', 'country'])['cuisines'].nunique().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(df_group, x= 'city', y= 'cuisines', color = 'country', title='Top 10 Cidades com mais restaurantes com tipos culinários distintos',
                  labels={"city": "Cidades", "cuisines": "Quantidade de cozinhas"})
    st.plotly_chart(fig, use_container_width=True)