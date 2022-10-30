from Repositorios.RepositorioResultado import RepositorioResultado
from Modelos.Resultado import Resultado

class ControladorResultado():
    def __init__(self):
        print("Creando ControladorResultado")
        self.repositorioResultado = RepositorioResultado()

    def index(self):
        print("Listar todos los Resultados")
        return self.repositorioResultado.findAll()

    def create(self,infoResultado):
        print("Crear un Resultado")
        nuevoResultado = Resultado(infoResultado)
        return self.repositorioResultado.save(nuevoResultado)

    def show(self,id):
        print("Mostrando un  Resultado con id", id)
        elResultado = Resultado(self.repositorioResultado.findById(id))
        return elResultado.__dict__

    def update(self, id, infoResultado):
        print("Actualizando  Resultado con id", id)
        resultadoActual = Resultado(self.repositorioResultado.findById(id))
        resultadoActual.numero_Mesa = infoResultado["numero_Mesa"]
        resultadoActual.cedula_candidato = infoResultado["cedula_candidato"]
        resultadoActual.numero_votos = infoResultado["numero_votos"]
        return self.repositorioResultado.save(resultadoActual)

    def delete(self, id):
        print("Eliminando  Resultado con id ", id)
        return self.repositorioResultado.delete(id)