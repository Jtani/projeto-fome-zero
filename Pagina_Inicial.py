import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'Página Inicial',
    page_icon='house',
    layout='wide'
)

image = Image.open('img/logo.png')
st.sidebar.image(image, width=120)

# ===============================
# Barra Lateral no Streamlit
# ===============================

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")

st.write('# Fome Zero Growth Dashboard')

st.markdown(
    """
    Growth Dashboard foi construído com o intuito de ter uma visão dos dados dos restaurantes;
    ### O que temos no dashboard?
    - #### Visão Geral:
        - Qtd de restaurantes cadastrados
        - Qtd de países
        - Qtd de cidades
        - Qtd de avaliações
        - Qtd de tipos de culinárias diferentes
        - Mapa com a localização dos restaurantes

    - #### Visão País:
        - Gráfico de Restaurantes registrados x País
        - Gráfico de Cidades registrados x País
        - Gráfico de Quantidade de avaliações x País
        - Gráfico de Média de preços por casal x País

    - #### Visão Cidades:
        - Top 10 cidades com mais restaurantes na base de dados
        - Top 7 cidades com restaurantes com média acima de 4
        - Top 7 cidades com restaurantes com média abaixo de 2.5
        - Top 10 cidades com mais restaurantes com tipo culinário distintos

    - #### Visão Culinárias:
        - Melhores restaurantes por tipo de culinária
        - Top 10 melhores restaurantes
        - Top 10 melhores tipos de culinárias
        - Top 10 piores tipos de culinárias
    """
)

st.sidebar.markdown('### by Jooji Tani')
