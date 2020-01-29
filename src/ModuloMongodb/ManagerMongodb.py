import bson.objectid
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


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
            if len(ok) >= 1:
                return True
        return False

    def insertarelemento(self, elemento: dict):
        resultado_puntuacionmaxima = self.cursorcoleccion.find_one({"_id": elemento["usuario"] })
        maximo = resultado_puntuacionmaxima["maxima_puntuacion"]
        if elemento["puntuacion_total"] > resultado_puntuacionmaxima["maxima_puntuacion"]:
            ok = self.cursorcoleccion.update_one(
                {"_id": elemento["usuario"]},
                {'$set': {"maxima_puntuacion": elemento["puntuacion_total"]}}
            )
            maximo = elemento["puntuacion_total"]

        ok = self.cursorcoleccion.insert_one(elemento)
        if ok.inserted_id != None:
            return True, maximo
        return False
    
    def getall(self, usuario):
        resultados = list(self.cursorcoleccion.find(
            {"usuario": usuario}, {"_id": False}))
        if resultados != None:
            if len(resultados) > 0:
                return resultados
        return None



managermongo = ManagerMongo()
managermongo.conectDB("pepito", "pepito", "cluster0-6oq5a.gcp.mongodb.net", "dados", "tiradas")
