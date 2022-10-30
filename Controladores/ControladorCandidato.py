from Modelos.Candidato import Candidato
from Repositorios.RepositorioCandidato import RepositorioCandidato

class ControladorCandidato():
    def __init__(self):
        print("Creando ControladorCandidato")
        self.repositorioCandidato = RepositorioCandidato()

    def index(self):
        print("Listar todos los Candidato")
        return self.repositorioCandidato.findAll()

    def create(self,infocandidato):
        print("Crear un Candidato")
        nuevoCandidato = Candidato(infocandidato)
        return self.repositorioCandidato.save(nuevoCandidato)

    def show(self,id):
        print("Mostrando un  Candidato con id", id)
        unCandidato = Candidato(self.repositorioCandidato.findById(id))
        return unCandidato.__dict__

    def update(self,id, infocandidato):
        print("Actualizando Candidato con id", id)
        candidatoActual = Candidato(self.repositorioCandidato.findById(id))
        candidatoActual.cedula = infocandidato["cedula"]
        candidatoActual.numero_resolucion = infocandidato["numero_resolucion"]
        candidatoActual.nombre = infocandidato["nombre"]
        candidatoActual.apellido = infocandidato["apellido"]
        return self.repositorioCandidato.save(candidatoActual)

    def delete(self, id):
        print("Eliminando Candidato con id ", id)
        return self.repositorioCandidato.delete(id)