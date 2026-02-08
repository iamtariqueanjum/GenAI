from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()


def process_query(query: str):
    
    print("Searching similar chunks...", query)
    
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-large"
    )
    vector_db = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name="learning_rag",
        embedding=embedding_model
    )
    search_results = vector_db.similarity_search(query=query)
    
    print("Generating context...")
    
    context = "\n\n\n".join([
        f"""Page Content: {result.page_content}\n
        Page Number: {result.metadata['page_label']}\n
        File Location: {result.metadata['source']}""" 
        for result in search_results
    ])
    SYSTEM_PROMPT = f"""
    You are a helpful AI assistant who answers user query based on the available
    context retrieved from a PDF file along with page_contents and page_number

    You should only answer based on the following context and navigate the user
    to the right page numbers to know more.

    Context: {context}
    """

    print("Calling OpenAI...")
    
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "system", "content": SYSTEM_PROMPT,
            "role": "user", "content": query
        }]
    )
    print(f"🤖: {response.choices[0].message.content}")
    return response.choices[0].message.content