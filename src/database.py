import os 
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.agent_toolkits import GmailToolkit
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.llms import Ollama




## 1. Create a model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
gmail_toolkit = GmailToolkit()
# llm = Ollama(base_url = "http://localhost:11434",model = "llama2")
llm=ChatOpenAI(temperature=0.0,model="gpt-3.5-turbo")


### 2. Load the documents and split it
file_path = "info.xlsx"
loader = UnstructuredExcelLoader(file_path)
docs = loader.load()


# 3. Split the data
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
splits = text_splitter.split_documents(docs)

## 4. Create embeddings and retriever

# embedding = OpenAIEmbeddings(model = 'text-embedding-3-large')
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# To database
db = Chroma.from_documents(documents= splits, embedding = embeddings)
retreiver = db.as_retriever()

