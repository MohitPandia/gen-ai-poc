
"""###Dynamic relevant table selection"""

from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
import pandas as pd
from utils.util import get_openai_model

llm = get_openai_model()

def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("database_table_descriptions.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Table'] + "\n" + "Table Description:" + row['Description'] + "\n\n"

    return table_details


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")

# table_names = "\n".join(db.get_usable_table_names())
table_details = get_table_details()
print(table_details)

table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

{table_details}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

table_chain = create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt)

def get_tables(tables: List[Table]) -> List[str]:
    tables  = [table.name for table in tables]
    return tables

select_table = {"input": itemgetter("question")} | create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt) | get_tables