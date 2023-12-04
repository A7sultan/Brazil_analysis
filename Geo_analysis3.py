from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

geo = pd.read_csv("olist_geolocation_dataset.csv", dtype={'geolocation_zip_code_prefix': str})
geo['geolocation_zip_code_prefix_1_digits'] = geo['geolocation_zip_code_prefix'].str[0:1]
geo['geolocation_zip_code_prefix_2_digits'] = geo['geolocation_zip_code_prefix'].str[0:2]
geo['geolocation_zip_code_prefix_3_digits'] = geo['geolocation_zip_code_prefix'].str[0:3]
geo['geolocation_zip_code_prefix_4_digits'] = geo['geolocation_zip_code_prefix'].str[0:4]
geo = geo[geo.geolocation_lat <= 5.27438888]
geo = geo[geo.geolocation_lng >= -73.98283055]
geo = geo[geo.geolocation_lat >= -33.75116944]
geo = geo[geo.geolocation_lng <= -34.79314722]

from datashader.utils import lnglat_to_meters as webm
x, y = webm(geo.geolocation_lng, geo.geolocation_lat)
geo['x'] = pd.Series(x)
geo['y'] = pd.Series(y)
geo['geolocation_zip_code_prefix'] = geo['geolocation_zip_code_prefix'].astype(int)
geo['geolocation_zip_code_prefix_1_digits'] = geo['geolocation_zip_code_prefix_1_digits'].astype(int)
geo['geolocation_zip_code_prefix_2_digits'] = geo['geolocation_zip_code_prefix_2_digits'].astype(int)
geo['geolocation_zip_code_prefix_3_digits'] = geo['geolocation_zip_code_prefix_3_digits'].astype(int)
geo['geolocation_zip_code_prefix_4_digits'] = geo['geolocation_zip_code_prefix_4_digits'].astype(int)
agg_name = 'geolocation_zip_code_prefix'

def filter_data(level, name):
    df = geo[geo[level] == name]
    #remove outliers
    df = df[(df.x <= df.x.quantile(0.999)) & (df.x >= df.x.quantile(0.001))]
    df = df[(df.y <= df.y.quantile(0.999)) & (df.y >= df.y.quantile(0.001))]
    return df

saopaulo = filter_data('geolocation_city', 'sao paulo')
agg_name = 'geolocation_zip_code_prefix'
a= saopaulo[agg_name].describe().to_frame()


def create_plotly_map(data, label):
    fig = px.scatter(data, x='x', y='y', color='geolocation_zip_code_prefix',
                     labels={'geolocation_zip_code_prefix': 'Zip Code'},
                     title=label,
                     opacity=0.7, size_max=5)
    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)
    return plot_html

@app.route('/')
def index():
    plot_html = create_plotly_map(saopaulo, 'Map of Zip Codes in Sao Paulo State')
    return render_template('map3.html', a=a, plot_html=plot_html)

if __name__ == '__main__':
    app.run(port=5003)
