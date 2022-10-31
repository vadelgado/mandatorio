from Modelos.Resultado import Resultado
from Modelos.Candidato import Candidato
from Modelos.Mesa import Mesa
from Repositorios.RepositorioResultado import RepositorioResultado
from Repositorios.RepositorioCandidato import RepositorioCandidato
from Repositorios.RepositorioMesa import RepositorioMesa


class ControladorResultado:
    def __init__(self):
        print("Creando ControladorResultado")
        self.repositorioResultado = RepositorioResultado()
        self.repositorioMesa = RepositorioMesa()
        self.repositorioCandidato = RepositorioCandidato()

    def index(self):
        print("Listar todos los Resultados")
        return self.repositorioResultado.findAll()

    # Asignacion Candidato y Mesa a Resultado
    def create(self, info_resultado, id_mesa, id_candidato):
        print("Crear un Resultado")
        nuevo_resultado = Resultado(info_resultado)
        la_mesa = Mesa(self.repositorioMesa.findById(id_mesa))
        candidate = Candidato(self.repositorioCandidato.findById(id_candidato))
        nuevo_resultado.candidato = candidate
        nuevo_resultado.mesa = la_mesa
        return self.repositorioResultado.save(nuevo_resultado)

    # def create(self,infoResultado):
    #     print("Crear un Resultado")
    #     nuevoResultado = Resultado(infoResultado)
    #     return self.repositorioResultado.save(nuevoResultado)

    def show(self, id):
        print("Mostrando un  Resultado con id", id)
        el_resultado = Resultado(self.repositorioResultado.findById(id))
        return el_resultado.__dict__

    def update(self, id, info_resultado, id_mesa, id_candidato):
        print("Actualizando  Resultado con id", id)
        resultado_actual = Resultado(self.repositorioResultado.findById(id))
        resultado_actual.numero_votos = info_resultado["numero_votos"]
        la_mesa = Mesa(self.repositorioMesa.findById(id_mesa))
        candidate = Candidato(self.repositorioCandidato.findById(id_candidato))
        resultado_actual.candidato = candidate
        resultado_actual.mesa = la_mesa
        return self.repositorioResultado.save(resultado_actual)

    #    def update(self, id, infoResultado):
    #        print("Actualizando  Resultado con id", id)
    #        resultadoActual = Resultado(self.repositorioResultado.findById(id))
    #        resultadoActual.numero_Mesa = infoResultado["numero_Mesa"]
    #        resultadoActual.cedula_candidato = infoResultado["cedula_candidato"]
    #        resultadoActual.numero_votos = infoResultado["numero_votos"]
    #        return self.repositorioResultado.save(resultadoActual)

    def delete(self, id):
        print("Eliminando  Resultado con id ", id)
        return self.repositorioResultado.delete(id)
