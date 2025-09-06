import streamlit as st
import pandas as pd
import altair as alt

# 1. 제목 설정
st.title("물체의 움직임 분석: 속도-시간 그래프")

# CSV 파일 불러오기
# 'positions_and_velocities.csv' 파일을 pandas DataFrame으로 읽어옵니다.
try:
    df = pd.read_csv("positions_and_velocities.csv")
except FileNotFoundError:
    st.error("`positions_and_velocities.csv` 파일을 찾을 수 없습니다. 파일이 올바른 위치에 있는지 확인해 주세요.")
    st.stop()

# 시간(Time) 열 추가
# 데이터프레임의 인덱스를 '시간(Time)'으로 사용합니다.
df['Time'] = df.index

# 데이터 전처리
# V1, V2, V3 속도 데이터만 남깁니다.
df_velocities = df[['Time', 'V1', 'V2', 'V3']]

# 데이터프레임을 Long Format으로 변환
# Altair에서 다중 선 그래프를 그리기 위해 데이터를 재구성합니다.
df_long = pd.melt(df_velocities, id_vars=['Time'], var_name='Velocity_Component', value_name='Velocity')

# 5. 속도-시간 그래프 만들기
st.subheader("속도-시간 그래프")
st.write("세 물체의 속도 변화를 시간에 따라 보여줍니다.")

chart = alt.Chart(df_long).mark_line().encode(
    x=alt.X('Time', title='시간 (단위: 프레임 또는 단계)'),
    y=alt.Y('Velocity', title='속도'),
    color=alt.Color('Velocity_Component', title='속도 성분'),
    tooltip=['Time', 'Velocity_Component', 'Velocity']
).properties(
    title='물체별 속도 변화'
).interactive() # 사용자가 그래프를 확대/축소할 수 있게 만듭니다.

st.altair_chart(chart, use_container_width=True)
