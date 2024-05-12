import pymongo
from llama_index.embeddings.openai import OpenAIEmbedding
import os
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings, Document
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.llms.ollama import Ollama
from contents import parse_blog_urls
from llama_index.llms.openai import OpenAI

def get_mongo_client(mongo_uri):
  """Establish connection to the MongoDB."""
  try:
    client = pymongo.MongoClient(mongo_uri)
    print("Connection to MongoDB successful")
    return client
  except pymongo.errors.ConnectionFailure as e:
    print(f"Connection failed: {e}")
    return None

def query(text, collection="collection"):
  mongo_uri = os.environ["MONGO_URI"]

  if not mongo_uri:
    print("MONGO_URI not set in environment variables")

  mongo_client = get_mongo_client(mongo_uri)

  DB_NAME = "DB"
  COLLECTION_NAME = collection

  db = mongo_client[DB_NAME]
  collection = db[COLLECTION_NAME]

  atlas_vector_search = MongoDBAtlasVectorSearch(
      mongo_client,
      db_name = DB_NAME,
      collection_name = COLLECTION_NAME,
      index_name = "vector_index",
  )

  print(DB_NAME, COLLECTION_NAME)

  # Retrieve vector store index for query.
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

  Settings.embed_model = OpenAIEmbedding(
              model = "text-embedding-3-small",
              embed_batch_size=100
          )

  Settings.llm = Ollama(model="llama3:70b")

  atlas_vector_search = MongoDBAtlasVectorSearch(
      mongo_client,
      db_name = db_name,
      collection_name = collection_name,
      index_name = "vector_index",
  )

#   documents = SimpleDirectoryReader("../data/pottery").load_data()
  documents = SimpleDirectoryReader("../data/pottery").load_data()
  print(len(documents))
  vector_store_context = StorageContext.from_defaults(vector_store=atlas_vector_search)
  VectorStoreIndex.from_documents(
    documents, storage_context=vector_store_context, show_progress=True
  )

# create_database(db_name="DB", collection_name="pottery")
# create_database(db_name="DB", collection_name="collection")
# print(query("find articles related to embedding"))
# print(query("What is glazing pottery?", collection="pottery"))
# print(query("Olivia wants to learn how to do pottery. What would you recommend her to do? And why? ", collection="pottery"))