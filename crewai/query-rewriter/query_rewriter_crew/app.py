import os
from datetime import datetime
from dotenv import load_dotenv
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from crew import SQLCrew
from utils import extract_answer_tag, extract_sql_tag
from tools.custom_tools import query_table_tool, _read_table_list, _read_table_info


load_dotenv()
app = FastAPI()
timestamp = datetime.today().now().timestamp()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str


def parse_result(result: str) -> str:
    if isinstance(result, list):
        return '\n '.join(', '.join(str(value) for value in tuple_item) for tuple_item in result)
    return str(result)
    

@app.post("/api/search")
async def search(query: Query):
    os.makedirs('output', exist_ok=True)

    inputs = {
        'query': query.query,
        'available_tables': parse_result(_read_table_list()),
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

    logger.info(f'Query results = {query_results}')

    query_results = parse_result(query_results)

    logger.info(f'Final parsed query output = {query_results}')

    return {
        "query": cleaned_query,
        "result": query_results
    }

@app.get("/api/tables")
async def get_tables():
    tables = _read_table_list()
    return {"tables": parse_result(tables)}

@app.get("/api/tables/{table_name}")
async def get_table_info(table_name: str):
    try:
        table_info = _read_table_info(table_name)
        return {"table_info": parse_result(table_info)}
    except Exception as e:
        logger.error(f"Error fetching table info for {table_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=300,  # 5 minutes
        timeout_graceful_shutdown=300,  # 5 minutes
    )