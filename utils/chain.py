

from operator import itemgetter
from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough
from utils.get_table_info import select_table

from utils.util import get_rephrase_answer
from utils.validations import validate_sql_query

def get_chain(generate_query, execute_query, llm):
    
    rephrase_answer = get_rephrase_answer(llm)

    def validate_and_execute(params):
        query = params["query"]
        print("Generated SQL query:", query)  # Log the generated SQL query
        validation_res = validate_sql_query(query)  # Validate the query
        if validation_res == True:
            return execute_query(query)  # Execute the query if validation passes
        else:
            return """
You have requested information that you do not have access to.
Please contact your administrator or check your permissions and try again.
"""

    def extract_query(params):
        print("In Betwwen query: ", params["query"])
        return {"query": params["query"]}

    chain = (
        RunnablePassthrough.assign(table_names_to_use=select_table) |
        RunnablePassthrough.assign(query=generate_query).assign(
            result=extract_query
        ) |
        RunnablePassthrough.assign(result=validate_and_execute) |
        rephrase_answer
    )

    return chain

