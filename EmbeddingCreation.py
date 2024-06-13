import os
from openai import OpenAI
import pdfplumber
from Utility import TextSplitter, GenerateEmbedding,UploadDocument
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import(SearchField,SearchFieldDataType,SearchIndex,SimpleField,SearchableField,SemanticConfiguration,VectorSearch,HnswAlgorithmConfiguration,VectorSearchProfile)
import pandas as pd


API_Key = "sk-proj-FH8UWKIBBoADzwf5w1LAT3BlbkFJAYMxKC9BjCjgLGuaf1Dm"
Resource_Endpoint = "https://api.openai.com/"


Search_Service_Keys = "TAt1YgTQUVWUfmKwv1oDpWqsa83VhVpUftvqyvG68YAzSeDfNBDA"
Search_Service_EndPoint = "https://openai-search-service-genai.search.windows.net"
index_name = "vectortable"

credential = AzureKeyCredential(Search_Service_Keys)

indexClient = SearchIndexClient(Search_Service_EndPoint,credential)

indexExist=False


vector_search = VectorSearch(
        profiles=[VectorSearchProfile(name="my-vector-config", algorithm_configuration_name="my-algorithms-config")],
        algorithms=[HnswAlgorithmConfiguration(name="my-algorithms-config")],
    )

fields = [
    SimpleField(name="id",type=SearchFieldDataType.String,key=True),
    SimpleField(name="content",type=SearchFieldDataType.String,key=False),
    SearchField(name="contentVector",type=SearchFieldDataType.Collection(SearchFieldDataType.Single),searchable=True,vector_search_dimensions=1536,vector_search_profile_name="my-vector-config")
]



for index in indexClient.list_index_names():
    if(index==index_name):
        indexExist=True

if (indexExist is False):
    index = SearchIndex(name=index_name,fields=fields,vector_search=vector_search)
    indexClient.create_or_update_index(index)
    print("index created")

#client = OpenAI()

# Open the PDF file




def PDF_Embeddings():
    Extracted_Text=""
    with pdfplumber.open(r"C:\Users\thaku\Downloads\budget_speech.pdf") as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            Extracted_Text = Extracted_Text + text


    chunks = TextSplitter(Extracted_Text)
    i=0
    for chunk in chunks:
        print("==========================================")
        contentVector = GenerateEmbedding(chunk)
        content = chunk
        i = i+1
        document = {"id":str(i),"content":content,"contentVector":contentVector}
        UploadDocument(document,Search_Service_EndPoint,index_name,credential)
        print(i)

def Excel_Embeddings():
    Extracted_Text = ""
    df = pd.read_excel(r"C:\Users\thaku\Downloads\FAQDate.xlsx")
    for index, row in df.iterrows():
        Extracted_Text = Extracted_Text+" Question:"+row['Question'] + " Answer:" + row['Answer'] 
        
    print(Extracted_Text)
    chunks = TextSplitter(Extracted_Text)
    i=26
    for chunk in chunks:
        print("==========================================")
        contentVector = GenerateEmbedding(chunk)
        content = chunk
        i = i+1
        document = {"id":str(i),"content":content,"contentVector":contentVector}
        UploadDocument(document,Search_Service_EndPoint,index_name,credential)
        print(i)

Excel_Embeddings()


    










