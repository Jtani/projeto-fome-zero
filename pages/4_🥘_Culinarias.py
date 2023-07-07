# ===============================
# Imports
# ===============================
import pandas as pd
import plotly.express as px
from datetime import datetime
import folium
from haversine import haversine
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
    page_title = 'Culinárias',
    page_icon="🥘",
    layout='wide'
)

image_path = 'logo.png'
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

st.markdown('# 🥘Visão - Culinárias')
st.markdown('## Análise com foco nos tipos de culinárias')

with st.container():
    st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')
    italian, american, arabian, japanese, brazilian = st.columns(5)
    with italian:
        df_aux = df1[df1['cuisines'] == 'Italian']
        df_aux = df_aux.sort_values(['aggregate_rating', 'restaurant_id'],ascending=[False,True]).iloc[0,:]
        
        italian.metric(label = f'Italian: {df_aux["restaurant_name"]}',
                       value =  f'{df_aux["aggregate_rating"]}/5.0',
                       help=f"""
                            País: {df_aux['country']}\n
                            Cidade: {df_aux['city']}\n
                            Média Prato para dois: {df_aux['average_cost_for_two']} ({df_aux['currency']})
                            """)
    with american:
        df_aux = df1[df1['cuisines'] == 'American']
        df_aux = df_aux.sort_values(['aggregate_rating', 'restaurant_id'],ascending=[False,True]).iloc[0,:]

        american.metric(label = f'American: {df_aux["restaurant_name"]}',
                        value =  f'{df_aux["aggregate_rating"]}/5.0',
                        help=f"""
                            País: {df_aux['country']}\n
                            Cidade: {df_aux['city']}\n
                            Média Prato para dois: {df_aux['average_cost_for_two']} ({df_aux['currency']})
                            """)

    with arabian:
        df_aux = df1[df1['cuisines'] == 'Arabian']
        df_aux = df_aux.sort_values(['aggregate_rating', 'restaurant_id'],ascending=[False,True]).iloc[0,:]

        arabian.metric(label = f'Arabian: {df_aux["restaurant_name"]}',
                       value = f'{df_aux["aggregate_rating"]}/5.0',
                       help=f"""
                            País: {df_aux['country']}\n
                            Cidade: {df_aux['city']}\n
                            Média Prato para dois: {df_aux['average_cost_for_two']} ({df_aux['currency']})
                            """)

    with japanese:
        df_aux = df1[df1['cuisines'] == 'Japanese']
        df_aux = df_aux.sort_values(['aggregate_rating', 'restaurant_id'],ascending=[False,True]).iloc[0,:]

        japanese.metric(label = f'Japanese: {df_aux["restaurant_name"]}',
                        value =f'{df_aux["aggregate_rating"]}/5.0',
                        help=f"""
                            País: {df_aux['country']}\n
                            Cidade: {df_aux['city']}\n
                            Média Prato para dois: {df_aux['average_cost_for_two']} ({df_aux['currency']})
                            """)

    with brazilian:
        df_aux = df1[df1['cuisines'] == 'Brazilian']
        df_aux = df_aux.sort_values(['aggregate_rating', 'restaurant_id'],ascending=[False,True]).iloc[0,:]

        brazilian.metric(label = f'Brazilian: {df_aux["restaurant_name"]}',
                         value = f'{df_aux["aggregate_rating"]}/5.0',
                         help=f"""
                            País: {df_aux['country']}\n
                            Cidade: {df_aux['city']}\n
                            Média Prato para dois: {df_aux['average_cost_for_two']} ({df_aux['currency']})
                            """)
    
 
with st.container():
    st.markdown('## Top 10 Restaurantes')
    cols = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "cuisines",
        "average_cost_for_two",
        "aggregate_rating",
        "votes",
    ]
    df_aux = df1[cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).head(10)
    st.dataframe(df_aux)
    
    

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # st.markdown('Top 10 Melhores Tipos de Culinárias')
        df_group = df1[['restaurant_id', 'cuisines', 'aggregate_rating']].groupby(['cuisines']).mean('aggregate_rating').sort_values('aggregate_rating',ascending=False).head(10).reset_index()
        fig = px.bar(df_group, 
                     x= 'cuisines', y= 'aggregate_rating',  
                     title='Top 10 Melhores Tipos de Culinárias',
                      labels={"cuisines": "Culinárias", "aggregate_rating": "Média da avaliação média"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # st.markdown('Top 10 Piores Tipos de Culinárias')
        df_group = df1[['restaurant_id', 'cuisines', 'aggregate_rating']].groupby(['cuisines']).mean('aggregate_rating').sort_values('aggregate_rating',ascending=True).head(10).reset_index()
        fig = px.bar(df_group, 
                     x= 'cuisines', y= 'aggregate_rating', 
                      title='Top 10 Piores Tipos de Culinárias', 
                      labels={"cuisines": "Culinárias", "aggregate_rating": "Média da avaliação média"})
        st.plotly_chart(fig, use_container_width=True)


