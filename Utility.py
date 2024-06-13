from langchain.text_splitter import  RecursiveCharacterTextSplitter
from openai import OpenAI
from azure.search.documents import SearchClient


API_Key = "sk-proj-FH8UWKIBBoADzwf5w1LAT3BlbkFJAYMxKC9BjCjgLGuaf1Dm"
Resource_Endpoint = "https://api.openai.com/"

client = OpenAI(api_key=API_Key)




recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)


def TextSplitter(text):
    chunks = recursive_text_splitter.split_text(text)
    return chunks


def GenerateEmbedding(text):
    response = client.embeddings.create(input=text,model="text-embedding-ada-002")
    embeddings = response.data[0].embedding
    return embeddings

def UploadDocument(document, search_service_endpoint,index_name,credential):
    try:
        search_client = SearchClient(endpoint=search_service_endpoint,index_name=index_name,credential=credential)
        search_client.upload_documents(documents=[document])
        print("document is uploaded")
    except Exception as e:
        print("Error occurred")
        print(e)

