from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Resultado import Resultado
from bson import ObjectId

class RepositorioResultado(InterfaceRepositorio[Resultado]):
    #Da las votaciones por mesa
    def getListadoCandidatosInscritosMesa(self, id_mesa):
        theQuery = {"mesa.$id": ObjectId(id_mesa)}
        return self.query(theQuery)

    #Da las votaciones por candidato

    def getListadoMesasCandidatoInscrito(self, id_candidato):
        theQuery = {"candidato.$id": ObjectId(id_candidato)}
        return self.query(theQuery)

    def getsumatoriaVotos(self, id_candidato):
        consulta1 = {
            "$match": {"candidato.$id": ObjectId(id_candidato)}
        }
        consulta2 = {
            "$group": {
                "_id": "$candidato",
                "Total_Votos": {
                    "$sum": "$numero_votos"
                }
            }
        }
        pipeline = [consulta1, consulta2]
        return self.queryAggregation(pipeline)