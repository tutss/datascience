import argparse
import requests
from typing import List
from datetime import datetime

from tqdm import tqdm
import pandas as pd
import json

from model import APIResponse, DataItem, Delito, ListaDados
from constants import BASE_URL, DELEGACIAS, MONTH_MAP


def parse_args():
    parser = argparse.ArgumentParser(description="SSP‑SP data crawler")
    parser.add_argument(
        "--year",
        nargs="+",
        type=int,
        help="Years to fetch (e.g. --year 2010 2014). Defaults to all available years.",
    )
    parser.add_argument(
        "--delegacias",
        nargs="+",
        type=str,
        help='Delegacias to fetch, by name (e.g. --delegacias "DP - Brás" "DP - Campos Elíseos"). Defaults to all delegacias.',
    )
    return parser.parse_args()


def api_response_to_dataframe(api_response: APIResponse):
    rows = []
    for data_item in api_response.data:
        for lista in data_item.listaDados:
            for month_field, month_num in MONTH_MAP:
                rows.append({
                    'nome_distrito': api_response.delegacia if api_response.delegacia else "Desconhecido",
                    "ano": lista.ano,
                    "mes": month_num,
                    "num_ocorrencias": getattr(lista, month_field),
                    "publicado": lista.publicado,
                    "total": lista.total,
                    "delito_idDelito": lista.delito.idDelito,
                    "delito_idGrupoDelito": lista.delito.idGrupoDelito,
                    "delito_nome": lista.delito.delito,
                })
    return pd.DataFrame(rows)

def api_responses_to_dataframe(api_responses: List[APIResponse]) -> pd.DataFrame:
    frames = []
    for resp in api_responses:
        frames.append(api_response_to_dataframe(resp))
    return pd.concat(frames, ignore_index=True)

def main(anos, delegacias_map):
    complete_data: List[APIResponse] = list()
    json_data = list()

    for ano in tqdm(anos):
        print(f'ANO = {ano}')
        for id_delegacia, nome_delegacia in delegacias_map.items():
            print(f'DELEGACIA = {nome_delegacia}, ID Delegacia = {id_delegacia}')
            try:
                url = f'{BASE_URL}ano={ano}&grupoDelito=6&tipoGrupo=DISTRITO&idGrupo={id_delegacia}'
                response = requests.get(url)
                data = response.json()
                data['delegacia'] = nome_delegacia
                parsed_data = APIResponse(**data)
                complete_data.append(parsed_data)
                json_data.append(data)
            except Exception as e:
                print(e)
                continue

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    api_responses_df = api_responses_to_dataframe(complete_data)
    api_responses_df.to_csv(f'ssp-data-{timestamp}.csv', index=False)

    with open(f'ssp-data-{timestamp}.jsonl', 'w', encoding='utf-8') as f:
        for record in json_data:
            json.dump(record, f, ensure_ascii=False)
            f.write('\n')

if __name__ == "__main__":
    args = parse_args()

    # years to crawl
    if args.year:
        anos = args.year
    else:
        anos = list(range(2010, datetime.now().year + 1))

    # delegacias to crawl
    if args.delegacias:
        name_to_id = {v: k for k, v in DELEGACIAS.items()}
        delegacias_map = {
            name_to_id[name]: name
            for name in args.delegacias
            if name in name_to_id
        }
        if not delegacias_map:
            raise ValueError("None of the specified delegacias matched the known list.")
    else:
        delegacias_map = DELEGACIAS

    main(anos, delegacias_map)