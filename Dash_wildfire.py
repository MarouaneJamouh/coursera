import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Créer l'application
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True  # Ne pas afficher les exceptions jusqu'à ce que le callback soit exécuté

# Lire les données sur les incendies dans un dataframe pandas
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

# Extraire l'année et le mois de la colonne Date
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month_name()  # Utilisé pour les noms des mois
df['Year'] = df['Date'].dt.year

# Section Layout de Dash
# Tâche 1 : Ajouter le titre au tableau de bord
app.layout = html.Div(children=[
    html.H1('Tableau de bord des incendies en Australie',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}),
    
    # Tâche 2 : Ajouter les éléments radio et un menu déroulant juste en dessous de la première division intérieure
    # Début de la division extérieure
    html.Div([
        # Première division intérieure pour ajouter un texte d'aide pour le choix de la région
        html.Div([
            html.H2('Sélectionnez la région :', style={'margin-right': '2em'}),
            
            # Éléments radio pour sélectionner la région
            dcc.RadioItems(
                options=[
                    {"label": "Nouvelle-Galles du Sud", "value": "NSW"},
                    {"label": "Territoire du Nord", "value": "NT"},
                    {"label": "Queensland", "value": "QL"},
                    {"label": "Australie-Méridionale", "value": "SA"},
                    {"label": "Tasmanie", "value": "TA"},
                    {"label": "Victoria", "value": "VI"},
                    {"label": "Australie-Occidentale", "value": "WA"}
                ],
                value="NSW", id='region', inline=True
            ),
            
            # Menu déroulant pour sélectionner l'année
            html.Div([
                html.H2('Sélectionnez l\'année :', style={'margin-right': '2em'}),
                dcc.Dropdown(
                    options=[{'label': year, 'value': year} for year in df['Year'].unique()],
                    value=2005, id='year'
                )
            ])
        ]),
        
        # Tâche 3 : Ajouter deux divisions vides pour les sorties à l'intérieur de la prochaine division intérieure
        # Deuxième division intérieure pour ajouter deux divisions internes pour les graphiques de sortie
        html.Div([
            html.Div([], id='plot1'),
            html.Div([], id='plot2')
        ], style={'display': 'flex'}),
    ])
    # Fin de la division extérieure
])

# Tâche 4 : Ajouter les composants de sortie et d'entrée à l'intérieur du décorateur @app.callback
@app.callback(
    [Output('plot1', 'children'),
     Output('plot2', 'children')],
    [Input('region', 'value'),
     Input('year', 'value')]
)
# Tâche 5 : Ajouter la fonction de rappel
def reg_year_display(input_region, input_year):
    # Filtrer les données selon la région sélectionnée et l'année
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]
    
    # Graphique 1 - Moyenne mensuelle de la surface estimée brûlée
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month',
                  title="{} : Moyenne mensuelle de la surface estimée brûlée en {}".format(input_region, input_year))
    
    # Graphique 2 - Moyenne mensuelle du nombre de pixels pour les incendies de végétation présumés
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x='Month', y='Count',
                  title='{} : Nombre moyen de pixels pour les incendies de végétation présumés en {}'.format(input_region, input_year))
    
    return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)]

# Lancer le serveur
if __name__ == '__main__':
    app.run_server(debug=True)
