import os
from datetime import datetime
from dotenv import load_dotenv
import logging

from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import psycopg2

from app import parse_result
from crew import SQLCrew
from utils import extract_answer_tag, extract_sql_tag
from tools.custom_tools import query_table_tool, _read_table_list, _read_table_info


load_dotenv()
timestamp = datetime.today().now().timestamp()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute_sql_file(file_path: str, connection_params: dict):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**connection_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Read and execute the SQL file
        with open(file_path, 'r') as file:
            sql_commands = file.read()
            cursor.execute(sql_commands)
            
        cursor.close()
        conn.close()
        logger.info(f"Successfully executed SQL file: {file_path}")
    except Exception as e:
        logger.error(f"Error executing SQL file: {str(e)}")
        raise e


def test_model(query: str):
    inputs = {
        'query': query,
        'available_tables': parse_result(_read_table_list()),
        'tables_schemas': 'UNKNOWN'
    }

    logger.info('Kicking off the crew')
    result = SQLCrew().crew().kickoff(inputs=inputs)
    logger.info(f'Final Crew output = {result}')

    cleaned_query = extract_sql_tag(result.raw)
    
    try:
        query_results = query_table_tool(cleaned_query)
    except Exception as err:
        logger.error('Couldnt execute query')
        query_results = 'Failed'

    try:
        parsed_query_results = parse_result(query_results)
    except Exception as err:
        logger.error('Couldnt parse query results')
        parsed_query_results = query_results
    
    logger.info(f'Final parsed query output = {parsed_query_results}')

    return {
        "query": cleaned_query,
        "result": parsed_query_results,
        "raw_results": query_results
    }


def run_test():
    db_params = {
        'host': 'localhost',
        'dbname': 'test',
        'user': 'arturmagalhaes'
    }

    test_type = 'exercise-3'
    creation_file_name = 'criacao_bd_CooperAgri.sql'
    sql_file_path = f'test/{test_type}/{creation_file_name}'
    execute_sql_file(sql_file_path, db_params)

    df = pd.read_csv(f'test/{test_type}/test_file.csv')

    results = {
        'llm_query': [],
        'llm_executed_query_results': [],
        'expected_query_results': [],
        'llm_query_raw_results': [],
        'expected_query_raw_results': []
    }
    for index, row in df.iterrows():
        question = row['question']
        expected_answer = row['expected_query'].replace('\n', ' ')

        logger.info(f'Query: {question}')
        logger.info(f'Gold query: {expected_answer}')
        
        result = test_model(question)
        logger.info(f'Result: {result}')

        try:
            gold_executed_query_raw = query_table_tool(expected_answer)
            gold_executed_query = parse_result(gold_executed_query_raw)
        except Exception as err:
            gold_executed_query = 'Failed'
    
        results['llm_query'].append(result['query'])
        results['llm_executed_query_results'].append(result['result'])
        results['llm_query_raw_results'].append(result['raw_results'])
        results['expected_query_results'].append(gold_executed_query)
        results['expected_query_raw_results'].append(gold_executed_query_raw)

    df_results = pd.DataFrame(results)
    df = pd.concat([df, df_results], axis=1)
    df.to_csv(f'test/{test_type}/test_file_results_1_agent_only.csv', index=False)


def test_model_w_spider(inputs: dict):
    logger.info('Kicking off the crew')
    result = SQLCrew().crew().kickoff(inputs=inputs)
    logger.info(f'Final Crew output = {result}')

    cleaned_query = extract_sql_tag(result.raw)
    
    try:
        query_results = query_table_tool(cleaned_query)
    except Exception as err:
        logger.error('Couldnt execute query')
        query_results = 'Failed'

    try:
        parsed_query_results = parse_result(query_results)
    except Exception as err:
        logger.error('Couldnt parse query results')
        parsed_query_results = query_results
    
    logger.info(f'Final parsed query output = {parsed_query_results}')

    return {
        "query": cleaned_query,
        "result": parsed_query_results,
        "raw_results": query_results
    }


def run_spider_test():
    """
    I modified optimizer agent to use db_schema
    I modified the tools usage on optimizer, removing them
    """
    db_params = {
        'host': 'localhost',
        'dbname': 'test',
        'user': 'arturmagalhaes'
    }

    sql_file_path = 'test/spider-style/criacao_bd_CooperAgri.sql'
    execute_sql_file(sql_file_path, db_params)
    sql_file_path = 'test/spider-style/script_criacao_bd_alunos.sql'
    execute_sql_file(sql_file_path, db_params)


    data_file_path = 'test/spider-style/mdb_proj2_resource.json'
    df = pd.read_json(data_file_path)

    results = {
        'llm_query': [],
        'llm_executed_query_results': [],
        'gold_sql_results': [],
        'llm_query_raw_results': []
    }
    for index, row in df.iterrows():
        instruction = row['instruction']
        db_schema = row['db_schema']
        gold_sql = row['gold_sql'].replace('\n', ' ')

        inputs = {
            'query': instruction,
            'db_schema': db_schema,
        }

        logger.info(f'Query inputs are = {inputs}')
        logger.info(f'Gold query = {gold_sql}')

        result = test_model_w_spider(inputs=inputs)
        results['llm_query'].append(result['query'])
        results['llm_executed_query_results'].append(result['result'])
        results['llm_query_raw_results'].append(result['raw_results'])

        try:
            gold_executed_query = query_table_tool(gold_sql)
        except Exception as err:
            gold_executed_query = 'Failed'

        results['gold_sql_results'].append(gold_executed_query)

    df_results = pd.DataFrame(results)
    df = pd.concat([df, df_results], axis=1)
    df.to_csv('test/spider-style/test_file_results_1_agent_only.csv', index=False)


if __name__ == "__main__":
    # run_test()
    run_spider_test()