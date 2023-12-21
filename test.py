import os
import pandas as pd
from llama_index.llms import HuggingFaceInferenceAPI, HuggingFaceLLM
from llama_index import StorageContext, load_index_from_storage, ServiceContext, VectorStoreIndex, SimpleDirectoryReader
from geopy.geocoders import Nominatim
import spacy
import requests

os.environ['OPENAI_API_KEY'] = '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'
os.environ['HF_API_KEY'] = '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'

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
HF_KEY = os.getenv('HF_API_KEY')
headers = {"Authorization": f"Bearer {HF_KEY}"}

los_rios = pd.read_csv('noticias-losrios-2023.csv')
test = pd.read_csv('test/dataset-test-desafio2.csv')
news_article=test['text'][30]
print(news_article+"\n")

documents = SimpleDirectoryReader('data').load_data()
# print("Vectorización de los datos...")
# index = VectorStoreIndex.from_documents(documents)
# index.storage_context.persist()
# print("Vectores guardados en la carpeta ./storage")

remotely_run = HuggingFaceInferenceAPI(
    model_name="HuggingFaceH4/zephyr-7b-alpha", token=HF_KEY
)

service_context = ServiceContext.from_defaults(chunk_size=512, llm=remotely_run)

index = VectorStoreIndex.from_documents(
    documents, service_context=service_context
)

query_engine = index.as_query_engine()

question=""".Read the following news article and tell me what is the main event (try to be the more specific). Your response will be formatted in CSV with one columns: main event"""

query_event = question+": "+news_article
response_event = query_engine.query(query_event)
main_event = str(response_event.response)
# print(main_event+"\n")

question_address=""".Read the following summary and tell me where does the main event take place (limit yourself to just providing an address or location, without additional text). 
Your response will be formatted in CSV with one columns: location"""
query_address = question_address+": "+main_event
response_address = query_engine.query(query_address)
address = str(response_address.response)
# print(address+"\n")

API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-es"
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({"inputs": address})
text = str(output[0]['translation_text'])

nlp = spacy.load("es_core_news_sm")
doc = nlp(text)
print("Texto traducido al español: ",doc,"\n")
for ent in doc.ents:
    if ent.label_ == "LOC" or ent.label_ == "GPE":
        print(ent.text, ent.label_)

#Final: Geolocalizar
# geolocator = Nominatim(user_agent="Sophia")
# location = geolocator.geocode(place)
# # print(location)
# # print((location.latitude, location.longitude))
# # geolocator = Nominatim(user_agent="specify_your_app_name_here")
# print(location)
