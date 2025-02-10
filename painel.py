import os
import requests
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

st.set_page_config(
    page_title="Ligas",
    page_icon="🏃🏼",
    layout="wide"
)

st.markdown('# Análise de Ligas Por Temporada')

# URL do certificado
url_certificado = "https://letsencrypt.org/certs/isrgrootx1.pem"  # Substitua pelo link correto

# Caminho para salvar o certificado temporariamente
# caminho_certificado_temp = '/tmp/certificado.pem'
caminho_certificado_temp = r"C:\Users\RAYSON\cer\isrgrootx1.pem"

# Baixar o certificado se necessário
if not os.path.exists(caminho_certificado_temp):
    try:
        response = requests.get(url_certificado)
        response.raise_for_status()  # Verifica se o download foi bem-sucedido
        with open(caminho_certificado_temp, 'wb') as file:
            file.write(response.content)
        st.write("Certificado baixado com sucesso.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao baixar o certificado: {e}")

# Função para carregar os dados do banco de dados
def load_data():
    # Informações de conexão e caminho do certificado
    username = 'root'
    password = 'FomFAYykiMbEFBR15ahPbuPcPiaN1lq2'
    host = '3il9oh.stackhero-network.com'
    port = 6454
    database = 'BD_Anos_Consolidados'

    # Configurações SSL
    ssl_args = {
        'ssl': {
            'ca': caminho_certificado_temp  # Use o caminho local do certificado
        }
    }

# caminho_certificado_temp

    # Criar a engine de conexão com o banco de dados
    engine = create_engine(
        f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}',
        connect_args=ssl_args
    )

    df_liga_anos = pd.read_sql_table('t_ligas_anos', con=engine)
    df_times_anos = pd.read_sql_table('t_times_anos', con=engine)

    return df_liga_anos, df_times_anos

# Carregar os dados
try:
    df_liga_anos, df_times_anos = load_data()
    # Exibir os dados
    st.dataframe(df_liga_anos)
    st.dataframe(df_times_anos)
except Exception as e:
    st.error(f"Erro ao carregar os dados do banco: {e}")