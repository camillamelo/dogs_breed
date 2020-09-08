import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas
import plotly.express as px
import dash_table as dt
from django_plotly_dash import DjangoDash

from get_breed import models
from get_breed import serializers
import plotly.figure_factory as ff

import numpy as np

dev_data = 'C:/Users/cammy/OneDrive/MIT IA/git/projeto_dogs/dogs_brand/Data/Modeling/dev_results.jbl'
classes_file = 'C:/Users/cammy/OneDrive/MIT IA/git/projeto_dogs/dogs_brand/Data/Modeling/classes.jbl'



#with open(classes_file, 'rb') as f:
#    classes = pd.read_parquet(f, engine='pyarrow')
classes = pandas.read_parquet(classes_file)

# Training data
data = pandas.read_parquet(dev_data)

# Read operation data
# ALERTA: COMENTAR ANTES DE FAZER python manage.py migrate.
# DESCOMENTAR DEPOIS PARA FUNCIONAR CORRETAMENTE
pictures_list = models.Pictures.objects
pictures_data = serializers.PicturesSerializer(pictures_list, many=True)
pictures_table = pandas.DataFrame(pictures_data.data)

app = DjangoDash(
    "DogsDashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    # external_stylesheets=external_stylesheets
)

@app.callback([
    dash.dependencies.Output('image', 'src'),
    dash.dependencies.Output('real_breed', 'children'),
    dash.dependencies.Output('classification', 'children'),
    dash.dependencies.Output('estimated_score1', 'children'),
    dash.dependencies.Output('estimated_score2', 'children'),
    dash.dependencies.Output('estimated_score3', 'children')],
    [dash.dependencies.Input('image-dropdown', 'value')])

def update_image_src(value):
    return value[0], value[1], value[2], value[3], value[4], value[5]


def update_dash():

    # Read operation data
    # ALERTA: COMENTAR ANTES DE FAZER python manage.py migrate.
    # DESCOMENTAR DEPOIS PARA FUNCIONAR CORRETAMENTE
    pictures_list = models.Pictures.objects
    pictures_data = serializers.PicturesSerializer(pictures_list, many=True)
    pictures_table = pandas.DataFrame(pictures_data.data)

    hist_data = [pictures_table['estimated_score1'].values, data.estimated_score1.values]
    fig_dist = ff.create_distplot(hist_data, ['Menu Ofertado', 'Menu Referencia'],show_hist=False)
    ntop = 10

    app.layout = html.Div([
        dcc.Dropdown(
            id='image-dropdown',
            options=[{'label': i[0], 'value': i}  for i in pictures_table.values],
        value=pictures_table.values[0]
        ),
        html.Div([
            html.Table(
                html.Tr([
                    html.Td(html.Img(id='image')),
                    html.Td(
                        html.Table([
                            html.Tr([html.Td('Real Breed:'), html.Td(id='real_breed')]),
                            html.Tr([html.Td('Classification:'), html.Td(id='classification')]),
                            html.Tr([html.Td('Estimated Score:')]),
                            html.Tr([html.Td(classes.values[0]), html.Td(id='estimated_score1')]),
                            html.Tr([html.Td(classes.values[1]), html.Td(id='estimated_score2')]),
                            html.Tr([html.Td(classes.values[2]), html.Td(id='estimated_score3')]),
                        ])
                    )
                ])
            )
        ])
    ])


# if __name__ == '__main__':
#     app.run_server(debug=True)
