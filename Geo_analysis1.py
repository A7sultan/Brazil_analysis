import numpy as np
from flask import Flask, render_template, url_for
import pandas as pd 
import os
import io
import base64
import matplotlib.pyplot as plt
import plotly.express as px 


app = Flask(__name__)

@app.route('/')
def index():

      geo = pd.read_csv("olist_geolocation_dataset.csv", dtype={'geolocation_zip_code_prefix': str})

      # Gets the first three and four first digits of zip codes, we will explore this further to understand how zip codes work
      geo['geolocation_zip_code_prefix_1_digits'] = geo['geolocation_zip_code_prefix'].str[0:1]
      geo['geolocation_zip_code_prefix_2_digits'] = geo['geolocation_zip_code_prefix'].str[0:2]
      geo['geolocation_zip_code_prefix_3_digits'] = geo['geolocation_zip_code_prefix'].str[0:3]
      geo['geolocation_zip_code_prefix_4_digits'] = geo['geolocation_zip_code_prefix'].str[0:4]
      a= (geo.head(3))
      b= (geo['geolocation_zip_code_prefix'].value_counts().to_frame().describe())
# Removing some outliers
# Brazil's most Northern spot is at 5 deg 16′ 27.8″ N latitude.
      geo = geo[geo.geolocation_lat <= 5.27438888]
# Its most Western spot is at 73 deg, 58′ 58.19″W Long.
      geo = geo[geo.geolocation_lng >= -73.98283055]
# Its most southern spot is at 33 deg, 45′ 04.21″ S Latitude.
      geo = geo[geo.geolocation_lat >= -33.75116944]
# Its most Eastern spot is 34 deg, 47′ 35.33″ W Long.
      geo = geo[geo.geolocation_lng <= -34.79314722]

      from datashader.utils import lnglat_to_meters as webm
      x, y = webm(geo.geolocation_lng, geo.geolocation_lat)
      geo['x'] = pd.Series(x)
      geo['y'] = pd.Series(y)
      c= (geo.head(3))
      geo['geolocation_zip_code_prefix'] = geo['geolocation_zip_code_prefix'].astype(int)
      geo['geolocation_zip_code_prefix_1_digits'] = geo['geolocation_zip_code_prefix_1_digits'].astype(int)
      geo['geolocation_zip_code_prefix_2_digits'] = geo['geolocation_zip_code_prefix_2_digits'].astype(int)
      geo['geolocation_zip_code_prefix_3_digits'] = geo['geolocation_zip_code_prefix_3_digits'].astype(int)
      geo['geolocation_zip_code_prefix_4_digits'] = geo['geolocation_zip_code_prefix_4_digits'].astype(int)
      brazil = geo
      agg_name = 'geolocation_zip_code_prefix'
      d= brazil[agg_name].describe().to_frame()

      # Plotting with Plotly Express
      fig = px.scatter(geo, x='x', y='y', color='geolocation_zip_code_prefix',
                     labels={'geolocation_zip_code_prefix': 'Zip Code'},
                     title='Map of Zip Codes in Brazil',
                     opacity=0.7, size_max=5)
      

      # Convert the Plotly figure to HTML
      plot_html = fig.to_html(full_html=False)     

      return render_template('map1.html', a=a, b=b, c=c, d=d, plot_html=plot_html)

if __name__ == '__main__':
    app.run(port=5001)
