
import bson.objectid
from pymongo import MongoClient

class ManagerMongo:
    def __init__(self):
        self.MONGO_URL = "mongodb+srv://{0}:{1}@{2}"
        self.cliente: MongoClient = None
        self.db: Database = None
        self.cursorcoleccion: Collection = None
        self.cursoradmin: Collection = None

    def conectDB(self, usuario, password, host, db, coleccion):
        try:
            self.cliente = MongoClient(self.MONGO_URL.format(usuario, password, host), ssl_cert_reqs=False)
            self.db = self.cliente[db]
            self.cursorcoleccion = self.db[coleccion]
            self.cursorusuarios = self.db["usuarios"]

        except ConnectionFailure:
            raise Exception("Servidor no disponible")
        
    def comprobarlogin(self, usuario, password):
        ok = self.cursorusuarios.find_one({"usuario": usuario, "password": password})
        if ok != None:
            if len(ok) == 1:
                return True
        return False
    
    
    def insertarelemento(self, usuario, tirada: list, puntuacion_total):
        
        ok = self.cursorcoleccion.insert_one(
            {
                "usuario": usuario,
                "tirada": tirada,
                "puntuacion_total": puntuacion_total
            
            })
        if ok.inserted_id != None:
            return True
        return False
    
managermongo = ManagerMongo()
managermongo.conectDB("pepito", "pepito", "cluster0-6oq5a.gcp.mongodb.net", "dados", "tiradas" )
