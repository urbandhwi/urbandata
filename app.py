%%writefile app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")

st.title('🌎 COVID-19 데이터 대시보드 - 시계열 분석')

@st.cache_data
def load_data():
    file_path = 'covid_19_clean_complete.csv'
    if not os.path.exists(file_path):
        st.error(
            "'covid_19_clean_complete.csv' 파일을 찾을 수 없습니다.\n\n"
            "이 앱을 배포하기 전에 Kaggle에서 'imdevskp/corona-virus-report' 데이터셋을 다운로드하여\n"
            "`covid_19_clean_complete.csv` 파일을 `app.py` 파일과 같은 디렉토리에 넣어주세요."
        )
        st.stop()
    
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df_corona_app = load_data()

if df_corona_app is not None:
    st.sidebar.title('설정')
    
    countries = ['전체 세계'] + sorted(df_corona_app['Country/Region'].unique().tolist())
    selected_country = st.sidebar.selectbox('국가 선택:', countries)

    # Filter and aggregate data based on selection
    if selected_country == '전체 세계':
        df_display = df_corona_app.groupby('Date').agg({
            'Confirmed': 'sum',
            'Deaths': 'sum',
            'Recovered': 'sum',
            'Active': 'sum'
        }).reset_index()
        title_prefix = '전 세계'
    else:
        df_display = df_corona_app[df_corona_app['Country/Region'] == selected_country]
        df_display = df_display.groupby('Date').agg({
            'Confirmed': 'sum',
            'Deaths': 'sum',
            'Recovered': 'sum',
            'Active': 'sum'
        }).reset_index()
        title_prefix = selected_country

    # Create the time series plot
    fig = px.line(
        df_display,
        x='Date',
        y=['Confirmed', 'Deaths', 'Recovered', 'Active'],
        title=f'<b>{title_prefix} COVID-19 확진, 사망, 회복, 활동 사례 추이</b>',
        labels={'value': '환자 수', 'variable': '사례 유형'},
        hover_data={'value': ':,.0f'}
    )

    fig.update_layout(
        hovermode='x unified',
        xaxis_title='날짜',
        yaxis_title='환자 수',
        legend_title_text='유형'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"### 현재 선택된 국가: **{selected_country}**")

    st.sidebar.markdown("--- 이 앱은 COVID-19 데이터를 시각화합니다. --- ")
    st.sidebar.markdown("**데이터 출처:** imdevskp/corona-virus-report (Kaggle)")
