import os
from openai import OpenAI
import pdfplumber
from Utility import TextSplitter, GenerateEmbedding,UploadDocument
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import(SearchField,SearchFieldDataType,SearchIndex,SimpleField,SearchableField,SemanticConfiguration,VectorSearch,HnswAlgorithmConfiguration,VectorSearchProfile)
from azure.search.documents.models import VectorizedQuery
from azure.search.documents import SearchClient


API_Key = "sk-proj-FH8UWKIBBoADzwf5w1LAT3BlbkFJAYMxKC9BjCjgLGuaf1Dm"
Resource_Endpoint = "https://api.openai.com/"


Search_Service_Keys = "TAt1YgTQUVWUfmKwv1oDpWqsa83VhVpUftvqyvG68YAzSeDfNBDA"
Search_Service_EndPoint = "https://openai-search-service-genai.search.windows.net"
indexName = "vectortable"

credential = AzureKeyCredential(Search_Service_Keys)

search_client= SearchClient(endpoint=Search_Service_EndPoint,index_name=indexName,credential=credential)
client = OpenAI(api_key=API_Key)


indexClient = SearchIndexClient(Search_Service_EndPoint,credential)


query = input("Enter Query to search: ")


queryVector = GenerateEmbedding(query)


vector_query = VectorizedQuery(vector=queryVector,k_nearest_neighbors=5,fields="contentVector")

results = search_client.search(
    search_text=None,
    vector_queries=[vector_query],
    select=["content"],
    top=4
)

print(results)
context = []
for result in results:
    context.append(result.get("content"))


prompt = """ You are a chatbot. Please respond to the user query below only from the context. Pls provide a brief answer to help user understand and don't hide any numbers or figures. If you don't find an answer from the context, just say "Sorry, I can't help you with this query"
Query : {Query}
Context : {Context}
"""

openaiResult = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt.format(Query=query,Context=context)
        }
      ]
    }
  ]
)

print(openaiResult.choices[0].message.content)

