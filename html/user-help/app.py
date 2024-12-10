import os
import requests
from langchain.document_loaders import WebBaseLoader
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

from sublinks import sublinks

load_dotenv()

def extract_docs_from_urls(url):
    docs = []
    session = requests.Session()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    # Update headers with your browser's User-Agent and any other necessary headers
    session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            })
    # Access the main page to get any necessary cookies
    print('loading from web url')
    print(url)
    loader = WebBaseLoader (url)
    web_doc_list = loader.load()
    for doc in web_doc_list:
        split_texts = text_splitter.split_text(doc.page_content)
        docs.extend([Document(page_content=text, metadata=doc.metadata) for text in split_texts])

    return docs

if __name__ == '__main__':

    try:
        embeddings = OpenAIEmbeddings()
        # Initialize Pinecone Vector Store
        PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
        # Make sure to set API_KEY environment variable or replace it with your actual Pinecone API key.
        PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
        # Ensure the Pinecone API Key is set
        if not PINECONE_API_KEY:
            raise EnvironmentError("Missing Pinecone API Key. Set the PINECONE_API_KEY environment variable.")
        for sublink in sublinks:
            docs = extract_docs_from_urls(sublink)
            print(docs)
            print(f"Number of documents: {len(docs)}")
            # Connect to Pinecone index and insert the chunked docs as contents
            docsearch = PineconeVectorStore.from_documents(
                documents=docs,
                embedding=embeddings,
                index_name=PINECONE_INDEX_NAME,
                namespace='aa4k'
            )
            print(f"Documents loaded into Pinecone successfully")

    except Exception as e:
        print(f"An error occurred: {e}")  # Print the error message
