import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px

######################### CARREGA O DATAFRAME (Chamados.csv) #########################
df = pd.read_csv("Chamados.csv", encoding='latin1')

# Formata as datas para o padrão brasileiro
df['DATA DE ABERTURA'] = pd.to_datetime(df['DATA DE ABERTURA'], format='%d/%m/%Y')

# Mapeia os meses (para o gráfico de linhas por mês)
meses_em_portugues = {
    1: '01/2024',
    2: '02/2024',
    3: '03/2024',
    4: '04/2024',
    5: '05/2024',
    6: '06/2024',
    7: '07/2024',
    8: '08/2024',
    9: '09/2024',
    10: '10/2024',
    11: '11/2024',
    12: '12/2024'
}

# Extrair o mês da data de abertura e converter para nome do mês em português
df['Mês de Abertura'] = df['DATA DE ABERTURA'].dt.month.map(meses_em_portugues)

# Função para calcular o total de chamados, chamados resolvidos e chamados não resolvidos
def calcular_totais(df_filtrado):
    total_chamados = len(df_filtrado)
    total_resolvidos = df_filtrado['RESOLVIDO?'].astype(str).str.lower().eq('sim').sum()
    total_nao_resolvidos = total_chamados - total_resolvidos
    return total_chamados, total_resolvidos, total_nao_resolvidos

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

######################### Layout do Dashboard #########################
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Chamados'),

# Botão retrátil para mostrar/ocultar filtro
    html.Button('Mostrar Filtro', id='botao-filtro'),

# Div para o filtro retrátil
    html.Div(id='filtro-container', style={'display': 'none'}, children=[
# Menu retrátil para as opções de filtro
        html.Div([
            html.Label('Filtrar por categoria:'),
            dcc.RadioItems(
                id='filtro-categoria',
                options=[
                    {'label': 'Todas', 'value': 'Todas'},
                    {'label': 'Autenticação', 'value': 'Autenticacao'},
                    {'label': 'Arquivo', 'value': 'Arquivo'},
                    {'label': 'Marcação', 'value': 'Marcacao'},
                    {'label': 'Visualização', 'value': 'Visualizacao'},
                    {'label': 'Cálculo', 'value': 'Calculo'},
                    {'label': 'Cadastro', 'value': 'Cadastro'},
                    {'label': 'Comunicação', 'value': 'Comunicacao'},
                    {'label': 'Funcionalidade', 'value': 'Funcionalidade'}
                ],
                value='Todas',
                labelStyle={'display': 'block'}
            ),
            html.Br(),
            html.Label('Filtrar por plataforma:'),
            dcc.RadioItems(
                id='filtro-plataforma',
                options=[
                    {'label': 'Todas', 'value': 'Todas'},
                    {'label': 'Web', 'value': 'Web'},
                    {'label': 'Mobile', 'value': 'Mobile'},
                    {'label': 'Ambos', 'value': 'Ambos'}
                ],
                value='Todas',
                labelStyle={'display': 'block'}
            ),
            html.Br(),
            html.Button('Filtrar', id='botao-filtrar', n_clicks=0)
        ], className='sidebar')
    ]),

# Container para os totais
    html.Div(className='total-container', children=[
# Caixas de texto para os totais
        html.Div(id='total-chamados', className='total-box'),
        html.Div(id='total-resolvidos', className='total-box'),
        html.Div(id='total-nao-resolvidos', className='total-box')
    ]),

# Container para os Gráficos
    html.Div(id='graficos', className='graphs-container')
], className='container')



######################### PARTE DE INTERAÇÃO/INPUT/OUTPUT #########################

#mostrar/ocultar filtro ao clicar no botão
@app.callback(
    Output('filtro-container', 'style'),
    [Input('botao-filtro', 'n_clicks')],
    [State('filtro-container', 'style')]
)
def toggle_filtro(n_clicks, style):
    if n_clicks and n_clicks % 2 == 1:
        style['display'] = 'block'
    else:
        style['display'] = 'none'
    return style

#atualiza os gráficos e os totais quando o botão de filtrar for clicado
@app.callback(
    [Output('graficos', 'children'),
     Output('total-chamados', 'children'),
     Output('total-resolvidos', 'children'),
     Output('total-nao-resolvidos', 'children')],
    [Input('botao-filtrar', 'n_clicks')],
    [State('filtro-categoria', 'value'),
     State('filtro-plataforma', 'value')]
)
def atualizar_graficos_e_totais(n_clicks, categoria, plataforma):
    if n_clicks == 1:
        df_filtrado = df
    else:
        df_filtrado = df.copy()
        if categoria != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['CATEGORIA'] == categoria]
        if plataforma != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['PLATAFORMA'] == plataforma]

# Calcula totais
    total_chamados, total_resolvidos, total_nao_resolvidos = calcular_totais(df_filtrado)



######################### PARTE DE GRÁFICOS #########################

# Paleta de cores dos gráficos
    blue_palette = ['#004c6d','#32607e','#517590','#6e8ba1','#8aa1b4','#a7b8c6','#c4cfd9','#e1e7ec','#ffffff']

# Atualizar gráficos
    graficos = [
        dcc.Graph(
            id='chamados-por-categoria',
            figure=px.pie(df_filtrado, names='CATEGORIA', title='Chamados por Categoria',color_discrete_sequence=blue_palette)
        ),
        dcc.Graph(
            id='chamados-por-plataforma',
            figure=px.pie(df_filtrado, names='PLATAFORMA', title='Chamados por Plataforma',color_discrete_sequence=blue_palette)
        ),
        dcc.Graph(
            id='resolvido',
            figure=px.histogram(df_filtrado, x='RESOLVIDO?', color='RESOLVIDO?', barmode='group', title='Resolvidos x não resolvidos', color_discrete_sequence=blue_palette)
        ),
        dcc.Graph(
            id='abertura-chamados-mes',
            figure=px.line(df_filtrado.groupby('Mês de Abertura').size().reset_index(name='Número de Chamados'), x='Mês de Abertura', y='Número de Chamados', title='Abertura de chamados por mês', markers=True, color_discrete_sequence=blue_palette)
        )
    ]



######################### ATUALIZA OS CONTEÚDOS EXIBIDOS #########################
    return graficos, f"{total_chamados} Chamados", f"{total_resolvidos} Resolvidos", f"{total_nao_resolvidos} Não Resolvidos"



######################### EXECUTA O APLICATIVO #########################
if __name__ == '__main__':
    app.run_server(debug=True)