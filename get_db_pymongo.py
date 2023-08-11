from pymongo import MongoClient

def get_database():
   
   CONNECTION_STRING = "mongodb+srv://cluster0.yxmxbbi.mongodb.net/?authMechanism=MONGODB-X509&authSource=%24external&tls=true&tlsCertificateKeyFile=%2FUsers%2Fvivify%2FDownloads%2FX509-cert-1131158266968443415.pem"
 
   client = MongoClient(CONNECTION_STRING)
 
   return client['truckdb']