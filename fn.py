import os
import pinecone
from google.cloud import bigquery
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_pinecone import PineconeVectorStore

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
INDEX_NAME = os.getenv('INDEX_NAME')
columns = ['bug_id','bug_source','status','priority','report_date','resolution_date','resolution_time_hrs','solution_steps','assigned_to','tags']



def update_pinecone():
    # Step 1: Get the last processed ID from environment variables
    last_processed_id = os.getenv('LAST_PROCESSED_ID', "0")  # Default to "0" if not set
    
    # Step 2: Query BigQuery for data with an ID greater than the last processed ID
    client = bigquery.Client()
    query = f"""
    SELECT * FROM `rag-learn-435708.rag_1.bugs`
    WHERE id > 0
    ORDER BY id ASC
    """
    
    query_job = client.query(query)
    results = query_job.result()
    
    new_last_processed_id = last_processed_id  # Initialize with the current last processed ID
    
    # Step 3: Process each row and update Pinecone
    docs = generate_vector(results)
    PineconeVectorStore.from_documents(docs, embeddings, index_name=INDEX_NAME)
    
    return f"Processed ", 200

# Helper function to generate a vector from the data (this could use embeddings, etc.)
def generate_vector(data):
    documents = []
    for idx, row in data.iterrows():
        content = row['description']
        metadata = {};
        for column in columns:
            metadata[column] = row[column]

            # Create a LangChain Document object
            doc = Document(
                page_content=content, 
                metadata=metadata  
            )
            print(doc)
            documents.append(doc)

        return documents


if __name__ == '__main__':
    update_pinecone();