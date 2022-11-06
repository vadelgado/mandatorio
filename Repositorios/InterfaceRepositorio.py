import pymongo
import certifi
from bson import DBRef #arcjivo JSON pero Binario
from bson.objectid import ObjectId
from typing import TypeVar, Generic, get_args, List, get_origin
import json

T = TypeVar('T')#Variable Generica BD

class InterfaceRepositorio(Generic[T]):
   #Constructor de la clase
    def __init__(self):
        ca = certifi.where()
        dataConfig = self.loadFileConfig()
        client = pymongo.MongoClient(dataConfig["data-db-connection"], tlsCAFile=ca)
        self.baseDatos = client[dataConfig["name-db"]]
        theClass = get_args(self.__orig_bases__[0])
        self.colleccion = theClass[0].__name__.lower()

    def loadFileConfig(self):
        with open('config.json') as f:
            data = json.load(f)
        return data

    def save(self, item: T):
        laColeccion = self.baseDatos[self.colleccion]
        elId = ""
        item = self.transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            elId = item._id
            _id = ObjectId(elId)
            laColeccion = self.baseDatos[self.colleccion]
            delattr(item, "_id")
            item = item.__dict__
            updateItem = {"$set": item}
            x = laColeccion.update_one({"_id": _id}, updateItem)
        else:
            _id = laColeccion.insert_one(item.__dict__)
            elId = _id.inserted_id.__str__()
        x = laColeccion.find_one({"_id": ObjectId(elId)})
        x["_id"] = x["_id"].__str__()
        return self.findById(elId)

    #Borrar
    def delete(self, id):
        laColeccion = self.baseDatos[self.colleccion]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": cuenta}

    #Actualizar
    def update(self, id, item: T):
        _id = ObjectId(id)
        laColeccion = self.baseDatos[self.colleccion]
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item}
        x = laColeccion.update_one({"_id": _id}, updateItem)#Lenguaje Mongo
        return {"updated_count": x.matched_count}

    #Funcion buscar por Id
    def findById(self, id):
        laColeccion = self.baseDatos[self.colleccion]
        x = laColeccion.find_one({"_id": ObjectId(id)})
        x = self.getValuesDBRef(x)
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x

    #Buscartodo en una Coleccion
    def findAll(self):
        laColeccion = self.baseDatos[self.colleccion]
        data = []
        for x in laColeccion.find():
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data
    #Consulta
    def query(self, theQuery):
        laColeccion = self.baseDatos[self.colleccion]
        data = []
        for x in laColeccion.find(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data
    #Consulta Especifica
    def queryAggregation(self, theQuery):
        laColeccion = self.baseDatos[self.colleccion]
        data = []
        for x in laColeccion.aggregate(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    #Obtener los valores de dbref
    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):#vienen ordenada
                laColeccion = self.baseDatos[x[k].collection]
                valor = laColeccion.find_one({"_id": ObjectId(x[k].id)})
                valor["_id"] = valor["_id"].__str__()
                x[k] = valor
                x[k] = self.getValuesDBRef(x[k])
            elif isinstance(x[k], list) and len(x[k]) > 0:#viene como lista
                x[k] = self.getValuesDBRefFromLis(x[k])
            elif isinstance(x[k], dict):
                x[k] = self.getValuesDBRef(x[k])
        return x

    # obtiene los valores de ref de una lista
    def getValuesDBRefFromLis(self, theList):
        newList = []
        laColeccion = self.baseDatos[theList[0]._id.collection]
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(item.id)})#linea con comando de mongo
            value["_id"] = value["_id"].__str__()#conv de bin a string
            newList.append(value)
        return newList

#Transformamos sus objetos en sus Ids
    def transformObjectIds(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId):
                x[attribute] = x[attribute].__str__()
            elif isinstance(x[attribute], list):
                x[attribute] = self.formatList(x[attribute])
            elif isinstance(x[attribute], dict):
                x[attribute] = self.transformObjectIds(x[attribute])
        return x

    #Formateamos una Lista
    def formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())

        if len(newList) == 0:
            newList = x
        return newList

    #Transforma las Referencias
    def transformRefs(self, item):
        theDict = item.__dict__
        keys = list(theDict.keys())
        for k in keys:
            if theDict[k].__str__().count("object") == 1:
                newObject = self.ObjectToDBRef(getattr(item, k))
                setattr(item, k, newObject)
        return item
    #Obtener los Objetos desde una referencia
    def ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower()
        return DBRef(nameCollection, ObjectId(item._id))