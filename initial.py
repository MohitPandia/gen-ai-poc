from utils.util import get_db_connection, get_openai_model, get_rephrase_answer
from utils.prompts import get_final_prompt
from utils.chain import get_chain
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from utils.validations import validate_sql_query

def initialize_ai(question):

    db = get_db_connection()
    llm = get_openai_model()

    final_prompt = get_final_prompt()

    generate_query = create_sql_query_chain(llm, db, final_prompt)
    execute_query = QuerySQLDataBaseTool(db=db)
    
    chain = get_chain(generate_query, execute_query, llm)

    rephrase_answer = get_rephrase_answer(llm)
    
    
    from utils.few_shots import few_shot_prompt

    from langchain.memory import ChatMessageHistory
    history = ChatMessageHistory()

    response = chain.invoke({"question": question,"messages":history.messages})

    history.add_user_message(question)
    history.add_ai_message(response)


    return response