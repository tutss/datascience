import os
from datetime import datetime
from dotenv import load_dotenv
import logging

from fastapi import FastAPI
from pydantic import BaseModel

from crew import SQLCrew
from utils import extract_answer_tag, extract_sql_tag
from tools.custom_tools import query_table_tool


load_dotenv()
app = FastAPI()
timestamp = datetime.today().now().timestamp()
logging.basicConfig(
    encoding='utf-8', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class Query(BaseModel):
    query: str

@app.post("/api/search")
async def search(query: Query):
    os.makedirs('output', exist_ok=True)
    # Replace this with your actual Python logic
    # result = f"You searched for: {query.query}"

    inputs = {
        'query': query.query,
        'available_tables': 'UNKNOWN',
        'tables_schemas': 'UNKNOWN'
    }

    logger.info(f'User inputs = {inputs}')

    logger.info('Kicking off the crew')
    result = SQLCrew().crew().kickoff(inputs=inputs)
    logger.info(f'Final Crew output = {result}')

    if extract_answer_tag(result.raw) != 'yes':
        return {'result': "Couldn't generate a query for you, sorry!"}
    
    cleaned_query = extract_sql_tag(result.raw)
    query_results = query_table_tool(cleaned_query)

    logger.info(f'Final query output = {query_results}')

    return {
        "query": cleaned_query,
        "result": query_results
    }