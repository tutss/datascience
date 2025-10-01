import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use('ggplot')
sns.set_palette("husl")


def load_and_preprocess_data(file_path: str, ano: int = 2024, neighborhoods: list = None) -> tuple:
    data = pd.read_excel(file_path)
    total_records = len(data)

    sp_data = data[data['NOME_MUNICIPIO'] == 'S.PAULO']
    print(f"  Filtrado para São Paulo: {len(sp_data):,} registros ({len(sp_data)/total_records*100:.1f}% do total)")

    sp_data = sp_data[sp_data['ANO_BO'] == ano]
    sp_data = sp_data[sp_data['DATA_REGISTRO'].dt.year == ano]
    sp_data = sp_data[sp_data['DATA_OCORRENCIA_BO'].dt.year == ano]
    print(f"  Filtrado para ano {ano}: {len(sp_data):,} registros")

    sp_data['BAIRRO'] = sp_data['BAIRRO'].astype(str).str.lower()

    sp_data['HORA_OCORRENCIA_BO'] = pd.to_datetime(
        sp_data['HORA_OCORRENCIA_BO'],
        format='%H:%M:%S',
        errors='coerce'
    )
    sp_data['HOUR_OF_DAY'] = sp_data['HORA_OCORRENCIA_BO'].dt.hour

    sp_data['DAY_OF_WEEK'] = sp_data['DATA_OCORRENCIA_BO'].dt.dayofweek

    neighborhood_data = None
    if neighborhoods:
        neighborhoods_lower = [n.lower() for n in neighborhoods]
        neighborhood_data = sp_data[sp_data['BAIRRO'].isin(neighborhoods_lower)].copy()
        print(f"  Filtrado para bairros específicos: {len(neighborhood_data):,} registros")
        if len(neighborhood_data) == 0:
            print(f"    AVISO: Nenhum registro encontrado para os bairros: {', '.join(neighborhoods)}")

    valid_coords = sp_data[
        (sp_data['LATITUDE'].notna()) &
        (sp_data['LONGITUDE'].notna()) &
        (sp_data['LATITUDE'] >= -23.8) &
        (sp_data['LATITUDE'] <= -23.3) &
        (sp_data['LONGITUDE'] >= -46.9) &
        (sp_data['LONGITUDE'] <= -46.3) &
        (sp_data['LATITUDE'] != 0) &
        (sp_data['LONGITUDE'] != 0)
    ]
    sp_data['HAS_VALID_COORDS'] = sp_data.index.isin(valid_coords.index)
    print(f"  Coordenadas válidas: {len(valid_coords):,} registros ({len(valid_coords)/len(sp_data)*100:.1f}%)")

    if neighborhood_data is not None:
        valid_coords_neighborhood = neighborhood_data[
            (neighborhood_data['LATITUDE'].notna()) &
            (neighborhood_data['LONGITUDE'].notna()) &
            (neighborhood_data['LATITUDE'] >= -23.8) &
            (neighborhood_data['LATITUDE'] <= -23.3) &
            (neighborhood_data['LONGITUDE'] >= -46.9) &
            (neighborhood_data['LONGITUDE'] <= -46.3) &
            (neighborhood_data['LATITUDE'] != 0) &
            (neighborhood_data['LONGITUDE'] != 0)
        ]
        neighborhood_data['HAS_VALID_COORDS'] = neighborhood_data.index.isin(valid_coords_neighborhood.index)

    return sp_data, neighborhood_data


def plot_hourly_heatmap(data: pd.DataFrame, output_dir: Path, ano: int):
    missing_hours_pct = data['HOUR_OF_DAY'].isna().sum() / len(data) * 100
    hourly_data = data.dropna(subset=['HOUR_OF_DAY', 'DAY_OF_WEEK'])

    if len(hourly_data) == 0:
        print("Insufficient data for hourly heatmap")
        return

    pivot_table = hourly_data.groupby(['DAY_OF_WEEK', 'HOUR_OF_DAY']).size().unstack(fill_value=0)

    days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    pivot_table.index = [days[i] for i in pivot_table.index]

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot_table, cmap='YlOrRd', annot=False, fmt='d', cbar_kws={'label': 'Número de crimes'}, ax=ax)
    title = f'Crimes por hora do dia e dia da semana - {ano}'
    if missing_hours_pct > 0:
        title += f'\n({missing_hours_pct:.1f}% de registros sem hora da ocorrência não foram incluídos)'
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_xlabel('Hora do dia', fontsize=12)
    ax.set_ylabel('Dia da semana', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_dir / 'hourly_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_monthly_trends(data: pd.DataFrame, output_dir: Path, ano: int):
    monthly_data = data.groupby(['MES_ESTATISTICA', 'NATUREZA_APURADA']).size().reset_index(name='count')

    top_crimes = data['NATUREZA_APURADA'].value_counts().head(5).index
    filtered_data = monthly_data[monthly_data['NATUREZA_APURADA'].isin(top_crimes)]

    available_months = sorted(data['MES_ESTATISTICA'].unique())
    min_month = min(available_months)
    max_month = max(available_months)

    fig, ax = plt.subplots(figsize=(12, 6))
    for crime_type in top_crimes:
        crime_data = filtered_data[filtered_data['NATUREZA_APURADA'] == crime_type]
        ax.plot(crime_data['MES_ESTATISTICA'], crime_data['count'], marker='o', label=crime_type, linewidth=2)

    ax.set_title(f'Tendência mensal dos 5 crimes mais frequentes - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Número de ocorrências', fontsize=12)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)

    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    ax.set_xticks(available_months)
    ax.set_xticklabels([months[m-1] for m in available_months])
    ax.set_xlim(min_month - 0.5, max_month + 0.5)

    plt.tight_layout()
    plt.savefig(output_dir / 'monthly_trends.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_time_series(data: pd.DataFrame, output_dir: Path, ano: int):
    daily_counts = data.groupby('DATA_OCORRENCIA_BO').size().reset_index(name='count')
    daily_counts = daily_counts.sort_values('DATA_OCORRENCIA_BO')

    daily_counts['MA_7'] = daily_counts['count'].rolling(window=7, center=True).mean()
    daily_counts['MA_30'] = daily_counts['count'].rolling(window=30, center=True).mean()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(daily_counts['DATA_OCORRENCIA_BO'], daily_counts['count'], alpha=0.3, color='gray', label='Diário')
    ax.plot(daily_counts['DATA_OCORRENCIA_BO'], daily_counts['MA_7'], linewidth=2, label='Média móvel 7 dias')
    ax.plot(daily_counts['DATA_OCORRENCIA_BO'], daily_counts['MA_30'], linewidth=2, label='Média móvel 30 dias')

    ax.set_title(f'Série temporal de crimes em São Paulo - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Data', fontsize=12)
    ax.set_ylabel('Número de crimes', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'time_series.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_crime_type_distribution(data: pd.DataFrame, output_dir: Path, ano: int):
    crime_counts = data['NATUREZA_APURADA'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = sns.color_palette('Set2', len(crime_counts))
    crime_counts.plot(kind='barh', ax=ax, color=colors)
    ax.set_title(f'Distribuição dos 10 tipos de crime mais frequentes - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de ocorrências', fontsize=12)
    ax.set_ylabel('Tipo de crime', fontsize=12)
    ax.invert_yaxis()

    for i, v in enumerate(crime_counts.values):
        ax.text(v + 100, i, f'{v:,}', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'crime_type_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_high_risk_crimes(data: pd.DataFrame, output_dir: Path, ano: int):
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

    crime_data = []
    for category, crime_types in high_risk_categories.items():
        count = data[data['NATUREZA_APURADA'].isin(crime_types)].shape[0]
        crime_data.append({'category': category, 'count': count})

    crime_df = pd.DataFrame(crime_data).sort_values('count', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['darkred', 'purple', 'orange', 'maroon']
    bars = ax.barh(crime_df['category'], crime_df['count'], color=colors)

    ax.set_title(f'Crimes de alto risco em São Paulo - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de ocorrências', fontsize=12)
    ax.set_ylabel('Categoria', fontsize=12)

    for i, (bar, count) in enumerate(zip(bars, crime_df['count'])):
        ax.text(count + 10, i, f'{int(count):,}', va='center', fontsize=11)

    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(output_dir / 'high_risk_crimes.png', dpi=300, bbox_inches='tight')
    plt.close()

    detailed_counts = data[data['NATUREZA_APURADA'].isin([crime for crimes in high_risk_categories.values() for crime in crimes])]['NATUREZA_APURADA'].value_counts()

    fig, ax = plt.subplots(figsize=(12, 10))
    colors_detailed = sns.color_palette('Reds_r', len(detailed_counts))
    detailed_counts.plot(kind='barh', ax=ax, color=colors_detailed)
    ax.set_title(f'Crimes de alto risco detalhados - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de ocorrências', fontsize=12)
    ax.set_ylabel('Tipo de crime', fontsize=12)
    ax.invert_yaxis()

    for i, v in enumerate(detailed_counts.values):
        ax.text(v + 5, i, f'{v:,}', va='center', fontsize=9)

    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(output_dir / 'high_risk_crimes_detailed.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_neighborhood_crime_matrix(data: pd.DataFrame, output_dir: Path, ano: int):
    top_neighborhoods = data['BAIRRO'].value_counts().head(20).index
    top_crimes = data['NATUREZA_APURADA'].value_counts().head(5).index

    filtered_data = data[data['BAIRRO'].isin(top_neighborhoods) & data['NATUREZA_APURADA'].isin(top_crimes)]

    matrix_data = filtered_data.groupby(['BAIRRO', 'NATUREZA_APURADA']).size().unstack(fill_value=0)
    matrix_data = matrix_data.loc[top_neighborhoods[::-1]]

    fig, ax = plt.subplots(figsize=(14, 10))
    matrix_data.plot(kind='barh', stacked=True, ax=ax, width=0.8)

    for c in ax.containers:
        widths = [w.get_width() for w in c]
        total_width = sum(widths)
        labels = [f'{int(w.get_width())}' if w.get_width() / total_width > 0.04 else '' for w in c]
        ax.bar_label(c, labels=labels, label_type='center', fontsize=8, color='white', weight='bold')

    ax.set_title(f'Crimes por bairro (top 20 bairros) - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de crimes', fontsize=12)
    ax.set_ylabel('Bairro', fontsize=12)
    ax.legend(title='Tipo de crime', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.tight_layout()
    plt.savefig(output_dir / 'neighborhood_crime_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_top_crime_types(data: pd.DataFrame, output_dir: Path, ano: int):
    crime_counts = data['NATUREZA_APURADA'].value_counts().head(15)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = sns.color_palette('mako', len(crime_counts))
    crime_counts.plot(kind='barh', ax=ax, color=colors)
    ax.set_title(f'Top 15 tipos de crime mais frequentes - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de ocorrências', fontsize=12)
    ax.set_ylabel('Tipo de crime', fontsize=12)
    ax.invert_yaxis()

    for i, v in enumerate(crime_counts.values):
        ax.text(v + 100, i, f'{v:,}', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'top_crime_types.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_neighborhood_ranking(data: pd.DataFrame, output_dir: Path, ano: int):
    neighborhood_counts = data['BAIRRO'].value_counts().head(25)

    fig, ax = plt.subplots(figsize=(12, 10))
    colors = sns.color_palette('rocket', len(neighborhood_counts))
    neighborhood_counts.plot(kind='barh', ax=ax, color=colors)
    ax.set_title(f'Top 25 bairros com mais crimes registrados - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de crimes', fontsize=12)
    ax.set_ylabel('Bairro', fontsize=12)
    ax.invert_yaxis()

    for i, v in enumerate(neighborhood_counts.values):
        ax.text(v + 50, i, f'{v:,}', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'neighborhood_ranking.png', dpi=300, bbox_inches='tight')
    plt.close()


def generate_neighborhood_stats_table(data: pd.DataFrame, output_dir: Path):
    neighborhood_stats = data.groupby('BAIRRO').agg({
        'NUM_BO': 'count',
        'HAS_VALID_COORDS': 'sum',
        'NATUREZA_APURADA': lambda x: x.mode()[0] if len(x.mode()) > 0 else None
    }).rename(columns={
        'NUM_BO': 'total_crimes',
        'HAS_VALID_COORDS': 'records_with_coords',
        'NATUREZA_APURADA': 'most_common_crime'
    })

    neighborhood_stats['coord_coverage_pct'] = (
        neighborhood_stats['records_with_coords'] / neighborhood_stats['total_crimes'] * 100
    ).round(1)

    neighborhood_stats = neighborhood_stats.sort_values('total_crimes', ascending=False).head(30)

    neighborhood_stats.to_csv(output_dir / 'neighborhood_stats.csv')

    print("\nTop 10 bairros por número de crimes:")
    print(neighborhood_stats.head(10)[['total_crimes', 'most_common_crime', 'coord_coverage_pct']])


def plot_crime_density_by_district(data: pd.DataFrame, output_dir: Path, ano: int):
    district_counts = data['NOME_DELEGACIA'].value_counts().head(20)

    fig, ax = plt.subplots(figsize=(12, 10))
    colors = sns.color_palette('mako', len(district_counts))
    district_counts.plot(kind='barh', ax=ax, color=colors)
    ax.set_title(f'Top 20 delegacias por número de crimes registrados - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de crimes', fontsize=12)
    ax.set_ylabel('Delegacia', fontsize=12)
    ax.invert_yaxis()

    for i, v in enumerate(district_counts.values):
        ax.text(v + 100, i, f'{v:,}', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'district_crime_density.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_crime_density_by_district_physical(data: pd.DataFrame, output_dir: Path, ano: int):
    online_delegacias = ['DELEGACIA ELETRONICA', 'DELEGACIA ELETRONICA 1', 'DELEGACIA DA MULHER ONLINE']
    physical_data = data[~data['NOME_DELEGACIA'].isin(online_delegacias)]

    district_counts = physical_data['NOME_DELEGACIA'].value_counts().head(20)

    fig, ax = plt.subplots(figsize=(12, 10))
    colors = sns.color_palette('mako', len(district_counts))
    district_counts.plot(kind='barh', ax=ax, color=colors)
    ax.set_title(f'Top 20 delegacias por número de crimes registrados (sem atendimento online) - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de crimes', fontsize=12)
    ax.set_ylabel('Delegacia', fontsize=12)
    ax.invert_yaxis()

    for i, v in enumerate(district_counts.values):
        ax.text(v + 100, i, f'{v:,}', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'district_crime_density_physical.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_data_completeness(data: pd.DataFrame, output_dir: Path, ano: int):
    completeness = {
        'Coordenadas válidas': data['HAS_VALID_COORDS'].sum() / len(data) * 100,
        'Hora da ocorrência': data['HORA_OCORRENCIA_BO'].notna().sum() / len(data) * 100,
        'Período do dia': data['DESC_PERIODO'].notna().sum() / len(data) * 100,
        'Bairro': data['BAIRRO'].notna().sum() / len(data) * 100,
        'Tipo de local': data['DESCR_SUBTIPOLOCAL'].notna().sum() / len(data) * 100,
        'Conduta': data['DESCR_CONDUTA'].notna().sum() / len(data) * 100
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    fields = list(completeness.keys())
    percentages = list(completeness.values())
    colors = ['green' if p > 80 else 'orange' if p > 60 else 'red' for p in percentages]

    bars = ax.barh(fields, percentages, color=colors)
    ax.set_xlim(0, 100)
    ax.set_xlabel('Porcentagem de completude (%)', fontsize=12)
    ax.set_title(f'Qualidade dos dados: Completude por campo - {ano}', fontsize=16, pad=20)
    ax.axvline(x=80, color='gray', linestyle='--', alpha=0.5, linewidth=1)

    for i, (bar, pct) in enumerate(zip(bars, percentages)):
        ax.text(pct + 1, i, f'{pct:.1f}%', va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(output_dir / 'data_completeness.png', dpi=300, bbox_inches='tight')
    plt.close()


def generate_summary_stats(data: pd.DataFrame, output_dir: Path, ano: int):
    stats = {
        'total_records': len(data),
        'date_range': f"{data['DATA_OCORRENCIA_BO'].min().strftime('%Y-%m-%d')} a {data['DATA_OCORRENCIA_BO'].max().strftime('%Y-%m-%d')}",
        'unique_neighborhoods': data['BAIRRO'].nunique(),
        'unique_crime_types': data['NATUREZA_APURADA'].nunique(),
        'unique_districts': data['NOME_DELEGACIA'].nunique(),
        'records_with_valid_coords': data['HAS_VALID_COORDS'].sum(),
        'coord_coverage_pct': f"{data['HAS_VALID_COORDS'].sum() / len(data) * 100:.1f}%",
        'most_common_crime': data['NATUREZA_APURADA'].mode()[0],
        'most_affected_neighborhood': data['BAIRRO'].mode()[0],
    }

    summary_text = f"""
ESTATÍSTICAS RESUMIDAS - CRIMES EM SÃO PAULO {ano}
{'=' * 60}

Registros totais: {stats['total_records']:,}
Período: {stats['date_range']}

COBERTURA DE DADOS:
- Registros com coordenadas válidas: {stats['records_with_valid_coords']:,} ({stats['coord_coverage_pct']})

DIMENSÕES:
- Bairros únicos: {stats['unique_neighborhoods']:,}
- Tipos de crime únicos: {stats['unique_crime_types']:,}
- Delegacias únicas: {stats['unique_districts']:,}

PRINCIPAIS PADRÕES:
- Crime mais frequente: {stats['most_common_crime']}
- Bairro mais afetado: {stats['most_affected_neighborhood'].title()}

CRIMES POR TIPO (Top 10):
"""

    top_crimes = data['NATUREZA_APURADA'].value_counts().head(10)
    for crime, count in top_crimes.items():
        summary_text += f"  - {crime}: {count:,} ({count/len(data)*100:.1f}%)\n"

    summary_text += f"\n{'=' * 60}\n"
    summary_text += f"Relatório gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    with open(output_dir / 'summary_statistics.txt', 'w', encoding='utf-8') as f:
        f.write(summary_text)

    print(summary_text)


def plot_neighborhood_comparison(citywide_data: pd.DataFrame, neighborhood_data: pd.DataFrame, output_dir: Path, neighborhoods: list, ano: int):
    citywide_top = citywide_data['BAIRRO'].value_counts().head(10)

    neighborhood_total = len(neighborhood_data)
    neighborhood_name = "Bairros selecionados"

    comparison_data = pd.concat([
        citywide_top,
        pd.Series({neighborhood_name: neighborhood_total})
    ]).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ['red' if idx == neighborhood_name else 'steelblue' for idx in comparison_data.index]
    comparison_data.plot(kind='barh', ax=ax, color=colors)

    ax.set_title(f'Comparação: seus bairros vs top 10 bairros de São Paulo - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de crimes', fontsize=12)
    ax.set_ylabel('Bairro', fontsize=12)

    for i, v in enumerate(comparison_data.values):
        ax.text(v + 50, i, f'{v:,}', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'neighborhood_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_neighborhood_crime_breakdown(neighborhood_data: pd.DataFrame, output_dir: Path, ano: int):
    crime_counts = neighborhood_data['NATUREZA_APURADA'].value_counts().head(8)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = sns.color_palette('mako', len(crime_counts))
    crime_counts.plot(kind='barh', ax=ax, color=colors)
    ax.set_title(f'Distribuição de crimes nos seus bairros - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Número de ocorrências', fontsize=12)
    ax.set_ylabel('Tipo de crime', fontsize=12)

    for i, v in enumerate(crime_counts.values):
        ax.text(v + 0.1, i, f'{v:,}', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'neighborhood_crime_breakdown.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_neighborhood_time_series(neighborhood_data: pd.DataFrame, output_dir: Path, ano: int):
    daily_counts = neighborhood_data.groupby('DATA_OCORRENCIA_BO').size().reset_index(name='count')
    daily_counts = daily_counts.sort_values('DATA_OCORRENCIA_BO')

    daily_counts['MA_7'] = daily_counts['count'].rolling(window=7, center=True).mean()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(daily_counts['DATA_OCORRENCIA_BO'], daily_counts['count'], alpha=0.4, color='gray', label='Diário', marker='o', markersize=3)
    ax.plot(daily_counts['DATA_OCORRENCIA_BO'], daily_counts['MA_7'], linewidth=2.5, label='Média móvel 7 dias', color='darkred')

    ax.set_title(f'Tendência temporal de crimes nos seus bairros - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Data', fontsize=12)
    ax.set_ylabel('Número de crimes', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'neighborhood_time_series.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_neighborhood_hourly_pattern(neighborhood_data: pd.DataFrame, output_dir: Path, ano: int):
    missing_hours_pct = neighborhood_data['HOUR_OF_DAY'].isna().sum() / len(neighborhood_data) * 100
    hourly_data = neighborhood_data.dropna(subset=['HOUR_OF_DAY', 'DAY_OF_WEEK'])

    if len(hourly_data) < 10:
        print("    Dados insuficientes para mapa de calor por hora dos bairros")
        return

    pivot_table = hourly_data.groupby(['DAY_OF_WEEK', 'HOUR_OF_DAY']).size().unstack(fill_value=0)

    days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    pivot_table.index = [days[i] for i in pivot_table.index if i < len(days)]

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot_table, cmap='Reds', annot=False, cbar_kws={'label': 'Número de crimes'}, ax=ax)
    title = f'Crimes por hora do dia e dia da semana nos seus bairros - {ano}'
    if missing_hours_pct > 0:
        title += f'\n({missing_hours_pct:.1f}% registros sem hora da ocorrência não foram incluídos)'
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_xlabel('Hora do dia', fontsize=12)
    ax.set_ylabel('Dia da semana', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_dir / 'neighborhood_hourly_pattern.png', dpi=300, bbox_inches='tight')
    plt.close()


def generate_neighborhood_safety_table(neighborhood_data: pd.DataFrame, output_dir: Path):
    neighborhood_breakdown = neighborhood_data.groupby('BAIRRO').agg({
        'NUM_BO': 'count',
        'HAS_VALID_COORDS': 'sum',
        'NATUREZA_APURADA': lambda x: x.mode()[0] if len(x.mode()) > 0 else None
    }).rename(columns={
        'NUM_BO': 'total_crimes',
        'HAS_VALID_COORDS': 'records_with_coords',
        'NATUREZA_APURADA': 'most_common_crime'
    })

    neighborhood_breakdown = neighborhood_breakdown.sort_values('total_crimes', ascending=False)

    neighborhood_breakdown.to_csv(output_dir / 'neighborhood_safety_breakdown.csv')

    print("\nDetalhamento por bairro:")
    for bairro, row in neighborhood_breakdown.iterrows():
        print(f"  {bairro.title()}: {int(row['total_crimes'])} crimes - Crime mais comum: {row['most_common_crime']}")


def plot_neighborhood_monthly_change(neighborhood_data: pd.DataFrame, output_dir: Path, ano: int):
    monthly_counts = neighborhood_data.groupby('MES_ESTATISTICA').size().reset_index(name='count')
    monthly_counts = monthly_counts.sort_values('MES_ESTATISTICA')

    fig, ax = plt.subplots(figsize=(12, 6))
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    month_labels = [months[m-1] for m in monthly_counts['MES_ESTATISTICA']]

    bars = ax.bar(month_labels, monthly_counts['count'], color='darkred', alpha=0.7)
    ax.set_title(f'Evolução mensal de crimes nos seus bairros - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Número de crimes', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')

    for bar, count in zip(bars, monthly_counts['count']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}',
                ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(output_dir / 'neighborhood_monthly_change.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_neighborhood_vs_citywide_crimes(citywide_data: pd.DataFrame, neighborhood_data: pd.DataFrame, output_dir: Path, ano: int):
    citywide_top = citywide_data['NATUREZA_APURADA'].value_counts().head(6)
    neighborhood_top = neighborhood_data['NATUREZA_APURADA'].value_counts().head(6)

    citywide_pct = (citywide_top / len(citywide_data) * 100).to_dict()
    neighborhood_pct = (neighborhood_top / len(neighborhood_data) * 100).to_dict()

    all_crimes = set(citywide_pct.keys()) | set(neighborhood_pct.keys())

    comparison = pd.DataFrame({
        'São Paulo': [citywide_pct.get(crime, 0) for crime in all_crimes],
        'Seus bairros': [neighborhood_pct.get(crime, 0) for crime in all_crimes]
    }, index=list(all_crimes))

    comparison = comparison.sort_values('São Paulo', ascending=False).head(5)

    fig, ax = plt.subplots(figsize=(12, 8))
    comparison.plot(kind='barh', ax=ax, color=['steelblue', 'darkred'], width=0.7)
    ax.set_title(f'Comparação de tipos de crime: seus bairros vs São Paulo - {ano}', fontsize=16, pad=20)
    ax.set_xlabel('Porcentagem do total de crimes (%)', fontsize=12)
    ax.set_ylabel('Tipo de crime', fontsize=12)
    ax.legend(['São Paulo (geral)', 'Seus bairros'], fontsize=10)
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(output_dir / 'neighborhood_vs_citywide.png', dpi=300, bbox_inches='tight')
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Gerar análises e visualizações de dados criminais de São Paulo')
    parser.add_argument(
        '--input',
        type=str,
        default='SPDadosCriminais_2024.xlsx',
        help='Caminho para o arquivo Excel de entrada'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Diretório para salvar as visualizações geradas'
    )
    parser.add_argument(
        '--year',
        type=int,
        default=2024,
        help='Ano para filtrar os dados (padrão: 2024)'
    )
    parser.add_argument(
        '--neighborhoods',
        nargs='+',
        type=str,
        default=None,
        help='Lista de bairros para análise específica (ex: conceicao jabaquara "vila guarani")'
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    print(f"Carregando dados de {args.input}...")
    citywide_data, neighborhood_data = load_and_preprocess_data(args.input, ano=args.year, neighborhoods=args.neighborhoods)
    print(f"Dados carregados: {len(citywide_data):,} registros de São Paulo para {args.year}")

    print("\nGerando visualizações gerais de São Paulo...")

    print("  - Mapa de calor por hora...")
    plot_hourly_heatmap(citywide_data, output_dir, args.year)

    print("  - Tendências mensais...")
    plot_monthly_trends(citywide_data, output_dir, args.year)

    print("  - Série temporal...")
    plot_time_series(citywide_data, output_dir, args.year)

    # print("  - Distribuição de tipos de crime...")
    # plot_crime_type_distribution(citywide_data, output_dir, args.year)

    print("  - Análise de crimes de alto risco...")
    plot_high_risk_crimes(citywide_data, output_dir, args.year)

    print("  - Matriz crime × bairro...")
    plot_neighborhood_crime_matrix(citywide_data, output_dir, args.year)

    print("  - Top tipos de crime...")
    plot_top_crime_types(citywide_data, output_dir, args.year)

    # print("  - Ranking de bairros...")
    # plot_neighborhood_ranking(citywide_data, output_dir, args.year)

    print("  - Densidade por delegacia...")
    plot_crime_density_by_district(citywide_data, output_dir, args.year)

    print("  - Densidade por delegacia (sem atendimento online)...")
    plot_crime_density_by_district_physical(citywide_data, output_dir, args.year)

    print("  - Completude dos dados...")
    plot_data_completeness(citywide_data, output_dir, args.year)

    print("\nGerando estatísticas resumidas...")
    generate_neighborhood_stats_table(citywide_data, output_dir)
    generate_summary_stats(citywide_data, output_dir, args.year)

    if neighborhood_data is not None and len(neighborhood_data) > 0:
        print(f"\nGerando visualizações específicas para {len(args.neighborhoods)} bairro(s)...")

        print("  - Comparação com São Paulo...")
        plot_neighborhood_comparison(citywide_data, neighborhood_data, output_dir, args.neighborhoods, args.year)

        print("  - Distribuição de crimes nos bairros...")
        plot_neighborhood_crime_breakdown(neighborhood_data, output_dir, args.year)

        print("  - Tendência temporal dos bairros...")
        plot_neighborhood_time_series(neighborhood_data, output_dir, args.year)

        print("  - Padrão horário dos bairros...")
        plot_neighborhood_hourly_pattern(neighborhood_data, output_dir, args.year)

        print("  - Evolução mensal dos bairros...")
        plot_neighborhood_monthly_change(neighborhood_data, output_dir, args.year)

        print("  - Comparação de tipos de crime...")
        plot_neighborhood_vs_citywide_crimes(citywide_data, neighborhood_data, output_dir, args.year)

        print("\nGerando detalhamento por bairro...")
        generate_neighborhood_safety_table(neighborhood_data, output_dir)

    print(f"\n{'=' * 60}")
    print(f"Análises concluídas!")
    print(f"Visualizações salvas em: {output_dir.absolute()}")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
