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

    def __init__(self):
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

    def buscar_depto(self,nombre):
        if len(self.deptos) != 0:
            for depto in self.deptos:
                if depto.nombre == nombre:
                    return depto
                
            id =len(self.deptos) + 3
            depto_nuevo = Departamento(id, nombre)
            self.deptos.append(depto_nuevo)

            return depto_nuevo
        else:
            return None
        
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
        self.cargar_nacionalidades()
        print("... Informacion cargada Exitosamente")


    def listar_obras_deptos(self):
        """
        Mostrar al usuario una lista de los departamentos del museo, para luego seleccionar un departamento y mostrar las obras de ese departamento y seguido de eso que el usuario tenga la opcion de visualizar los detalles de la obra deseada.
        """
        print("\n==============================")
        print("    SELECCIONE EL DEPARTAMENTO")
        print("==============================")
        count = 1
        for depto in self.deptos:
            print(f"{count}. {depto.nombre}")
            count+=1

            print(f"{count}. Salir")

            option = input("\nIngrese la opcion deseada: ")
            while (not option.isnumeric()) or (not int (option) in range(1, count+1)):
                print("\nError! Opcion invalida")
                option = input("Ingrese la opcion deseada: ")

            if int(option) != count:
                indice = int(option) - 1
                depto_select = self.deptos[indice]

                lista_obras = self.buscar_obras_deptos(depto_select)

               
    
   
    def buscar_obras_deptos(self, depto):
        """
        Consulta las obras de un departamento y las muestra de 20 en 20, dando al usuario la opción de ver detalles y de continuar o detener la paginación.

        Parámetro
        depto : Departamento
            Instancia que contiene, al menos, el atributo `id` del departamento a consultar.
        """
       
        # Solicita a la API del MET todos los IDs de obras del departamento
        response = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds={depto.id}")
    
        data = response.json()
        
        # Lista completa de IDs de obras en el departamento
        ids_obras = data["objectIDs"]

        total = len(ids_obras) # Cantidad total de obras
        index = 0              # Para ir de 20 en 20

        while index < total:
            bloque_ids = ids_obras[index: index+20] # Siguiente bloque de 20 IDs
            
            for id_b in bloque_ids:
                
                url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id_b}"

                #Se consulta el detalle de la obra individual
                response_obra = requests.get(url)

                data_obra = response_obra.json()

                # Busca si la obra ya está registrada en la colección local
                obra_actual = self.buscar_obra(data_obra["objectID"])
                
                # Ya existe: solo se muestra información básica
                if obra_actual != None:
                    print(f"ID: {obra_actual.id} - Titulo: {obra_actual.titulo}")
                else:
                    #No existe: se crea una nueva instancia de Obra (y, si es necesario, de Autor)
                    id_obra = data_obra["objectID"]
                    titulo = data_obra["title"]
                    tipo = data_obra["classification"]
                    anio_creacion = data_obra["objectDate"]
                    imagen = data_obra["primaryImage"]

                    # Comprueba si ya existe el autor; si no, lo crea y lo añade a la lista
                    autor = self.buscar_autor(data_obra["artistDisplayName"])
                    if autor == None:
                        autor = Autor(data_obra["artistDisplayName"], data_obra["artistNationality"], data_obra["artistBeginDate"], data_obra["artistEndDate"])
                        self.autores.append(autor)
                    
                    # Crea la nueva obra y la añade al repositorio local
                    obra_nueva = Obra(id_obra, titulo, depto, autor, tipo, anio_creacion, imagen)

                    print(f"ID: {obra_nueva.id} - Titulo: {obra_nueva.titulo}")

                    self.obras.append(obra_nueva)

                time.sleep(0.3) # Pequeña pausa entre obras de un lote para no saturar la API

            index +=20
            if index >= total:
                print("\nYa no hay mas obras")
                break

            time.sleep(3) # Pausa mas larga entre bloques

            # Pregunta al usuario si desea ver detalles de una obra específica
            mostrar_detalle = input("\nDesea mostrar detalles de una obra:\n1. Si\n2. No\nIngrese la opcion deseada ")
            while (not mostrar_detalle.isnumeric()) or (not int(mostrar_detalle) in range(1,3)):
                print("\nError! Debes ingresar 1 si quieres ver mas detalles o 2 si no quieres")
                mostrar_detalle = input("Desea mostrar detalles de una obra:\n1. Si\n2. No\nIngrese la opcion deseada ")


            if mostrar_detalle == "1":
                 # Obtiene el ID de la obra cuyo detalle se quiere ver
                ver_detalle = input("\nIngrese el ID de la obra de la cual quiere ver detalles: ")

                while (not ver_detalle.isnumeric()) or (not int(ver_detalle) > 0) or (self.buscar_obra(int(ver_detalle)) == None):
                    print("Error! Debes ingresar el numero que corresponda al ID de una obra y debe ser mayor que cero")
                    ver_detalle = input("\nIngrese el ID de la obra de la cual quiere ver detalles: ")
                
                obra_select = self.buscar_obra(int(ver_detalle))
                print(f"\n{obra_select.mostrar()}\n") # Llama al metodo mostra() de la obra selccionada
                
            # Pregunta al usuario si desea continuar mostrando más obras      
            seguir=input("\nDeseas Mostrar 20 obras mas? [S/N]: ").lower()
            while seguir not in ["s", "n"]:
                print("Error! Ingresa S si deseas seguir viendo obras o N si deseas no ver mas obras")
                seguir=input("\nDeseas Mostrar 20 obras mas? [S/N]: ").lower()

            if seguir != "s":
                print("\nConsulta terminada.")
                break

    def buscar_obra(self, id):
        if len(self.obras) != 0:
          for obra in self.obras:
               if obra.id == id:
                    return obra
        return None
        
    def buscar_autor(self, nombre):
        if len(self.autores) != 0:
            for autor in self.autores:
                if autor.nombre == nombre:
                    return autor
        return None
    

    def iniciar(self):
        """
        Inicializar la aplicacion cargando la info en el sistema y presentando al usuario un menu.
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


