from typing import List
import logging

from crewai.tools import tool
import psycopg2


CONNECTION = psycopg2.connect("host='localhost' dbname='test' user='arturmagalhaes'")


logger = logging.getLogger("app")

logger.warning(f'Connecting to database...: {CONNECTION}')

@tool('ReadTablesList')
def read_tables_list_tool() -> List[str]:
    """
    This tool reads the list of tables from the database.
    It returns the list of table names as a string.
    """
    return _read_table_list()

def _read_table_list():
    logger.warning('Reading table list...')
    with CONNECTION.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
        """)
        fetched_results = cur.fetchall()
        logger.warning(f'Table list read. Results = {fetched_results}')
        return fetched_results

@tool('ReadTableInfo')
def read_table_info_tool(table_name: str) -> str:
    """
    This tool reads the information of a table.
    It returns the table information.
    """
    return _read_table_info(table_name)
    
def _read_table_info(table_name: str):
    logger.warning('Reading table info...')
    with CONNECTION.cursor() as cur:
        cur.execute(f"\
            SELECT column_name, data_type, character_maximum_length\
            FROM information_schema.columns\
            WHERE table_name = '{table_name}'\
        ")
        fetched_results = cur.fetchall()
        logger.warning(f'Table info read. Results = {fetched_results}')
        return fetched_results


def query_table_tool(query: str):
    """
    This tool queries a specific table in the database.
    It takes the table name and the query as input.
    It returns the result of the query as a string.
    """
    with CONNECTION.cursor() as cur:
        cur.execute("ROLLBACK")
    
    with CONNECTION.cursor() as cur:
        cur.execute(f"{query}")
        return cur.fetchall()