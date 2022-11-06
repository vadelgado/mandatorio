from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS  # Para rebase Unitarians
import json
from waitress import serve

"""
import pymongo
import certifi
"""
from Controladores.ControladorCandidato import ControladorCandidato
from Controladores.ControladorMesa import ControladorMesa
from Controladores.ControladorPartido import ControladorPartido
from Controladores.ControladorResultado import ControladorResultado

# Initio Implementation del Servitor
app = Flask(__name__)
cors = CORS(app)
"""
ca=certifi.where()
client=pymongo.MongoClient("mongodb+srv://admin:1234@cluster0.m665q1z.mongodb.net/db-mandatorio?retryWrites=true&w=majority",tlsCAFile=ca)
db = client.test
print(db)

baseDatos = client["db-mandatorio"]
print(baseDatos.list_collection_names())
"""
miControladorCandidato = ControladorCandidato()
miControladorMesa = ControladorMesa()
miControladorPartido = ControladorPartido()
miControladorResultado = ControladorResultado()


# ******************************************************Resultado*******************************************************#
# obtener todos los resultados
@app.route("/resultado/", methods=['GET'])
def getResultados():
    json = miControladorResultado.index()
    return jsonify(json)


# A;adir resultado a una mesa

@app.route("/resultado/mesa/<string:id_mesa>/candidato/<string:id_candidato>", methods=['POST'])
def crearResultado(id_mesa, id_candidato):
    data = request.get_json()
    json = miControladorResultado.create(data, id_mesa, id_candidato)
    return jsonify(json)


# Obtener Resultado Específico

@app.route("/resultado/<string:id>", methods=['GET'])
def getResultado(id):
    json = miControladorResultado.show(id)
    return jsonify(json)

# Modificar Un resultado

@app.route("/resultado/<string:id>/mesa/<string:id_mesa>/candidato/<string:id_candidato>", methods=['PUT'])
def modificarResultado(id, id_mesa, id_candidato):
    data = request.get_json()
    json = miControladorResultado.update(id, data, id_mesa, id_candidato)
    return jsonify(json)

# Eliminar un Resultado

@app.route("/resultado/<string:id_resultado>", methods=['DELETE'])
def eliminarResultado(id_resultado):
    json = miControladorResultado.delete(id_resultado)
    return jsonify(json)

#Buscar los candidatos votados en una Mesa
@app.route("/resultado/mesa/<string:id_mesa>", methods={'GET'})
def inscritosMesa(id_mesa):
    json = miControladorResultado.getListarCandidatosMesa(id_mesa)
    return jsonify(json)

#Buscar el candidato en la Mesa
@app.route("/resultado/candidato/<string:id_candidato>", methods={'GET'})
def inscritoEnMesa(id_candidato):
    json = miControladorResultado.getListarMesasDeIncritoCandidato(id_candidato)
    return jsonify(json)

#Buscar mayor cedula
@app.route("/resultado/maxdocument",methods={'GET'})
def getMaxDocument():
    json = miControladorResultado.getMayorCedula()
    return jsonify(json)



# ******************************************************Resultado*******************************************************#

# ****************************************************Partido***********************************************************#
@app.route("/partido", methods=['GET'])
def getPartidos():
    json = miControladorPartido.index()
    return jsonify(json)


@app.route("/partido", methods=['POST'])
def crearPartido():
    data = request.get_json()
    json = miControladorPartido.create(data)
    return jsonify(json)


@app.route("/partido/<string:id_partido>", methods=['GET'])
def getPartido(id_partido):
    json = miControladorPartido.show(id_partido)
    return jsonify(json)


@app.route("/partido/<string:id_partido>", methods=['PUT'])
def modificarPartido(id_partido):
    data = request.get_json()
    json = miControladorPartido.update(id_partido, data)
    return jsonify(json)


@app.route("/partido/<string:id_partido>", methods=['DELETE'])
def eliminarPartido(id_partido):
    json = miControladorPartido.delete(id_partido)
    return jsonify(json)


# ****************************************************Partido***********************************************************#

# ****************************************************Candidato*********************************************************#

@app.route("/candidato/<string:id>/partido/<string:id_partido>", methods=['PUT'])
def asignarPartidoACandidato(id, id_partido):
    json = miControladorCandidato.asignarPartido(id, id_partido)
    return jsonify(json)


@app.route("/candidato", methods=['GET'])
def getCandidatos():
    json = miControladorCandidato.index()
    return jsonify(json)


@app.route("/candidato", methods=['POST'])
def crearCandidato():
    data = request.get_json()
    json = miControladorCandidato.create(data)
    return jsonify(json)


@app.route("/candidato/<string:id>", methods=['GET'])
def getCandidato(id):
    json = miControladorCandidato.show(id)
    return jsonify(json)


@app.route("/candidato/<string:id>", methods=['PUT'])
def modificarCandidato(id):
    data = request.get_json()
    json = miControladorCandidato.update(id, data)
    return jsonify(json)


@app.route("/candidato/<string:id>", methods=['DELETE'])
def eliminarCandidato(id):
    json = miControladorCandidato.delete(id)
    return jsonify(json)


# ****************************************************Candidato*********************************************************#

# ******************************************************Mesas***********************************************************#
@app.route("/mesa", methods=['GET'])
def getMesas():
    json = miControladorMesa.index()
    return jsonify(json)


@app.route("/mesa", methods=['POST'])
def crearMesa():
    data = request.get_json()
    json = miControladorMesa.create(data)
    return jsonify(json)


@app.route("/mesa/<string:id_mesa>", methods=['GET'])
def getMesa(id_mesa):
    json = miControladorMesa.show(id_mesa)
    return jsonify(json)


@app.route("/mesa/<string:id_mesa>", methods=['PUT'])
def modificarMesa(id_mesa):
    data = request.get_json()
    json = miControladorMesa.update(id_mesa, data)
    return jsonify(json)


@app.route("/mesa/<string:id_mesa>", methods=['DELETE'])
def eliminarMesa(id_mesa):
    json = miControladorMesa.delete(id_mesa)
    return jsonify(json)


# ******************************************************Mesas***********************************************************#

# Servicio retornar un JSON el cual tiene un mensaje que dice el servidor está corriendo
@app.route("/", methods=['GET'])
def test():
    json = {}
    json["message"] = "Server running ..."
    return jsonify(json)


# Fin Servicio Json
# Metodo cargar configuracion
def loadFileConfig():
    with open('config.json') as f:  # Abrir archivo Guardarlo en la variable f
        data = json.load(f)
    return data


if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running : " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])  # Se arranca el Servidor
# Fin Implementación del Servidor
