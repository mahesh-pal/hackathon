from csv_loader import CSVLoader
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
INDEX_NAME = os.getenv('INDEX_NAME')

#get file path
FILE_PATH = f"{os.getcwd()}"
path = os.path.join(FILE_PATH, 'detaset.csv')

#=============read csv fil============
loader = CSVLoader(file_path=path)
docs = loader.load()
#============================================create 
    
PineconeVectorStore.from_documents(docs, embeddings, index_name=INDEX_NAME)
print('=====done============')
