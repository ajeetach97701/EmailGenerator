from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import os 
from langchain_community.agent_toolkits import GmailToolkit
from dotenv import load_dotenv

load_dotenv()
llm=ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'),model='gpt-3.5-turbo')
embeddings=OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
string_parser= StrOutputParser()
json_parser = JsonOutputParser()
gmail_toolkit = GmailToolkit()