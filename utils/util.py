from langchain_community.utilities.sql_database import SQLDatabase
import os

from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_host = os.getenv('db_host')
db_name = os.getenv('db_name')

def get_db_connection():

    db = SQLDatabase.from_uri(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}", include_tables=["file", "loan-terms", "invoice", "loan-drawdown", "banks-basic-details", "enterprises-basic-details", "business-partners-basic-details", "enterprise-partner-mapping-details"])

    # print(db.dialect)
    # print(db.get_usable_table_names())
    # print(db.table_info)

    return db

GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_AI_MODEL = os.getenv("GOOGLE_AI_MODEL")
OPEN_AI_MODEL = os.getenv("OPEN_AI_MODEL")
TEMPERATURE = os.getenv("TEMPERATURE")

googleLLM = GoogleGenerativeAI(model = GOOGLE_AI_MODEL, google_api_key=GOOGLE_AI_API_KEY)
openAILLM = ChatOpenAI(model=OPEN_AI_MODEL, temperature= TEMPERATURE)


def get_google_llm():
    return googleLLM

def get_openai_model():
    return openAILLM


from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

def get_rephrase_answer(llm):

    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
    )
    rephrase_answer = answer_prompt | llm | StrOutputParser()

    return rephrase_answer