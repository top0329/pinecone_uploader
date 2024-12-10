import os
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from dotenv import load_dotenv

from pdf_urls import pdf_urls

load_dotenv()

def extract_text_with_pages(pdf_filepath):
    pages = []
    for page_layout in extract_pages(pdf_filepath):
        page_text = ""
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                page_text += element.get_text()
        pages.append(page_text)
    return pages

if __name__ == '__main__':

    try:
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        embeddings = OpenAIEmbeddings()
        # Initialize Pinecone Vector Store
        PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
        # Make sure to set API_KEY environment variable or replace it with your actual Pinecone API key.
        PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
        # Ensure the Pinecone API Key is set
        if not PINECONE_API_KEY:
            raise EnvironmentError("Missing Pinecone API Key. Set the PINECONE_API_KEY environment variable.")

        b_download = True
        if b_download == False:
            docs_dir = Path('./docs')

            # Glob pattern to match all pdf files
            pdf_files = docs_dir.glob('*.pdf')
            # Iterate over the matching files and print their absolute paths
            for pdf_file in pdf_files:
                path_file_absolute = pdf_file.resolve()
                print(path_file_absolute)
                rawdocs = extract_text(path_file_absolute)
                docs = text_splitter.split_text(rawdocs)
                docs = [Document(page_content=doc) for doc in docs]

                # Connect to Pinecone index and insert the chunked docs as contents
                docsearch = PineconeVectorStore.from_documents(
                    documents=docs,
                    embedding=embeddings,
                    index_name=PINECONE_INDEX_NAME,
                    namespace='aa4k'
                )
                print("Documents loaded into Pinecone successfully")
        else:
            for pdf_url in pdf_urls:
                print(pdf_url)
                # Parse the URL to get the path component
                parsed_url = urlparse(pdf_url)

                # Extract the basename which should be the file name
                file_name = os.path.basename(parsed_url.path)

                print(file_name)

                # Get the current datetime
                now = datetime.now()

                # Specify the directory where you want to save the PDF
                download_directory = Path(f"./docs")
                # Ensure that download directory exists
                download_directory.mkdir(parents=True, exist_ok=True)
                # Full path to the downloaded file
                pdf_filepath = download_directory / file_name

                # Download the PDF if it hasn't been downloaded yet
                if not pdf_filepath.is_file():
                    # Create a session object to handle cookies
                    print ('downloading')
                    session = requests.Session()

                    # Update headers with your browser's User-Agent and any other necessary headers
                    session.headers.update({
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                    })
                    # Access the main page to get any necessary cookies
                    response = session.get(pdf_url, verify=False)  # Replace with the appropriate starting page

                    # response = requests.get(pdf_url)
                    response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
                    with open(pdf_filepath, 'wb') as f:
                        print('wrting')
                        f.write(response.content)

                rawdocs = extract_text_with_pages(pdf_filepath)
                docs = []

                for page_num, page_content in enumerate(rawdocs, start=1):
                    page_chunks = text_splitter.split_text(page_content)
                    for chunk in page_chunks:
                        doc = Document(page_content=chunk, metadata={"source": pdf_url, "page": page_num})
                        docs.append(doc)

                for i, doc in enumerate(docs):
                    print(f"Chunk {i}: {doc}")  # Displaying first 50 characters of each chunk

                # Connect to Pinecone index and insert the chunked docs as contents
                docsearch = PineconeVectorStore.from_documents(
                    documents=docs,
                    embedding=embeddings,
                    index_name=PINECONE_INDEX_NAME,
                    namespace='aa4k'
                )
                print(f"Documents from {file_name} loaded into Pinecone successfully")

    except Exception as e:
        print(f"An error occurred: {e}")  # Print the error message
