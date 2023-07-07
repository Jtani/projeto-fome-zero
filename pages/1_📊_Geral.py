# Imports
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
    page_title = 'Geral',
    page_icon="📊",
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
    default= paises
)

# Filtro de países
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""---""")
st.sidebar.markdown('### by Jooji Tani')


# ===============================
# Layout no Streamlit
# ===============================

st.markdown('# 📊 Visão - Geral')
st.markdown('## Análise geral')
st.markdown('### Temos as seguintes marcas dentro de nossa plataforma:')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5, gap='large')
    with col1:
        # Restaurantes cadastrados
        restarauntes_cadastrados = df1.loc[:,'restaurant_id'].nunique()
        col1.metric('Restaurantes cadastrados', restarauntes_cadastrados)
        
    with col2:
        # Países cadastrados
        paises = df1.loc[:, 'country'].nunique()
        col2.metric('Países cadastrados', paises)

    with col3:
        # Cidades cadastradas
        cidades = df1.loc[:, 'city'].nunique()
        col3.metric('Cidades cadastradas', cidades)

    with col4:
        # Avaliações feitas na plataforma
        votos = df1.loc[:, 'votes'].sum()
        col4.metric('Avaliações feitas na plataforma', f'{votos:,}'.replace(',','.'))

    with col5:
        # Tipos de culinárias oferecidas
        cozinhas = df1.loc[:, 'cuisines'].nunique()
        col5.metric('Tipos de culinárias oferecidas', cozinhas)
 

with st.container():
    st.markdown('## Localização dos restaurantes')
    func.country_maps(df1)      




