import os;
from dotenv import load_dotenv;
from langchain_core.prompts import PromptTemplate;
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain import hub
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

load_dotenv()


if __name__ == '__main__':
    question = 'Form submission causes a server error'
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    llm = ChatOpenAI()
    vectorStore = PineconeVectorStore(index_name = os.environ['INDEX_NAME'], embedding=embeddings)
    result = vectorStore.similarity_search(question)
    prompt = PromptTemplate.from_template("""
                                          
          Answer the question from the provided context only.

                                          context: {context}                                
            question: {question}                              
                                          
                                          
                                          """)
    
    chain = prompt | llm
    result = chain.invoke(input = {"question": question, "context":result[0].metadata['solution_steps'] })
    print(result.content)