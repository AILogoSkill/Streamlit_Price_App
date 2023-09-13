# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15PGGtTE4ut2OubmJkDYGexBsm2wRDZW8
"""

import pandas as pd
import streamlit as st
import seaborn as sns
import json
import joblib

st.header('House prices in city')
PATH_DATA = "data/all_v2.csv"
PATH_UNIQUE_VALUES = "data/unique_values.json"
PATH_MODEL = "models/lr_pipeline.sav"

@st.cache_data
def load_data(path):
  #Load data from path***
  data = pd.read_csv(path)
  #for demonstration
  data = data.sample(5898)
  return data

@st.cache_data
def load_model(path):
  #Load model from path
  model=joblib.load(PATH_MODEL)
  return model

@st.cache_data
def transform(data):
  #Transform data
  colors=sns.color_palette("coolwarm").as_hex()
  n_colors= len(colors)
  data = data.reset_index(drop=True)
  data["norm_price"] = data["price"] / data["area"]
  data["label_colors"] = pd.qcut(data["norm_price"], n_colors, labels=colors)
  data["label_colors"] = data["label_colors"].astype("str")
  return data
df = load_data(PATH_DATA)
df = transform(df)
st.write(df[:4])

st.map(data=df, latitude="geo_lat", longitude="geo_lon",colors="label_colors")

with open (PATH_UNIQUE_VALUES, "w") as file:
    dict_unique=json.dump(file)


#features
building_type = st.sidebar.selectbox('Building type', (dict_unique['building_type']))
object_type = st.sidebar.selectbox("Object type", (dict_unique["object_type"]))
level= st.sidebar.slider(
    "Level", min_values=min(dict_unique["level"]), max_value=max(dict_unique["level"])
)

levels= st.sidebar.slider(
    "Levels", min_values=min(dict_unique["levels"]), max_value=max(dict_unique["levels"])
)

rooms = st.sidebar.selectbox("Rooms", (dict_unique["rooms"]))
area = st.sidebar.slider(
    "Area", min_value=min(dict_unique["area"]), max_value=max(dict_unique["area"])
)
kitchen_area = st.sidebar.slider(
    "Kitchen area",
    min_value=min(dict_unique["kitchen_area"]),
    max_value=max(dict_unique["kitchen_area"])
)


dict_data = {
    "building_type": building_type,
    "object_type": object_type,
    "Level": level,
    "levels": levels,
    "room": rooms,
    "area": area,
    "kitchen_area": kitchen_area,
    }


data_predict = pd.DataFrame([dict_data])
model = load_model(PATH_MODEL)
buttom = st.button("Predict")

if buttom:
   output=model.predict(data_predict)[0]
   st.success(f'{round(output[8])} rub')
