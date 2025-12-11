import streamlit as st 
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data   #데이터를 캐싱(저장)해서 불필요한 재계산을 막아주는 데코레이터
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data = data.dropna(how="any", axis=0)
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

st.subheader('Raw data 5 lines preview')
st.write(data.head())


###히스토그램###
st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)


### 지도에 표시하기###
#1. st.map()
'''
st.map() : 지도에 표시됨
- 데이터프레임에 lat (위도)와 lon (경도)라는 이름의 컬럼이 있어야 합니다.
- 컬럼명은 반드시 lat, lon으로 맞춰야 Streamlit이 인식합니다. (대소문자 구분 O)
'''
st.subheader('Map of all pickups')
st.map(data)

# hour_to_filter = 17
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


#2. st.pydeck_chart
#어렵다..! 

### st.checkbox ###


