#Function to split the pdf file into chunks 

import PyPDF2
from langchain_text_splitters import CharacterTextSplitter

def chunk_pdf(text, chunk_size=1500, chunk_overlap=100, by="word"):
    if by not in ["word", "char"]:
        raise ValueError("Invalid value for 'by'. Use 'word' or 'char'. ")
    
    chunks = []

    if by == "word":
        text= text.split()
    elif by == "char":
        text= text

    
    current_chunk_start= 0
    while current_chunk_start < len(text):
        current_chunk_end = current_chunk_start + chunk_size

        if by == "word":
            chunk = " ".join(text[current_chunk_start:current_chunk_end])
        elif by == "char":
            chunk = text[current_chunk_start:current_chunk_end]

        
        chunks.append(chunk)
        current_chunk_start += (chunk_size - chunk_overlap)
        
    return chunks


def chunk_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size= 1000,
        chunk_overlap= 200,
        length_function= len
    )

    chunks= text_splitter.split_text(text)
    return chunks