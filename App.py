import requests 
from Departamento import Departamento
from Autor import Autor
from Obra import Obra
import time 

class App:
    """
    Representa la aplicacion en si.
    
   Atributos:
   deptos (list[Departamento]): lista de instancias de la clase Departamento que representa los departamentos del museo.
   autores (list[Autores]): lista de instancias de la clase Autor que representa los autores de las Obras que hay en el museo.
   obras (list[Obra]): lista de instancias de la clase Obra que representa las Obras del museo.
   nacionalidades (list[str]): lista de nacionalidades que representa las nacionalidades de los Autores de Obras del Museo.
   """

    def _init_(self):
        #Atributos inicializan vacios y se llenan con la API al inicializar el sistema
        self.deptos = []
        self.autores = []
        self.obras = []
        self.nacionalidades = []

    def cargar_deptos(self):
        """
        Cargar los departamentos de la API
        """
        #Respuesta que se recibira de la API
        response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")
       
        #Validar el status de la respuesta. Si es 200 es correcta si no avisar que hubo un error
        if response.status_code == 200:
            #Transformo la respuesta de la API en json
            data = response.json()
            
            #Obtengo la lista de departamentos del json anterior
            lista_deptos = data["departments"]

            #Itero sobre esa lista para obtener la info de los deptos y crear los objetos para agregarlos en la lista
            for info_depto in lista_deptos:

                id = info_depto["departmentId"] #Obtengo Id
                nombre = info_depto["displayName"] #Obtengo el nombre

                departamento = Departamento(id, nombre)

                self.deptos.append(departamento)
        else:
            print("Hubo algun error al intentar obtener los datos de la API")


    def cargar_obras_autores(self):
        """
        Cargar las obras a partir de la API y a su vez cargar los autores
        """
        pass

    def cargar_nacionalidades(self):
        """
        Cargar nacionalidades
        """
        pass
    
    def cargar(self):
        """
        Cargar TODA la informacion de sistema
        """
        print("\nCargando...")
        self.cargar_deptos()
        self.cargar_obras_autores()
        self.cargar_nacionalidades()
        print("... Informacion cargada Exitosamente")

    def listar_obras_deptos(self):
        """
        Mostrar al usuario una lista de los departamentos del museo, para luego seleccionar un departamento y mostrar las obras de ese departamento y seguido de eso que el usuario tenga la opcion de visualizar los detalles de la obra deseada.
        """
        pass

    def iniciar(self):
        """
        Inicializar la aplicacion cargando la info en el sistema y presentando al usuario un menu
        """
        self.cargar() #Cargar informacion

        #While True para que se ejecute el menu hasta que el usuario desee salir del sistema
        while True:
            print("\n===============================")
            print("     BIENVENIDOS A MetroArt")
            print("===============================")

            print("1. Ver lista de obras por Departamento.\n2. Ver lista de obras por Nacionalidad del Autor.\n3. Ver lista de obras por nombre del autor.\n4. Salir")

            option = input("\nIngrese la opcion correspondiente a la accion que desea realizar: ")
            #validar que la opcion sea un numero y la opcion se encuentre en el rango del 1 al 5 sin incluir el 5.
            while (not option.isnumeric()) or (not int(option) in range(1,5)):
                print("Error! Opcion invalida")
                option = input("\nIngrese la opcion correspondiente a la accion que desee realizar: ")

            if option == "1":
                self.listar_obras_deptos()
            elif option == "2":
                pass
            elif option == "3":
                pass
            else:
                print("\nAdios")
                break


