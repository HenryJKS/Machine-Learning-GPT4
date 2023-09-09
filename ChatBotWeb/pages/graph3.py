import time

import dash
import pandas as pd
from dash import html, dcc, Output, Input, State, callback
import dash_bootstrap_components as dbc
from ChatBotWeb.components import navbar
from ChatBotWeb.query.queryVeiculoProblema import df
from ChatBotWeb.chatAPI.ModelAPI import chat_analise_veiculo

NAVBAR = navbar.create_navbar()

pd.set_option('display.max_columns', None)

dash.register_page(
    __name__,
    name='Dashboard',
    path='/graph3',
    top_navbar=True,
)

layout = dbc.Container([

    dbc.Row([
        NAVBAR
    ]),

    html.Div([
        html.H2('Veículos com Problemas', className='text-center mt-2')
    ]),

    html.Div([
        html.Hr()
    ]),

    html.Div([
        html.P('Selecione o veículo: '),
        dcc.Dropdown(
            id='modelo-dropdown',
            options=[{'label': modelo, 'value': modelo} for modelo in df['MODELO'].unique()],
            value=df['MODELO'][0],
            multi=False,
        ),
    ], style={'width': '25%'}),

    html.Div([
        html.Div([], id='problemas-card')
    ], className='mt-2'),

    html.Div([
        dbc.Button("FordBot", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            html.Div([
                html.H4('Converse com o Bot', className='text-center'),
                html.Hr(),
                html.H6('Faça sua pergunta:', className='mt-2'),
                dcc.Textarea(style={'width': '100%'}, id='question'),
                html.Button('Perguntar', id='send-question', className='btn btn-secondary'),
                html.Div([
                ], className='mt-4', id='response-problem')
            ]),
            id="offcanvas",
            is_open=False,
            placement='end'
        ),
    ], className='mt-2'),

], fluid=True)


@callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@callback(
    Output('problemas-card', 'children'),
    Input('modelo-dropdown', 'value')
)
def update_problemas_card(selected_modelo):
    if selected_modelo is None:
        return ''

    problemas_modelo = df[df['MODELO'] == selected_modelo]['PROBLEMA'].unique()

    cliente = df[df['MODELO'] == selected_modelo]['CLIENTE'].unique()

    km_rodado = df[df['MODELO'] == selected_modelo]['KM'].unique()

    problemas_lista = problemas_modelo.tolist()

    # Cria uma string com os problemas separados por vírgula
    problemas_texto = ', '.join(problemas_lista)

    return dbc.Card([
        dbc.CardHeader('Relatório do Modelo'),
        dbc.CardBody([
            html.P(f'Modelo: {selected_modelo}'),
            html.P(f'Problemas Encontrados: {problemas_texto}'),
            html.P(f'Cliente: {cliente[0]}'),
            html.P(f'Quilometragem: {km_rodado[0]}km')
        ])
    ])


@callback(Output('response-problem', 'children'),
          Input('send-question', 'n_clicks'),
          State('question', 'value'))
def response(n_clicks, question):
    if not n_clicks:
        return dash.no_update
    elif n_clicks is None:
        return dash.no_update

    resposta = chat_analise_veiculo(f"dados: {df}, pergunta: {question}")

    # print(f"dados: {df}, pergunta: {question}")

    if question is None:
        return (
            html.P('Insira um pergunta', className='text-center border border-dark rounded', style={'padding': '2%'})
        )
    return (
        html.P(resposta, className='text-center border border-dark rounded', style={'padding': '2%'})
    )
