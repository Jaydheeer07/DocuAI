import streamlit as st
import os
import qdrant_client
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings 
from Components.user_query import get_chat_message
from Components.role_prompt import role_prompt
from Components.load_docu import load_pdf, load_text_file
from Components.chunk_docu import chunk_pdf, chunk_text

# Load the .env file
load_dotenv()

# Get the OPENAI API key and Client
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=openai_api_key)
embeddings= OpenAIEmbeddings()

# Qdrant Cloud connection details and create a client
qdrant_cloud_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_collection= os.getenv("QDRANT_COLLECTION")

vectors_config= qdrant_client.http.models.VectorParams(
    size= 1536, #size for OpenAI models
    distance= qdrant_client.http.models.Distance.COSINE
)

qdrant_client = qdrant_client.QdrantClient(
    url= qdrant_cloud_url,
    api_key= qdrant_api_key
)


# Streamlit App Interface

# Set your web app initial look
st.set_page_config(page_title="DocuAI 🤗", layout="wide")

st.title('Chat with DocuAI :computer:')
st.write(":speech_balloon: Communicate with Your Documents: Search Made Conversational. Powered by OpenAI and Qdrant. ")

# Upload document
filename = st.file_uploader("Choose a document :open_file_folder:", type=['pdf', 'txt'])
if filename is not None:

    file_details = {"FileName": filename.name, "FileType": filename.type, "FileSize": filename.size}
    st.write(file_details)
    if ".pdf" in filename.name: 
        pdf_loaded = load_pdf(filename)
        chunks = chunk_pdf(pdf_loaded, by="char")
    elif ".txt" in filename.name:
        text_loaded = load_text_file(filename)
        chunks= chunk_text(text_loaded)
    else:
        st.write("Invalid file format. Upload only .pdf and .txt files.")
    # Clear Qdrant collection before adding new data (if collection exists)
    try:
        with st.spinner("Clearing Qdrant collection..."):
            qdrant_client.delete_collection(qdrant_collection)
    except qdrant_client.exceptions.CollectionNotFoundError:
        st.warning("Qdrant collection does not exist. Creating a new one...")

    # Re-create Qdrant collection (if needed)
    with st.spinner("Creating Qdrant collection..."):
        qdrant_client.create_collection(
        collection_name=qdrant_collection,
        vectors_config=vectors_config,
        )

    # Initialize vector store
    vector_store = Qdrant(
        client=qdrant_client,
        collection_name=qdrant_collection,
        embeddings=embeddings
    )

    # Add chunks to vector store
    with st.spinner("Uploading to Qdrant....."):
        vector_store.add_texts(chunks)
    st.success('Document uploaded and vectors stored in Qdrant database.')

# Init prompt and convo
prompt = [{"role": "system", "content": role_prompt}]
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
    {"role": "assistant", "content": "Ask me a question about your uploaded document!"}
    ]


# Accept query from the user
if user_query := st.chat_input("Ask your document a question..."): # Prompt for user input
    st.session_state.messages.append({"role": "user", "content": user_query})


for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_chat_message(user_query, vector_store, openai_client, prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history
# Quit button to end the current session or conversation
if st.button('End the conversation. '):
    st.stop()
    








