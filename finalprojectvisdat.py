#!/usr/bin/env python
# coding: utf-8

# In[1]:
# Library

import streamlit as st

import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6

def main():
    # Menambahkan informasi teks
    st.title("Final Project Visualisasi Data dengan Bokeh dan Streamlit Deployment")
    st.header('Anggota')
    st.subheader('M. Aldi Haryojudanto - 1301194025')
    st.subheader('Andri Zefrinaldi - 1301204255')


    
    
    
    # In[2]:
    # Read dataset

    negara = ['Indonesia', 'Singapore', 'Malaysia', 'Vietnam', 'Thailand', 'Philippines']

    data = pd.read_csv("./data/cause_of_deaths.csv")
    data = data[data['Country/Territory'].isin(negara)]
    data.rename(columns={"Country/Territory": "Country"}, inplace=True)
    data.set_index('Year', inplace=True)


    
    
    
    # In[3]:
    # Membuat list sesuai Kolom Location dengan melakukan filter menggunakan unique dan mapping warna

    country_list = data.Country.unique().tolist()
    color_mapper = CategoricalColorMapper(factors=country_list, palette=Spectral6)


    
    
    
    # In[4]:
    # Membuat slider untuk tahun
    slider = st.slider("Year", 1990, 2019, value=1990, step=1)
    # membuat dropdown/selectbox untuk x
    x_select = st.selectbox(label='x-axis data',options=['Malaria', 'Drowning', 'Poisonings', 'Chronic Respiratory Diseases'], key="x-axis")
#     st.write('X Values:', x_select)
    # membuat dropdown/selectbox untuk y
    y_select = st.selectbox(label='y-axis data',options=['Malaria', 'Drowning', 'Poisonings', 'Chronic Respiratory Diseases'], key="y-axis", index=1)
#     st.write('Y Values:', y_select)

    # Membuat ColumnDataSource: source
    source = ColumnDataSource(data={
        'x'       : data.loc[slider].Malaria,
        'y'       : data.loc[slider].Drowning,
        'country' : data.loc[slider].Country,
    })


    
    
    
    # In[5]:
    # Visualisasi dengan menggunakan plot

    plot = figure(title="Death Cause "+str(slider), x_axis_label=str(x_select), y_axis_label=str(y_select),
                toolbar_location='right')
    
    # Menambahkan tools hover (muncul catatan ketika cursor diarahkan pada titik)
    plot.add_tools(HoverTool(tooltips=[('Country', '@country'),(x_select,'@x'),(y_select,'@y')]))

    # Tambah titik pada plot sesuai x dan y
    plot.circle(x='x', y='y', source=source, fill_alpha=0.9,
               color=dict(field='country', transform=color_mapper), legend_field='country')
    
    # Menambahan informasi kotak legend pada bottom_left
    plot.legend.location = 'bottom_left'

    st.bokeh_chart(plot)

if __name__ == '__main__':
    main()