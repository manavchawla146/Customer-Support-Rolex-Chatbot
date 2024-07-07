from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
import shutil

# Paths and environment variables
CHROMA_PATH = "chroma"
DATA_PATH = "data"
os.environ["OPENAI_API_KEY"] = ""

# Main function
def main():
    generate_data_store()

# Generate & Save data chunks
def generate_data_store():
    # Load documents from directory
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()

    # Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # Printing of accessing and printing a document
    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    # Save chunks into storage
    save_chunks(chunks)

# Function to save chunks into storage
def save_chunks(chunks: list[Document]):
    # Remove existing database
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new database using Chroma DB
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

# Entry point to execute the main function
if __name__ == "__main__":
    main()
