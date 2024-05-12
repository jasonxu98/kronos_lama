import pymongo
from llama_index.embeddings.openai import OpenAIEmbedding
import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.llms.ollama import Ollama

def get_mongo_client(mongo_uri):
  """Establish connection to the MongoDB."""
  try:
    client = pymongo.MongoClient(mongo_uri)
    print("Connection to MongoDB successful")
    return client
  except pymongo.errors.ConnectionFailure as e:
    print(f"Connection failed: {e}")
    return None

def query(text):
  mongo_uri = os.environ["MONGO_URI"]

  if not mongo_uri:
    print("MONGO_URI not set in environment variables")

  mongo_client = get_mongo_client(mongo_uri)

  DB_NAME = "DB"
  COLLECTION_NAME = "collection"

  db = mongo_client[DB_NAME]
  collection = db[COLLECTION_NAME]

  embed_model = OpenAIEmbedding(
              model = "text-embedding-3-large",
              embed_batch_size=100
          )

  Settings.embed_model = embed_model

  
  Settings.llm = Ollama(model="llama3:70b")

  atlas_vector_search = MongoDBAtlasVectorSearch(
      mongo_client,
      db_name = DB_NAME,
      collection_name = COLLECTION_NAME,
      index_name = "vector_index",
      embedding_key="embedding"
  )
#   vector_store_context = StorageContext.from_defaults(vector_store=atlas_vector_search)

  # vector_store_index = VectorStoreIndex.from_documents(
  #    documents, storage_context=vector_store_context, show_progress=True
  # )

  vector_store_index = VectorStoreIndex.from_vector_store(vector_store=atlas_vector_search)

  response = vector_store_index.as_query_engine().query(text)
  return str(response)

def create_database(db_name, collection_name):
  mongo_uri = os.environ["MONGO_URI"]
  if not mongo_uri:
    print("MONGO_URI not set in environment variables")

  mongo_client = get_mongo_client(mongo_uri)

  db = mongo_client[db_name]
  collection = db[collection_name]

  # Ensure we have fresh new collection when we recreate the database.
  collection.delete_many({})

  # Load documents
  documents = SimpleDirectoryReader("../data").load_data()

  Settings.embed_model = OpenAIEmbedding(
              model = "text-embedding-3-large",
              embed_batch_size=100
          )

  Settings.llm = Ollama(model="llama3:70b")

  atlas_vector_search = MongoDBAtlasVectorSearch(
      mongo_client,
      db_name = db_name,
      collection_name = collection_name,
      index_name = "vector_index",
      embedding_key="embedding"
  )

  vector_store_context = StorageContext.from_defaults(vector_store=atlas_vector_search)
  return VectorStoreIndex.from_documents(
     documents, storage_context=vector_store_context, show_progress=True
  )
create_database(db_name="DB", collection_name="collection")