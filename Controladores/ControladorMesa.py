from Repositorios.RepositorioMesa import RepositorioMesa
from Modelos.Mesa import Mesa

class ControladorMesa():
    def __init__(self):#CONSTRUCTOR
        print("Creando ControladorMesa")
        self.repositorioMesa = RepositorioMesa()

    def index(self):
        print("Listar todas las Mesa")
        return self.repositorioMesa.findAll()

    def create(self, infoMesa):
        print("Crear una Mesa")
        unaMesa = Mesa(infoMesa)
        return self.repositorioMesa.save(unaMesa)

    def show(self, id):
        print("Mostrando una Mesa  con numero", id)
        unaMesa = Mesa(self.repositorioMesa.findById(id))
        return unaMesa.__dict__

    def update(self, id, infoMesa):
        print("Actualizando Mesa con numero", id)
        mesaActual = Mesa(self.repositorioMesa.findById(id))
        mesaActual.numero = infoMesa["numero"]
        mesaActual.cantidad_inscritos=infoMesa["cantidad_inscritos"]
        return self.repositorioMesa.save(mesaActual)

    def delete(self, id):
        print("Eliminando Mesa con numero ", id)
        return self.repositorioMesa.delete(id)