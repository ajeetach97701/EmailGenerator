from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableMap
from langchain.agents import AgentType, initialize_agent
from database import db, llm
from emailFetch import check_for_mail


prompt = """
You are a virtual assistant who answers users query. When a user asks a question  you have to answer him based on the context given in three back ticks and make sure to provide all the details.
context: ```{context}```
question is given in double back ticks : ``{question}``.
If the questionis out of context, do not provide the wrong answer just say i am sorry i don't have an ansawer to that question.
"""


output_parser = StrOutputParser()
template = ChatPromptTemplate.from_template(prompt)



chain = RunnableMap(
    {
        "context": lambda x:db.similarity_search(x['question'], k =1),
        "question": lambda x:x['question']
    }
)|template|llm|output_parser


# Function calling
response = check_for_mail()
print(response)

for email in response['emails']:
    print(email['content'])
    result = chain.invoke({"question":email['content']})



