import pandas as pd
from langchain_core.document_loaders import BaseLoader
from langchain.docstore.document import Document


columns = ['bug_id','bug_source','status','priority','report_date','resolution_date','resolution_time','solution_steps','assigned_to','tags']
class CSVLoader(BaseLoader):
    def __init__(self, file_path: str):
        """Initialize the loader with the path to the CSV file."""
        self.file_path = file_path

    def load(self):
        """Load data from the CSV file and return a list of LangChain documents."""
        # Read the CSV file into a DataFrame
        df = pd.read_csv(self.file_path)

        # provinding default value for NaN
        df['resolution_time'].fillna('', inplace=True)
        df['resolution_date'].fillna('', inplace=True)

        # Convert each row into a document
        documents = []
        for idx, row in df.iterrows():
            # we are only taking description since only this column will be converted to vector
            content = row['description']
            metadata = {};
            for column in columns:
                metadata[column] = row[column]

            # Create a LangChain Document object
            doc = Document(
                page_content=content, 
                metadata=metadata  
            )
            documents.append(doc)

        return documents