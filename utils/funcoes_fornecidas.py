import inflection
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


# função para nomear os países conforme seu id
def country_names(country_id):
    return COUNTRIES[country_id]

# lista de id com seu respectivo país
COUNTRIES = {
    1: 'India',
    14: 'Australia',
    30: 'Brazil',
    37: 'Canada',
    94: 'Indonesia',
    148: 'New Zealand',
    162: 'Philippines',
    166: 'Qatar',
    184: 'Singapure',
    189: 'South Africa',
    191: 'Sri Lanka',
    208: 'Turkey',
    214: 'United Arab Emirates',
    215: 'England',
    216: 'United States of America'
}

# função para classificar os preços 
def create_price_type(price_range):
    if price_range == 1:
        return 'cheap'
    elif price_range == 2:
        return 'normal'
    elif price_range == 3:
        return 'expensive'
    else:
        return 'gourmet'

# função para nomear as cores dado os seus códigos
def color_name(color_code):
    return COLORS[color_code]

COLORS = {
    '3F7E00':'darkgreen',
    '5BA829':'green',
    '9ACD32':'lightgreen',
    'CDD614':'orange',
    'FFBA00':'red',
    'CBCBC8':'darkred',
    'FF7800':'darkred'
}

# função para renomear as colunas para o padrão snakecase
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    
    return df


def clean_code(df):
    # Eliminando dados duplicados
    df.drop_duplicates(inplace=True)
    # Eliminando dados faltantes
    df.dropna(inplace=True)
    # Excluindo coluna com apenas um valor (irrelevante para a análise)
    df.drop('Switch to order menu', axis = 1, inplace = True)
    # Renomeando colunas para padrão snakecase
    df = rename_columns(df)
    # Mudar para apenas uma categoria de culinária para facilitar o estudo
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
    # Criando coluna de categoria de faixa de preços
    df["price_type"] = df.loc[:, "price_range"].apply(lambda x: create_price_type(x))
    # Criando coluna países 
    df["country"] = df.loc[:, "country_code"].apply(lambda x: country_names(x))
    # Criando coluna de cores
    df["color_name"] = df.loc[:, "rating_color"].apply(lambda x: color_name(x))

    # Remover culinárias onde a média de avaliações é igual a zero
    df = df.drop(df[(df["cuisines"] == "Drinks Only")].index)
    df = df.drop(df[(df["cuisines"] == "Mineira")].index)

    return df

def country_maps(df):

    map = folium.Map()

    # for index, location_info in df.iterrows():
    #     folium.Marker([location_info['latitude'],
    #                 location_info['longitude']]).add_to(map)

    marker_cluster = MarkerCluster().add_to(map)

    for index, line in df.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggregate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(map, width=1024, height=600)


    

