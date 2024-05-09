from openai import OpenAI
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings 


def get_chat_message(user_query, vector_store, openai_client, prompt):
    # Now you can use the vector store to search for similar texts
    results = vector_store.similarity_search(user_query)
    context = results[0].page_content
    prompt.append({"role": "user", "content": user_query})
    prompt.append({"role": "user", "content": context})
    # Send and receive request using Chat
    response= openai_client.chat.completions.create(
        model= "gpt-3.5-turbo-0613",
        messages= prompt,
        temperature=0,
        max_tokens=150
    )

    chat_message= response.choices[0].message.content
    return chat_message

  