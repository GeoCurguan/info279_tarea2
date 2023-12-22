import os
import pandas as pd
from llama_index.llms import HuggingFaceInferenceAPI, HuggingFaceLLM
from llama_index import StorageContext, load_index_from_storage, ServiceContext, VectorStoreIndex, SimpleDirectoryReader
from geopy.geocoders import Nominatim
import spacy
import requests

from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
HF_TOKEN = os.getenv('HF_API_KEY')
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

los_rios = pd.read_csv('noticias-losrios-2023.csv')
test = pd.read_csv('test/dataset-test-desafio2.csv')

documents = SimpleDirectoryReader('data').load_data()
# print("Vectorización de los datos...")
# index = VectorStoreIndex.from_documents(documents)
# index.storage_context.persist()
# print("Vectores guardados en la carpeta ./storage")

# remotely_run = HuggingFaceInferenceAPI(
#     model_name="HuggingFaceH4/zephyr-7b-alpha", token=HF_TOKEN
# )

# service_context = ServiceContext.from_defaults(chunk_size=512, llm=remotely_run)

# index = VectorStoreIndex.from_documents(
#     documents, service_context=service_context
# )

# query_engine = index.as_query_engine()

remotely_run = HuggingFaceInferenceAPI(
    model_name="HuggingFaceH4/zephyr-7b-alpha", token=HF_TOKEN
)

question=""".Read the following news article and tell me what is the main event (try to be the more specific). Your response will be formatted in CSV with one column: main event"""

def main_event(new: str) -> str:
    query_event = question+": "+ new
    completion_response = remotely_run.complete(query_event)
    # response_event = query_engine.query(query_event)
    return str(completion_response)
# new = test['text'][12]
# print(main_event(new))

test['event'] = test['text'].apply(main_event)
test.to_csv("test_events_new.csv")
# promp_1 = """.Read the following summary and tell me where does the main event takes place (limit yourself to just providing an address or location, without additional text).
# Do not infer additional information such as numbers and street names. Your response will be formatted in CSV with one columns: location"""

# promp_2 = """.Read the following summary, extract the geographical location where the main event of the text occurs. If the event is held at a specific organization or location, mention it.
# Your response will be formatted in CSV with one columns: location"""

# query_address = promp_2+": "+main_event
# response_address = query_engine.query(query_address)
# address = str(response_address.response)

# Traducción de address al español
# API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-es"
# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()
	
# output = query({"inputs": address})
# text_es = str(output[0]['translation_text'])

# Procesamiento de entidades
# nlp_en = spacy.load("en_core_web_sm")
# doc_en = nlp_en(address)
# print("Ubicación en inglés: ",doc_en,"\n")
# for ent in doc_en.ents:
#     if ent.label_ == "LOC" or ent.label_ == "GPE":
#         print(ent.text, ent.label_)


# nlp_es = spacy.load("es_core_news_sm")
# doc_es = nlp_es(text_es)
# print("Traducción al español (ubicación): ",doc_es,"\n")
# for ent in doc_es.ents:
#     if ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "PER":
#         print(ent.text, ent.label_)

#Final: Geolocalizar
# geolocator = Nominatim(user_agent="Sophia")
# location = geolocator.geocode(place)
# # print(location)
# # print((location.latitude, location.longitude))
# # geolocator = Nominatim(user_agent="specify_your_app_name_here")
# print(location)
