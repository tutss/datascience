import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import folium
from folium import plugins
from branca.element import MacroElement
from jinja2 import Template

from generate_insights import load_and_preprocess_data


def get_crime_color(crime_type):
    crime_categories = {
        'FURTO - OUTROS': '#3388ff',
        'FURTO DE VEÍCULO': '#0066cc',
        'FURTO DE CARGA': '#004d99',
        'ROUBO - OUTROS': '#ff4444',
        'ROUBO DE VEÍCULO': '#cc0000',
        'ROUBO DE CARGA': '#990000',
        'ROUBO A BANCO': '#660000',
        'HOMICÍDIO DOLOSO': '#8b0000',
        'LATROCÍNIO': '#660000',
        'TENTATIVA DE HOMICÍDIO': '#b22222',
        'LESÃO CORPORAL SEGUIDA DE MORTE': '#8b0000',
        'HOMICÍDIO CULPOSO POR ACIDENTE DE TRÂNSITO': '#cd5c5c',
        'HOMICÍDIO CULPOSO OUTROS': '#cd5c5c',
        'HOMICÍDIO DOLOSO POR ACIDENTE DE TRÂNSITO': '#8b0000',
        'ESTUPRO': '#800080',
        'ESTUPRO DE VULNERÁVEL': '#4b0082',
        'LESÃO CORPORAL DOLOSA': '#ff8c00',
        'LESÃO CORPORAL CULPOSA POR ACIDENTE DE TRÂNSITO': '#ffa500',
        'LESÃO CORPORAL CULPOSA - OUTRAS': '#ffb84d',
        'TRÁFICO DE ENTORPECENTES': '#228b22',
        'PORTE DE ENTORPECENTES': '#32cd32',
        'APREENSÃO DE ENTORPECENTES': '#90ee90',
        'EXTORSÃO MEDIANTE SEQUESTRO': '#8b008b',
        'PORTE DE ARMA': '#696969',
    }
    return crime_categories.get(crime_type, '#808080')


def get_crime_category(crime_type):
    if 'FURTO' in crime_type:
        return 'Furtos'
    elif 'ROUBO' in crime_type:
        return 'Roubos'
    elif any(x in crime_type for x in ['HOMICÍDIO', 'LATROCÍNIO', 'TENTATIVA DE HOMICÍDIO', 'LESÃO CORPORAL SEGUIDA DE MORTE']):
        return 'Crimes violentos'
    elif 'ESTUPRO' in crime_type:
        return 'Crimes sexuais'
    elif 'ENTORPECENTES' in crime_type:
        return 'Drogas'
    else:
        return 'Outros'


def create_popup_html(row):
    hora_formatada = 'N/A'
    if pd.notna(row.get('HORA_OCORRENCIA_BO')):
        try:
            hora_formatada = pd.to_datetime(row['HORA_OCORRENCIA_BO']).strftime('%H:%M:%S')
        except:
            hora_formatada = str(row['HORA_OCORRENCIA_BO'])

    popup_html = f"""
    <div style="font-family: Arial; font-size: 12px; width: 250px;">
        <h4 style="margin: 0 0 10px 0; color: #333;">{row['NATUREZA_APURADA']}</h4>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 3px; border-bottom: 1px solid #ddd;"><b>Data:</b></td>
                <td style="padding: 3px; border-bottom: 1px solid #ddd;">{row['DATA_OCORRENCIA_BO'].strftime('%d/%m/%Y')}</td></tr>
            <tr><td style="padding: 3px; border-bottom: 1px solid #ddd;"><b>Hora:</b></td>
                <td style="padding: 3px; border-bottom: 1px solid #ddd;">{hora_formatada}</td></tr>
            <tr><td style="padding: 3px; border-bottom: 1px solid #ddd;"><b>Bairro:</b></td>
                <td style="padding: 3px; border-bottom: 1px solid #ddd;">{row['BAIRRO'].title()}</td></tr>
            <tr><td style="padding: 3px; border-bottom: 1px solid #ddd;"><b>Logradouro:</b></td>
                <td style="padding: 3px; border-bottom: 1px solid #ddd;">{row['LOGRADOURO'][:50]}</td></tr>
            <tr><td style="padding: 3px;"><b>Delegacia:</b></td>
                <td style="padding: 3px;">{row['NOME_DELEGACIA']}</td></tr>
        </table>
    </div>
    """
    return popup_html


def filter_by_time_period(data, period):
    if 'HOUR_OF_DAY' not in data.columns or data['HOUR_OF_DAY'].isna().all():
        return data

    hourly_data = data.dropna(subset=['HOUR_OF_DAY'])

    if period == 'manhã':
        return hourly_data[(hourly_data['HOUR_OF_DAY'] >= 6) & (hourly_data['HOUR_OF_DAY'] < 12)]
    elif period == 'tarde':
        return hourly_data[(hourly_data['HOUR_OF_DAY'] >= 12) & (hourly_data['HOUR_OF_DAY'] < 18)]
    elif period == 'noite':
        return hourly_data[((hourly_data['HOUR_OF_DAY'] >= 18) & (hourly_data['HOUR_OF_DAY'] < 24)) |
                          ((hourly_data['HOUR_OF_DAY'] >= 0) & (hourly_data['HOUR_OF_DAY'] < 6))]
    return data


def sample_data_for_performance(data, max_points=5000):
    if len(data) <= max_points:
        return data
    return data.sample(n=max_points, random_state=42)


def fit_map_to_bounds(crime_map, data_with_coords, padding=0.02):
    min_lat = data_with_coords['LATITUDE'].min()
    max_lat = data_with_coords['LATITUDE'].max()
    min_lon = data_with_coords['LONGITUDE'].min()
    max_lon = data_with_coords['LONGITUDE'].max()

    lat_padding = (max_lat - min_lat) * padding
    lon_padding = (max_lon - min_lon) * padding

    bounds = [
        [min_lat - lat_padding, min_lon - lon_padding],
        [max_lat + lat_padding, max_lon + lon_padding]
    ]

    crime_map.fit_bounds(bounds)
    return crime_map


def create_layered_crime_map(data, output_path, year):
    data_with_coords = data[data['HAS_VALID_COORDS']].copy()

    if len(data_with_coords) == 0:
        print("    AVISO: Nenhum dado com coordenadas válidas")
        return

    center_lat = data_with_coords['LATITUDE'].mean()
    center_lon = data_with_coords['LONGITUDE'].mean()

    crime_map = folium.Map(
        location=[center_lat, center_lon],
        tiles='OpenStreetMap'
    )

    fit_map_to_bounds(crime_map, data_with_coords)

    categories = data_with_coords.groupby(data_with_coords['NATUREZA_APURADA'].apply(get_crime_category))

    for category_name, category_data in categories:
        feature_group = folium.FeatureGroup(name=category_name)

        sampled_data = sample_data_for_performance(category_data, max_points=2000)

        for idx, row in sampled_data.iterrows():
            folium.CircleMarker(
                location=[row['LATITUDE'], row['LONGITUDE']],
                radius=4,
                popup=folium.Popup(create_popup_html(row), max_width=300),
                color=get_crime_color(row['NATUREZA_APURADA']),
                fill=True,
                fillColor=get_crime_color(row['NATUREZA_APURADA']),
                fillOpacity=0.7,
                opacity=0.8
            ).add_to(feature_group)

        feature_group.add_to(crime_map)

    folium.LayerControl(collapsed=False).add_to(crime_map)

    title_html = f'''
    <div style="position: fixed;
                top: 10px; left: 50px; width: 500px; height: 60px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:16px; padding: 10px; border-radius: 5px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
        <h4 style="margin: 0;">Mapa de crimes por categoria - São Paulo {year}</h4>
        <p style="margin: 5px 0 0 0; font-size: 12px;">Total de registros: {len(data_with_coords):,}</p>
    </div>
    '''
    crime_map.get_root().html.add_child(folium.Element(title_html))

    crime_map.save(str(output_path))
    print(f"    Mapa salvo: {output_path}")


def create_temporal_heatmap(data, output_path, year):
    data_with_coords = data[data['HAS_VALID_COORDS']].copy()

    if len(data_with_coords) == 0:
        print("    AVISO: Nenhum dado com coordenadas válidas")
        return

    center_lat = data_with_coords['LATITUDE'].mean()
    center_lon = data_with_coords['LONGITUDE'].mean()

    months = sorted(data_with_coords['MES_ESTATISTICA'].unique())

    if len(months) == 0:
        print("    AVISO: Nenhum dado de mês disponível")
        return

    month_names = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    heat_data = []
    valid_months = []
    MIN_POINTS_PER_MONTH = 5

    for month in months:
        month_data = data_with_coords[data_with_coords['MES_ESTATISTICA'] == month]

        if len(month_data) < MIN_POINTS_PER_MONTH:
            print(f"    DEBUG: Mês {month_names[month-1]} tem apenas {len(month_data)} pontos (mínimo: {MIN_POINTS_PER_MONTH}), ignorando")
            continue

        sampled_data = sample_data_for_performance(month_data, max_points=3000)
        month_points = [[row['LATITUDE'], row['LONGITUDE']] for _, row in sampled_data.iterrows()]

        if len(month_points) >= MIN_POINTS_PER_MONTH:
            heat_data.append(month_points)
            valid_months.append(month)
            print(f"    DEBUG: Mês {month_names[month-1]} incluído com {len(month_points)} pontos")

    if len(heat_data) < 2:
        print(f"    AVISO: Mapa temporal requer pelo menos 2 meses com dados suficientes")
        print(f"    Encontrados apenas {len(heat_data)} mês(es) válido(s)")
        print(f"    Meses disponíveis: {', '.join([month_names[m-1] for m in valid_months])}")
        return

    crime_map = folium.Map(
        location=[center_lat, center_lon],
        tiles='OpenStreetMap'
    )

    fit_map_to_bounds(crime_map, data_with_coords)

    index_labels = [month_names[m-1] for m in valid_months]

    print(f"    Gerando mapa temporal com {len(heat_data)} meses: {', '.join(index_labels)}")

    plugins.HeatMapWithTime(
        heat_data,
        index=index_labels,
        auto_play=True,
        max_opacity=0.8,
        radius=15,
        blur=20,
        gradient={0.4: 'blue', 0.6: 'lime', 0.7: 'yellow', 0.8: 'orange', 1: 'red'}
    ).add_to(crime_map)

    title_html = f'''
    <div style="position: fixed;
                top: 10px; left: 50px; width: 400px; height: 60px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:16px; padding: 10px; border-radius: 5px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
        <h4 style="margin: 0;">Evolução temporal de crimes - {year}</h4>
        <p style="margin: 5px 0 0 0; font-size: 12px;">Use o controle abaixo para navegar</p>
    </div>
    '''
    crime_map.get_root().html.add_child(folium.Element(title_html))

    crime_map.save(str(output_path))
    print(f"    Mapa salvo: {output_path}")


def create_time_period_maps(data, output_dir, year):
    data_with_coords = data[data['HAS_VALID_COORDS']].copy()

    if len(data_with_coords) == 0:
        print("    AVISO: Nenhum dado com coordenadas válidas")
        return

    periods = {
        'manha': 'Manhã (6h-12h)',
        'tarde': 'Tarde (12h-18h)',
        'noite': 'Noite/Madrugada (18h-6h)'
    }

    center_lat = data_with_coords['LATITUDE'].mean()
    center_lon = data_with_coords['LONGITUDE'].mean()

    for period_key, period_label in periods.items():
        period_data = filter_by_time_period(data_with_coords, period_key.replace('manha', 'manhã'))

        if len(period_data) == 0:
            print(f"    AVISO: Nenhum dado para o período {period_label}")
            continue

        crime_map = folium.Map(
            location=[center_lat, center_lon],
            tiles='OpenStreetMap'
        )

        fit_map_to_bounds(crime_map, period_data)

        sampled_data = sample_data_for_performance(period_data, max_points=3000)
        heat_data = [[row['LATITUDE'], row['LONGITUDE']] for _, row in sampled_data.iterrows()]

        plugins.HeatMap(
            heat_data,
            min_opacity=0.3,
            max_opacity=0.8,
            radius=15,
            blur=20,
            gradient={0.4: 'blue', 0.6: 'lime', 0.7: 'yellow', 0.8: 'orange', 1: 'red'}
        ).add_to(crime_map)

        title_html = f'''
        <div style="position: fixed;
                    top: 10px; left: 50px; width: 400px; height: 80px;
                    background-color: white; border:2px solid grey; z-index:9999;
                    font-size:16px; padding: 10px; border-radius: 5px;
                    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
            <h4 style="margin: 0;">Crimes por período: {period_label}</h4>
            <p style="margin: 5px 0 0 0; font-size: 12px;">São Paulo {year}</p>
            <p style="margin: 5px 0 0 0; font-size: 12px;">Total: {len(period_data):,} registros</p>
        </div>
        '''
        crime_map.get_root().html.add_child(folium.Element(title_html))

        output_path = output_dir / f'mapa_periodo_{period_key}_{year}.html'
        crime_map.save(str(output_path))
        print(f"    Mapa salvo: {output_path}")


def create_neighborhood_density_map(data, output_path, year):
    data_with_coords = data[data['HAS_VALID_COORDS']].copy()

    if len(data_with_coords) == 0:
        print("    AVISO: Nenhum dado com coordenadas válidas")
        return

    center_lat = data_with_coords['LATITUDE'].mean()
    center_lon = data_with_coords['LONGITUDE'].mean()

    crime_map = folium.Map(
        location=[center_lat, center_lon],
        tiles='OpenStreetMap'
    )

    neighborhood_stats = data_with_coords.groupby('BAIRRO').agg({
        'LATITUDE': 'mean',
        'LONGITUDE': 'mean',
        'NUM_BO': 'count',
        'NATUREZA_APURADA': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
    }).rename(columns={'NUM_BO': 'total_crimes', 'NATUREZA_APURADA': 'most_common_crime'})

    neighborhood_stats = neighborhood_stats.sort_values('total_crimes', ascending=False).head(50)

    max_crimes = neighborhood_stats['total_crimes'].max()
    min_crimes = neighborhood_stats['total_crimes'].min()

    for bairro, row in neighborhood_stats.iterrows():
        normalized_size = 10 + (row['total_crimes'] - min_crimes) / (max_crimes - min_crimes) * 30

        color_intensity = (row['total_crimes'] - min_crimes) / (max_crimes - min_crimes)
        if color_intensity < 0.33:
            color = '#ffeda0'
        elif color_intensity < 0.66:
            color = '#feb24c'
        else:
            color = '#f03b20'

        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px; width: 250px;">
            <h4 style="margin: 0 0 10px 0; color: #333;">{bairro.title()}</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 3px; border-bottom: 1px solid #ddd;"><b>Total de crimes:</b></td>
                    <td style="padding: 3px; border-bottom: 1px solid #ddd;">{int(row['total_crimes'])}</td></tr>
                <tr><td style="padding: 3px;"><b>Crime mais comum:</b></td>
                    <td style="padding: 3px;">{row['most_common_crime']}</td></tr>
            </table>
        </div>
        """

        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=normalized_size,
            popup=folium.Popup(popup_html, max_width=300),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.6,
            opacity=0.8
        ).add_to(crime_map)

    fit_map_to_bounds(crime_map, data_with_coords)

    legend_html = '''
    <div style="position: fixed;
                bottom: 50px; left: 50px; width: 200px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:14px; padding: 10px; border-radius: 5px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
        <b>Densidade de crimes</b><br>
        <i style="background:#f03b20; width:15px; height:15px; border-radius:50%; display:inline-block; margin-right:5px;"></i> Alta<br>
        <i style="background:#feb24c; width:15px; height:15px; border-radius:50%; display:inline-block; margin-right:5px;"></i> Média<br>
        <i style="background:#ffeda0; width:15px; height:15px; border-radius:50%; display:inline-block; margin-right:5px;"></i> Baixa<br>
        <p style="margin: 10px 0 0 0; font-size: 11px;">Tamanho = nº de crimes</p>
    </div>
    '''
    crime_map.get_root().html.add_child(folium.Element(legend_html))

    title_html = f'''
    <div style="position: fixed;
                top: 10px; left: 50px; width: 450px; height: 60px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:16px; padding: 10px; border-radius: 5px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
        <h4 style="margin: 0;">Densidade de crimes por bairro - São Paulo {year}</h4>
        <p style="margin: 5px 0 0 0; font-size: 12px;">Top 50 bairros com mais crimes</p>
    </div>
    '''
    crime_map.get_root().html.add_child(folium.Element(title_html))

    crime_map.save(str(output_path))
    print(f"    Mapa salvo: {output_path}")


def create_high_risk_crimes_map(data, output_path, year):
    data_with_coords = data[data['HAS_VALID_COORDS']].copy()

    if len(data_with_coords) == 0:
        print("    AVISO: Nenhum dado com coordenadas válidas")
        return

    high_risk_categories = {
        'Homicídios': [
            'HOMICÍDIO DOLOSO',
            'LATROCÍNIO',
            'LESÃO CORPORAL SEGUIDA DE MORTE',
            'HOMICÍDIO CULPOSO POR ACIDENTE DE TRÂNSITO',
            'HOMICÍDIO CULPOSO OUTROS',
            'HOMICÍDIO DOLOSO POR ACIDENTE DE TRÂNSITO'
        ],
        'Crimes sexuais': [
            'ESTUPRO',
            'ESTUPRO DE VULNERÁVEL'
        ],
        'Tentativa de homicídio': [
            'TENTATIVA DE HOMICÍDIO'
        ],
        'Crimes organizados': [
            'EXTORSÃO MEDIANTE SEQUESTRO',
            'ROUBO A BANCO',
            'ROUBO DE CARGA'
        ]
    }

    all_high_risk = [crime for crimes in high_risk_categories.values() for crime in crimes]
    high_risk_data = data_with_coords[data_with_coords['NATUREZA_APURADA'].isin(all_high_risk)].copy()

    if len(high_risk_data) == 0:
        print("    AVISO: Nenhum crime de alto risco encontrado nos dados")
        return

    center_lat = high_risk_data['LATITUDE'].mean()
    center_lon = high_risk_data['LONGITUDE'].mean()

    crime_map = folium.Map(
        location=[center_lat, center_lon],
        tiles='CartoDB dark_matter'
    )

    fit_map_to_bounds(crime_map, high_risk_data)

    category_colors = {
        'Homicídios': '#8b0000',
        'Crimes sexuais': '#4b0082',
        'Tentativa de homicídio': '#ff4500',
        'Crimes organizados': '#8b008b'
    }

    category_icons = {
        'Homicídios': 'remove',
        'Crimes sexuais': 'warning-sign',
        'Tentativa de homicídio': 'flash',
        'Crimes organizados': 'briefcase'
    }

    for category_name, crime_types in high_risk_categories.items():
        category_data = high_risk_data[high_risk_data['NATUREZA_APURADA'].isin(crime_types)]

        if len(category_data) == 0:
            continue

        feature_group = folium.FeatureGroup(name=category_name, show=True)

        for idx, row in category_data.iterrows():
            hora_formatada = 'N/A'
            if pd.notna(row.get('HORA_OCORRENCIA_BO')):
                try:
                    hora_formatada = pd.to_datetime(row['HORA_OCORRENCIA_BO']).strftime('%H:%M:%S')
                except:
                    hora_formatada = str(row['HORA_OCORRENCIA_BO'])

            popup_html = f"""
            <div style="font-family: Arial; font-size: 13px; width: 280px;">
                <h4 style="margin: 0 0 10px 0; color: {category_colors[category_name]}; border-bottom: 2px solid {category_colors[category_name]};">
                    ⚠️ {row['NATUREZA_APURADA']}
                </h4>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="background-color: #f9f9f9;">
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;"><b>Categoria:</b></td>
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;">{category_name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;"><b>Data:</b></td>
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;">{row['DATA_OCORRENCIA_BO'].strftime('%d/%m/%Y')}</td>
                    </tr>
                    <tr style="background-color: #f9f9f9;">
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;"><b>Hora:</b></td>
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;">{hora_formatada}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;"><b>Bairro:</b></td>
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;">{row['BAIRRO'].title()}</td>
                    </tr>
                    <tr style="background-color: #f9f9f9;">
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;"><b>Logradouro:</b></td>
                        <td style="padding: 5px; border-bottom: 1px solid #ddd;">{row['LOGRADOURO'][:40]}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px;"><b>Delegacia:</b></td>
                        <td style="padding: 5px;">{row['NOME_DELEGACIA'][:30]}</td>
                    </tr>
                </table>
            </div>
            """

            folium.Marker(
                location=[row['LATITUDE'], row['LONGITUDE']],
                popup=folium.Popup(popup_html, max_width=320),
                icon=folium.Icon(
                    color='darkred' if category_name == 'Homicídios' else
                          'purple' if category_name == 'Crimes sexuais' else
                          'red' if category_name == 'Tentativa de homicídio' else 'black',
                    icon=category_icons[category_name],
                    prefix='glyphicon'
                )
            ).add_to(feature_group)

        feature_group.add_to(crime_map)

    folium.LayerControl(collapsed=False).add_to(crime_map)

    legend_html = f'''
    <div style="position: fixed;
                bottom: 50px; left: 50px; width: 250px;
                background-color: white; border:3px solid #8b0000; z-index:9999;
                font-size:14px; padding: 15px; border-radius: 5px;
                box-shadow: 3px 3px 10px rgba(0,0,0,0.5);">
        <h4 style="margin: 0 0 10px 0; color: #8b0000;">⚠️ Crimes de Alto Risco</h4>
        <div style="margin: 8px 0;">
            <i class="glyphicon glyphicon-remove" style="color: darkred; margin-right: 8px;"></i>
            <span style="font-weight: bold;">Homicídios</span>
            <span style="float: right;">{len(high_risk_data[high_risk_data['NATUREZA_APURADA'].isin(high_risk_categories['Homicídios'])])}</span>
        </div>
        <div style="margin: 8px 0;">
            <i class="glyphicon glyphicon-warning-sign" style="color: purple; margin-right: 8px;"></i>
            <span style="font-weight: bold;">Crimes sexuais</span>
            <span style="float: right;">{len(high_risk_data[high_risk_data['NATUREZA_APURADA'].isin(high_risk_categories['Crimes sexuais'])])}</span>
        </div>
        <div style="margin: 8px 0;">
            <i class="glyphicon glyphicon-flash" style="color: red; margin-right: 8px;"></i>
            <span style="font-weight: bold;">Tentativa homicídio</span>
            <span style="float: right;">{len(high_risk_data[high_risk_data['NATUREZA_APURADA'].isin(high_risk_categories['Tentativa de homicídio'])])}</span>
        </div>
        <div style="margin: 8px 0;">
            <i class="glyphicon glyphicon-briefcase" style="color: black; margin-right: 8px;"></i>
            <span style="font-weight: bold;">Crimes organizados</span>
            <span style="float: right;">{len(high_risk_data[high_risk_data['NATUREZA_APURADA'].isin(high_risk_categories['Crimes organizados'])])}</span>
        </div>
        <hr style="border-top: 1px solid #ccc; margin: 10px 0;">
        <div style="font-weight: bold; text-align: center;">
            Total: {len(high_risk_data)} crimes
        </div>
    </div>
    '''
    crime_map.get_root().html.add_child(folium.Element(legend_html))

    title_html = f'''
    <div style="position: fixed;
                top: 10px; left: 50px; width: 500px; height: 80px;
                background-color: #ffffff; border:3px solid #8b0000; z-index:9999;
                font-size:16px; padding: 10px; border-radius: 5px;
                box-shadow: 3px 3px 10px rgba(0,0,0,0.5);">
        <h4 style="margin: 0; color: #8b0000;">⚠️ Mapa de Crimes de Alto Risco - São Paulo {year}</h4>
        <p style="margin: 5px 0 0 0; font-size: 12px;">Homicídios, crimes sexuais, tentativas de homicídio e crimes organizados</p>
        <p style="margin: 3px 0 0 0; font-size: 11px; color: #666;">Use os controles de camada para filtrar por categoria</p>
    </div>
    '''
    crime_map.get_root().html.add_child(folium.Element(title_html))

    crime_map.save(str(output_path))
    print(f"    Mapa salvo: {output_path}")
    print(f"    Total de crimes de alto risco mapeados: {len(high_risk_data)}")


def main():
    parser = argparse.ArgumentParser(
        description='Gerar mapas interativos de crimes de São Paulo usando folium'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='SPDadosCriminais_2024.xlsx',
        help='Caminho para o arquivo Excel de entrada'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='maps',
        help='Diretório para salvar os mapas gerados'
    )
    parser.add_argument(
        '--year',
        type=int,
        default=2024,
        help='Ano para filtrar os dados'
    )
    parser.add_argument(
        '--neighborhoods',
        nargs='+',
        type=str,
        default=None,
        help='Lista de bairros para análise específica'
    )
    parser.add_argument(
        '--map-type',
        type=str,
        choices=['layers', 'temporal', 'periods', 'density', 'high-risk', 'all'],
        default='all',
        help='Tipo de mapa a gerar (ou "all" para todos)'
    )
    parser.add_argument(
        '--max-points',
        type=int,
        default=5000,
        help='Número máximo de pontos por mapa (para performance)'
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    print(f"Carregando dados de {args.input}...")
    citywide_data, neighborhood_data = load_and_preprocess_data(
        args.input,
        ano=args.year,
        neighborhoods=args.neighborhoods
    )

    data_to_map = neighborhood_data if neighborhood_data is not None and len(neighborhood_data) > 0 else citywide_data

    area_label = f"{len(args.neighborhoods)} bairro(s)" if args.neighborhoods else "São Paulo"
    print(f"\nGerando mapas para {area_label} - {args.year}")
    print(f"Total de registros: {len(data_to_map):,}")
    print(f"Registros com coordenadas válidas: {data_to_map['HAS_VALID_COORDS'].sum():,}\n")

    map_types = {
        'layers': ('Mapa de camadas por categoria',
                   lambda: create_layered_crime_map(data_to_map, output_dir / f'mapa_camadas_{args.year}.html', args.year)),
        'temporal': ('Mapa de calor temporal',
                     lambda: create_temporal_heatmap(data_to_map, output_dir / f'mapa_temporal_{args.year}.html', args.year)),
        'periods': ('Mapas por período do dia',
                    lambda: create_time_period_maps(data_to_map, output_dir, args.year)),
        'density': ('Mapa de densidade por bairro',
                    lambda: create_neighborhood_density_map(data_to_map, output_dir / f'mapa_densidade_{args.year}.html', args.year)),
        'high-risk': ('Mapa de crimes de alto risco',
                      lambda: create_high_risk_crimes_map(data_to_map, output_dir / f'mapa_alto_risco_{args.year}.html', args.year)),
    }

    if args.map_type == 'all':
        maps_to_generate = map_types.items()
    else:
        maps_to_generate = [(args.map_type, map_types[args.map_type])]

    for map_key, (map_name, map_func) in maps_to_generate:
        print(f"Gerando: {map_name}...")
        map_func()

    print(f"\n{'=' * 60}")
    print(f"Mapas gerados com sucesso!")
    print(f"Localização: {output_dir.absolute()}")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
