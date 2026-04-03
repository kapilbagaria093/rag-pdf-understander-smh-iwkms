# here we figure out some way to load the pdf and embed them
# we got how to search for vectors and insert vectors, but we still need to create vectors

from openai import OpenAI
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv

load_dotenv()

# we dont need to pass anything here, it will automatically get the key from dotenv file
client = OpenAI()

# embed: convert it to a vector so we can store it in database

# chunk: to chunk it means to break the pdfs down into smaller pieces and then embed those smaller pieces 

# here, size is relevant, we dont want to store large amounts of data, or data in so small pieces that its impossible to search, so we use llama index which split all the pdf into chunks and embed those chunks

EMBED_MODEL = "text-embedding-3-large"
EMBED_DIM = 3072 

# we want some chunk overlap so we dont lose relevant context from data (coz previously data was connected and related to each other before we chunked it)
# 200 means 200 characters here 
splitter = SentenceSplitter(chunk_size=1000 ,chunk_overlap=200)

def load_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)

    text = [d.text for d in docs if getattr(d, "text", None)]
    # get only text data from pdf, and not images and stuff 

    # chunking process
    chunks = []
    for t in text:
        chunks.extend(splitter.split_text(t))
    return chunks

def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model = EMBED_MODEL,
        input = texts
    )
    return [item.embedding for item in response.data]