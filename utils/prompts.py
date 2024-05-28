
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from utils.few_shots import few_shot_prompt

"""Customizing prompts"""
def get_final_prompt():
    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a Postgre SQL expert. Given an input question, create a syntactically correct Postgre SQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Those examples are just for referecne and hsould be considered while answering follow up questions."),
            few_shot_prompt,
            MessagesPlaceholder(variable_name="messages"),
            ("human", "{input}"),
        ]
    )
    return final_prompt

