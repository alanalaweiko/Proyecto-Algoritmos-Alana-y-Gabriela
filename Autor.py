class Autor:
    """
    Representa un Autor.
    
    Atributos:
    nombre (str): Nombre del Autor.
    nacionalidad (str): Nacionalidad del Autor.
    fecha_nac (str): Fecha de Nacimiento del Autor.
    fecha_muerte (str): Fecha de Muerte del Autor.
    """
    
    def _init_(self, nombre, nacionalidad, fecha_nac, fecha_muerte):
        self.nombre = nombre
        self.nacionalidad = nacionalidad
        self.fecha_nac = fecha_nac
        self.fecha_muerte = fecha_muerte

    def mostrar(self):
        return f"Nombre: {self.nombre}\nNacionalidad: {self.nacionalidad}\nFecha de Nacimiento: {self.fecha_nac}\nFecha de Muerte: {self.fecha_muerte}"
