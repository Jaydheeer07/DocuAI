#Function to load pdf file and txt file
import PyPDF2
import streamlit


def load_pdf(file_content):
  """Loads text content from a PDF file."""
  file = PyPDF2.PdfReader(stream=file_content)
  text_from_pdf = ""

  for page in range(len(file.pages)):
    text_from_pdf += file.pages[page].extract_text()
  
  return text_from_pdf


def load_text_file(file_content):
  """Loads text content from a text file."""
  try:
    # To read file as bytes:
    bytes_data = file_content.getvalue()
    # Decode bytes content as UTF-8 for text files
    text_content = bytes_data.decode("utf-8")
    return text_content
  except UnicodeDecodeError:
    # Handle potential encoding issues (optional)
    raise ValueError("Unsupported file encoding")
  except FileNotFoundError:
    raise FileNotFoundError("File content is empty")





