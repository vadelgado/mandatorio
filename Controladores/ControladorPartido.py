from Repositorios.RepositorioPartido import RepositorioPartido
from Modelos.Partido import Partido

class ControladorPartido():
    def __init__(self):
        print("Creando ControladorPartido")
        self.repositorioPartido = RepositorioPartido()
    #Devuelce todos los documentos
    def index(self):
        print("Listar todos los Partido")
        return self.repositorioPartido.findAll()
    #Crea Documentos
    def create(self, info_partido):
        print("Crear un Partido")
        nuevo_partido = Partido(info_partido)
        return self.repositorioPartido.save(nuevo_partido)
    #Muestra un Documento
    def show(self, id):
        print("Mostrando un Partido con id", id)
        elPartido = Partido(self.repositorioPartido.findById(id))
        return elPartido.__dict__
    #Actualizar un Documento
    def update(self, Id, infoPartido):
        print("Actualizando Partido con id", Id)
        partidoActual = Partido(self.repositorioPartido.findById(Id))
        partidoActual.nombre = infoPartido["nombre"]
        partidoActual.lema = infoPartido["lema"]
        return self.repositorioPartido.save(partidoActual)
    #Borra un Documento
    def delete(self, id):
        print("Eliminando Partido con id ", id)
        return self.repositorioPartido.delete(id)