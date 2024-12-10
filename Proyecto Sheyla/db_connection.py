import pymongo
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
MONGO_DB_NAME = "cinemotion"
#coneccion a bd
def get_database():
    try:
        
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        client.server_info()
        return client[MONGO_DB_NAME]
    except ServerSelectionTimeoutError as e:
        print(f"Error: No se pudo conectar al servidor MongoDB. Tiempo excedido. Detalles: {e}")
        raise
    except ConnectionFailure as e:
        print(f"Error: Falló la conexión con MongoDB. Detalles: {e}")
        raise
#Obtiene la coleccion de mongo
def get_collection(collection_name):
   
    db = get_database()
    return db[collection_name]

