import PyPDF2
import chromadb
import os
from chromadb.utils import embedding_functions
import re
import string
import random

from src.constants import N_CHARACTRERS, RESSOURCES_DIR
from src.helpers import read_file

class Chroma():
    def __init__(self):
        self.client = self.connect()


    def connect(self):
        return chromadb.PersistentClient(path="./vector_database_data")
       
    def heartbeat(self):
        return self.client.heartbeat()
    
    def import_data(self, doc: str, meta_data: str, collection_name: str):
        # print(f"begin cleaning file {meta_data}")
        # cleaned_doc = self.clean_doc(doc)
        print(f"finished cleaning file {meta_data}")
        chunks = self.chunk_text_by_chars(doc, N_CHARACTRERS)
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
        # get or create collection if not exist
        collection = self.client.get_or_create_collection(name=collection_name, embedding_function=sentence_transformer_ef,
                                                            metadata={"hnsw:space": "cosine"})
        # Generate random IDs and store them in an array
        ids = [self.generate_random_id(8) for _ in range(len(chunks))]
        # create list metadata
        metadatas = [meta_data for _ in range(len(chunks))]

        # Batch size
        batch_size = 100

        print("Finished organizing chunks, start by inserting to db")

    # Process chunks in batches
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            batch_metadatas = metadatas[i:i + batch_size]

            # Add to collection
            collection.add(
                documents=batch_chunks,
                metadatas=batch_metadatas,
                ids=batch_ids,
            )
            print(f"Batch {i // batch_size + 1} of chunks added to {collection_name}")

        print(f"{meta_data} imported in {collection_name}")
        
        return "done"

    def generate_random_id(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def chunk_text_by_chars(self, text: str, chunk_size: int):
        return [
            text[i:i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]

    
    def clean_doc(text: str) -> str:
        # Remove sequences of dots separated by spaces (e.g., ". . . .")
        text = re.sub(r'(\.\s)+\.', '', text)
        # Remove sequences of three or more continuous dots (e.g., "...")
        cleaned = re.sub(r'\.{3,}', '', text)
        return cleaned
        
    
    
    def import_single_file_to_db(self, filename: str, collection_name: str):
        filepath = f"{RESSOURCES_DIR}/{filename}"
        if os.path.exists(filepath):
            file_extension = os.path.splitext(filename)[1]
            file_type = file_extension[1:]
            metadata = {"type": file_type, "file_name": filename}
            if file_type == "pdf":
                context = read_file(pdf_name=filename)
                self.import_data(doc=context, meta_data=metadata, collection_name=collection_name)
            return "done"
        else:
            return "file does not exist"
    
   
            
    def query_collection(self, prompt: str, n_results: int, collection_name: str):
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
        collection = self.client.get_collection(name=collection_name, embedding_function=sentence_transformer_ef)
        data_results = collection.query(
            query_texts=[prompt],
            n_results=n_results,
        )
        return data_results
       
    