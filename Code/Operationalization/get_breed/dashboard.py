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

# app.layout = html.Div([
#     dcc.Dropdown(
#         id='image-dropdown',
#         options=[{'label': i[0], 'value': i}  for i in pictures_table.values],
#     value=pictures_table.values[0]
#     ),
#     html.Div([
#         html.Img(id='image'),
#         dt.DataTable(id='data-table', columns=[
#             {'name': 'Real breed', 'id': 'real_breed'},
#             {'name': 'Classification', 'id': 'classification'},
#             {'name': 'Estimated Score', 'id': 'estimated_score'}
#         ])
#     ])
#
# #    dcc.Graph()
# ])

@app.callback([
    dash.dependencies.Output('image', 'src'),
    dash.dependencies.Output('real_breed', 'children'),
    dash.dependencies.Output('classification', 'children'),
    dash.dependencies.Output('estimated_score', 'children')],
    [dash.dependencies.Input('image-dropdown', 'value')])

def update_image_src(value):
    return value[0], value[1], value[2], value[3]


def update_dash():

    # hist_data = [pictures_table['estimated_score'].values, data.estimated_score.values]
    # fig_dist = ff.create_distplot(hist_data, ['Menu Ofertado', 'Menu Referencia'],show_hist=False)
    # ntop = 10

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
                            html.Tr([html.Td('Estimated Score:'), html.Td(id='estimated_score')]),
                        ])
                    )
                ])
            )
        ])
    ])


# if __name__ == '__main__':
#     app.run_server(debug=True)
