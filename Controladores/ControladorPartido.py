from Repositorios.RepositorioPartido import RepositorioPartido
from Modelos.Partido import Partido

class ControladorPartido():
    def __init__(self):
        print("Creando ControladorPartido")
        self.repositorioPartido = RepositorioPartido()

    def index(self):
        print("Listar todos los Partido")
        return self.repositorioPartido.findAll()

    def create(self, infoPartido):
        print("Crear un Partido")
        nuevoPartido = Partido(infoPartido)
        return self.repositorioPartido.save(nuevoPartido)

    def show(self, id):
        print("Mostrando un Partido con id", id)
        elPartido = Partido(self.repositorioPartido.findById(id))
        return elPartido.__dict__

    def update(self, Id, infoPartido):
        print("Actualizando Partido con id", Id)
        partidoActual = Partido(self.repositorioPartido.findById(Id))
        partidoActual.nombre = infoPartido["nombre"]
        partidoActual.lema = infoPartido["lema"]
        return self.repositorioPartido.save(partidoActual)

    def delete(self, id):
        print("Eliminando Partido con id ", id)
        return self.repositorioPartido.delete(id)