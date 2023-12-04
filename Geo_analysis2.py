from flask import Flask, render_template
app = Flask(__name__)

import datashader as ds
import holoviews as hv
import geoviews as gv
from datashader import transfer_functions as tf
from datashader.colors import colormap_select  # Import colormap_select
from functools import partial
from datashader.utils import export_image
from colorcet import fire, rainbow, bgy, bjy, bkr, kb, kr
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import plotly.express as px
geo = pd.read_csv("olist_geolocation_dataset.csv", dtype={'geolocation_zip_code_prefix': str})
# Gets the first three and four first digits of zip codes, we will explore this further to understand how zip codes work
geo['geolocation_zip_code_prefix_1_digits'] = geo['geolocation_zip_code_prefix'].str[0:1]
geo['geolocation_zip_code_prefix_2_digits'] = geo['geolocation_zip_code_prefix'].str[0:2]
geo['geolocation_zip_code_prefix_3_digits'] = geo['geolocation_zip_code_prefix'].str[0:3]
geo['geolocation_zip_code_prefix_4_digits'] = geo['geolocation_zip_code_prefix'].str[0:4]
geo['geolocation_zip_code_prefix'].value_counts().to_frame().describe()
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
(geo.head(3))
geo['geolocation_zip_code_prefix'] = geo['geolocation_zip_code_prefix'].astype(int)
geo['geolocation_zip_code_prefix_1_digits'] = geo['geolocation_zip_code_prefix_1_digits'].astype(int)
geo['geolocation_zip_code_prefix_2_digits'] = geo['geolocation_zip_code_prefix_2_digits'].astype(int)
geo['geolocation_zip_code_prefix_3_digits'] = geo['geolocation_zip_code_prefix_3_digits'].astype(int)
geo['geolocation_zip_code_prefix_4_digits'] = geo['geolocation_zip_code_prefix_4_digits'].astype(int)
brazil = geo
agg_name = 'geolocation_zip_code_prefix'

import datashader as ds
from datashader import transfer_functions as tf
from functools import partial
from datashader.utils import export_image
from colorcet import rainbow
from datashader.colors import colormap_select

background = "black"
cm = partial(colormap_select, reverse=(background != "black"))
export = partial(export_image, background=background, export_path="export")

W = 700 
def create_plotly_map(data, title, color_column='geolocation_zip_code_prefix'):
    # Create a Plotly scatter plot
    fig = px.scatter(data, x='x', y='y', color=color_column, title=title,
                     labels={'geolocation_zip_code_prefix': 'Zip Code'},
                     opacity=0.7, size_max=5)
    
    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)
    return plot_html

def filter_data(level, name):
    df = geo[geo[level] == name]
    #remove outliers
    df = df[(df.x <= df.x.quantile(0.999)) & (df.x >= df.x.quantile(0.001))]
    df = df[(df.y <= df.y.quantile(0.999)) & (df.y >= df.y.quantile(0.001))]
    return df

sp = filter_data('geolocation_state', 'SP')
agg_name = 'geolocation_zip_code_prefix'
a= sp[agg_name].describe().to_frame()

@app.route('/')
def index():
    plot_html = create_plotly_map(sp, 'Map of Zip Codes in Sao Paulo State')
    return render_template('map2.html', a=a, plot_html=plot_html)
if __name__ == '__main__':
    app.run(port=5002)  # You can specify the port number here
