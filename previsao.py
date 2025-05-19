### app.py
import streamlit as st
from weather import get_weather_forecast
from utils import plot_weather

st.set_page_config(page_title="Previsão do Tempo", layout="centered")

st.title("\ud83c\udf26\ufe0f Previsão do Tempo")

city = st.text_input("Digite o nome da cidade:", "São Paulo")

if city:
    forecast = get_weather_forecast(city)
    if forecast:
        st.write(f"Previsão para **{city}** nos próximos dias:")
        plot_weather(forecast)
    else:
        st.error("Cidade não encontrada ou erro na API.")


### weather.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=pt_br"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = [{
            'data': item['dt_txt'],
            'temp': item['main']['temp'],
            'descricao': item['weather'][0]['description']
        } for item in data['list'][:10]]  # reduzido para 10 entradas
        return forecast
    return None


### utils.py
import pandas as pd
import plotly.express as px
import streamlit as st

def plot_weather(forecast):
    df = pd.DataFrame(forecast)
    fig = px.line(df, x='data', y='temp', title='Temperatura nos próximos dias', markers=True, text='descricao')
    fig.update_traces(textposition='top center')
    fig.update_layout(xaxis_title="Data", yaxis_title="Temperatura (°C)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)


