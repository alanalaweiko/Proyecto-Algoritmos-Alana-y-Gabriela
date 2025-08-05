class Obra:
    """
    Representa una Obra.
    
    Atributos:
    titulo (str): Titulo de la Obra.
    depto (Departamento): Instancia de la clase Departamento que representa el depto al cual pertenece la obra.
    autor (Autor): Instancia de la clase Autor que representa el autor de la obra.
    tipo (str): Tipo (classification) de la obra.
    anio_creacion (int): Año de creacion de la obra.
    imagen (str): URL de la imagen de la obra.
    """

    def _init_(self, titulo, depto, autor, tipo, anio_creacion, imagen):
        self.titulo = titulo
        self.depto = depto
        self.autor = autor
        self.tipo = tipo
        self.anio_creacion = anio_creacion
        self.imagen = imagen

        