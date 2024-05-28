
examples = [
    {
        "input": "Find the total number of distinct invoices for each file and then get the maximum of these counts.",
        "query": """
SELECT MAX(invoice_count) AS invoice_count
FROM (
    SELECT COUNT(DISTINCT "invoice"."documentNo") AS invoice_count
    FROM "invoice"
    INNER JOIN "file" ON "invoice"."fileID" = "file"."id"
    GROUP BY "file"."id"
) subquery;
""",
    },
    {
        "input": "find the total invoices are there for enterprise Apollo",
        "query": """
SELECT COUNT(DISTINCT invoice.documentNo) AS total_invoices
FROM invoice
WHERE "enterpriseID" = (
    SELECT id
    FROM "enterprises-basic-details"
    WHERE LOWER(name) = LOWER('Apollo')
);
""",
    },
    {
        "input": "find the count of all loan-drawdowns related to business-partner S.M.G.C.V. ENTERPRISES",
        "query": """
SELECT COUNT(*) AS loan_drawdown_count
FROM "loan-drawdown"
WHERE "loanID" IN (
    SELECT id
    FROM "loan-terms"
    WHERE "borrowerID" = (
        SELECT id
        FROM "business-partners-basic-details"
        WHERE LOWER(name) = LOWER('S.M.G.C.V. ENTERPRISES')
    )
);
""",
    },
    
]

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)

"""###Dynamic few-shot example selection"""

from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma()
vectorstore.delete_collection()
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    vectorstore,
    k=1,
    input_keys=["input"],
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
    input_variables=["input","top_k"],
)