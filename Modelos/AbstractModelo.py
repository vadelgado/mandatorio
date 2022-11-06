from abc import ABCMeta #Descompone y convierte en un diccionario
#Aca esta el constructor que los demas modelos va a utiñizar
#constructor especial el cual permitirá instanciar un objeto del tipo requerido a partir de la información almacenada en un diccionario,
class AbstractModelo(metaclass=ABCMeta):
    def __init__(self, data):
        for llave, valor in data.items():
            setattr(self, llave, valor)