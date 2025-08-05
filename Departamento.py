class Departamento:
    """
    Representa un Departamento del Museo.
    
    Atributos:
    id (int): Identificador Unico del Departamento.
    nombre (str): Nombre del Autor.
    """

    def _init_(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def mostrar(self):
        """
        Funcion para mostrar un string
        Retorna un str con los atributos de la clase
        """

        return f"ID: {self.id}\nNombre: {self.nombre}\n\n"


