import logging

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import psycopg2

from tools.custom_tools import read_tables_list_tool, read_table_info_tool


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@CrewBase
class SQLCrew():
    """
    SQL crew for database interactions and data analysis

    I am using students table (user is crewai with password)
    """

    @agent
    def rewriter(self) -> Agent:
        return Agent(
            config=self.agents_config['rewriter'],
            verbose=True,
        )

    @agent
    def sql_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['sql_writer'],
            verbose=True,
            max_iter=5,
            tools=[read_tables_list_tool, read_table_info_tool]
        )
    
    # @agent
    # def optimizer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['optimizer'],
    #         verbose=True
    #     )
    
    @agent
    def auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['auditor'],
            max_iter=2,
            verbose=True
        )
    
    # @agent
    # def executor(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['executor'],
    #         verbose=True
    #     )

    @task
    def rewrite_task(self) -> Task:
        return Task(
            config=self.tasks_config['rewrite'],
        )

    @task
    def generate_query_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_query'],
            context=[self.rewrite_task()],
            max_retries=2,
        )
    
    @task
    def audit_query_task(self) -> Task:
        return Task(
            config=self.tasks_config['audit_query'],
            context=[self.generate_query_task()],
        )
    
    # @task
    # def improve_query_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['rewrite_task']
    #     )

    # @task
    # def retrieve_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['retrieve_task']
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the SQL crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )