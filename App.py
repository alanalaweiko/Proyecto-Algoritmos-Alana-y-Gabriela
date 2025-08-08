import requests 
import json
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
        

    def cargar_obras(self):
        """
        Carga una cantidad específica de obras en el sistema
        """

        response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q=true") # Se le pide a la API que busque obras con imágenes y las que están en el dominio público
        response.raise_for_status() # No rompe código si llega a ver un error

        data = response.json() # Convierte la respuesta de la API a formato JSON.

        
        id_obras = data.get("objectIDs", []) # Obtiene la lista de ID de las obras

        
        if not id_obras: # Si la lista de ID está vacía, muestra...
            print("No se encontraron obras con imágenes disponibles en la API...")
            return

    
        ids_obras_limitadas = id_obras[:100] #Limite de obras cargadas

        
        for i in ids_obras_limitadas: #Itera cada ID de esas obras

            
            if not self.buscar_obra(i): #Entra en función buscar_obra para ver si existe

                
                url_obra = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}" # Construye la URL para obtener los detalles de la obra individualmente

                try:
                    
                    response_obra = requests.get(url_obra)
                    response_obra.raise_for_status() # No rompe código si llega a ver un error

                    data_obra = response_obra.json() # Convierte la respuesta a JSON.

                    depto_nombre = data_obra.get("department", "Desconocido") # Busca el nombre, si no existe por defecto es Desconocido
                    depto_id = data_obra.get("departmentId", -1) # Busca el ID

                    # Busca el departamento en la lista local; si no existe, lo crea y lo añade.
                    depto = self.buscar_depto(depto_nombre)
                    if not depto:
                        depto = Departamento(depto_id, depto_nombre)
                        self.deptos.append(depto)

                    autor_nombre = data_obra.get("artistDisplayName", "Desconocido") # Busca el nombre, si no existe por defecto es Desconocido
                    autor = self.buscar_autor(autor_nombre) # Entra en la función buscar_autor y autor_nombre por parámetro

            
                    if not autor:
                        autor = Autor(
                            autor_nombre,
                            data_obra.get("artistNationality", "Desconocida"),
                            data_obra.get("artistBeginDate", "Desconocida"),
                            data_obra.get("artistEndDate", "Desconocida")
                        )
                        self.autores.append(autor) #Para agregar autores en la lista self.autores

                    
                    obra_nueva = Obra(
                        data_obra["objectID"],
                        data_obra.get("title", "Sin título"),
                        depto,
                        autor,
                        data_obra.get("classification", "Sin clasificación"),
                        data_obra.get("objectDate", "Sin fecha"),
                        data_obra.get("primaryImage", "No disponible")
                    ) # Crea un nuevo objeto Obra con todos los datos

                    
                    self.obras.append(obra_nueva) # Añade la nueva obra a la lista de obras del sistema

                    #time.sleep(0.1) 

                except (requests.exceptions.RequestException, json.decoder.JSONDecodeError): #Si llega a haber un error no explota el programa, solo continua
                    pass


    def cargar_nacionalidades(self):
        """
        Carga las nacionalidades de los autores de las obras
        """
        
        nacionalidades_unicas = set() #Set() para guardar datos sin que se dupliquen cada vez

        for i in self.obras: #Itera cada obra de la lista

            if i.autor and i.autor.nacionalidad: #Si tiene autor y el autor tiene nacionalidad entra acá

                nacionalidades_unicas.add(i.autor.nacionalidad) #Agrega las Nacionalidades al set() sin repetirse

        self.nacionalidades = sorted(list(nacionalidades_unicas)) #Se convierte en una lista y la ordenamos alfabeticamente. Asignamos esa lista a self.nacionalidades

    def cargar(self):
        """
        Cargar TODA la informacion de sistema
        """
        print("\nCargando información... Calma, puede durar aprox 1 minuto :)")
        self.cargar_deptos()
        self.cargar_obras()
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

    
    def listar_obras_nacionalidades(self):
        """
        Muestra la lista de nacionalidades y permite seleccionar una para listar las obras.
        """

        if not self.nacionalidades: # Verifica si la lista de nacionalidades está vacía y de estarlo manda un mensaje
            print("\nNo hay nacionalidades cargadas. Por favor, cargue obras primero.")
            return
    
        print("\n======================================")
        print("     SELECCIONE LA NACIONALIDAD")
        print("======================================")
    
        count = 1 #Contador que inicia en 1
        
        for i in self.nacionalidades: # Itera sobre la lista de nacionalidades
            
            print(f"{count}. {i}") # Imprime cada nacionalidad con su respectivo número
            count += 1 #Va sumando 1 al contador inicial
        
        print(f"{count}. Salir") # Imprime una opción adicional que muestra el último valor de count y salir
    
        # Solicita al usuario que ingrese una opción.
        option = input("\nIngrese la opción deseada: ")
        
        while (not option.isnumeric()) or (not int(option) in range(1, count + 1)): # Verifica que la entrada sea un número y que esté en el rango de opciones válidas
            print("\nError! Opción inválida.")
            option = input("Ingrese la opción deseada: ") #Crea un bucl hasta que esta respuesta sea correcta
    
        if int(option) == count: # Si la respuesta es igual al número de la opción Salir, sale de la función
            return  
    

        nacionalidad_seleccionada = self.nacionalidades[int(option) - 1] #Selecciona nacionalidad en la lista. Se coloca -1 porque los índices inician en cero
        
    
        print(f"\nObras de autores con nacionalidad: {nacionalidad_seleccionada}\n") #Titulo
     
        obras_encontradas = []
        for i in self.obras:
            if i.autor.nacionalidad == nacionalidad_seleccionada: #Si la nacionalidad escogida es igual a la del autor de la obra
                obras_encontradas.append(i) #Se agrega la obra a la lista
        
        if not obras_encontradas: #Si la lista está vacía muestra lo siguiente...
            print(f"No se encontraron obras para la nacionalidad: {nacionalidad_seleccionada}.")
            return
    
        for i in obras_encontradas:  # Itera las obras encontradas y muestra la información seleccionada
            print(f"ID: {i.id} - Título: {i.titulo}")
    
        
        while True: #Especie de submenú
            
            opcion_submenu = input("\nOpciones:\n1. Ver detalles de una obra.\n2. Volver al menú principal.\nIngrese una opción: ")
            
            if opcion_submenu == "1":

                ver_detalle = int(input("Ingrese el ID de la obra: ")) #Si el usuario decide ver más detalles entra acá

                try:
        
                    obra_seleccionada = self.buscar_obra(ver_detalle) #Busca la obra

                    if obra_seleccionada:
                        print(f"\n{obra_seleccionada.mostrar()}\n") # Si la encuentra, muestra sus detalles de la forma que está en clase Obra
                    else:
                        print("Error: ID de obra no encontrado.")

                except ValueError: # Acá se controla los errores, Si la entrada no es un número imprime lo siguiente...
                    
                    print("Error: El ID debe ser un número.")

            elif opcion_submenu == "2":
                break #Sale del bucle

            else:
                print("Opción inválida.")

    def listar_obras_autor(self):
        """
        Permite al usuario buscar obras por el nombre del autor.
        """

        if not self.autores: # Verifica si la lista de autores (self.autores) está vacía
            print("No hay autores cargados. Por favor, cargue obras primero.")
            return

        nombre_autor = input("Ingrese el nombre completo o parcial del autor: ").lower() # Solicita al usuario que ingrese el nombre del autor y convierte la entrada a minúsculas

        obras_encontradas = [] # Crea una lista vacía para guardar las obras

        for i in self.obras: # Itera sobre cada obra en la lista de obras cargadas
            if nombre_autor in i.autor.nombre.lower(): #Comprueba si el nombre ingresado por el usuario está en la obra iterada
                obras_encontradas.append(i) # Si hay coincidencia, la obra se añade a la lista de obras encontradas

        if not obras_encontradas: # Después de recorrer todas las obras, si obras_encontradas está vacía imprime...
            print(f"No se encontraron obras para el autor: {nombre_autor}")
            return

        print(f"\nObras del autor: {nombre_autor}") #Titulo

        for i in obras_encontradas: # Itera sobre la lista de obras encontradas y muestra la información seleccionada
            print(f"ID: {i.id} - Título: {i.titulo} - Autor: {i.autor.nombre}")

        print("\nDesea mostrar detalles de una obra:\n1. Si\n2. No")
        mostrar_detalle = input("\nIngrese la opcion deseada: ")

        if mostrar_detalle == "1":

            id_para_mostrar = int(input("\nIngrese el ID de la obra de la cual quiere ver detalles: ")) # Solicita el ID de la obra para ver los detalles

            obra_seleccionada = self.buscar_obra(int(id_para_mostrar)) #Entra en la función buscar_obra

            if obra_seleccionada:
                print(f"\n{obra_seleccionada.mostrar()}\n") # Si la obra existe, llama a su método mostrar() en la clase Obra para imprimir todos los detalles
            else:
                print("ID de obra no encontrado.")


    def buscar_obra(self, id): #Recibe parámetro id
        if len(self.obras) != 0:
          for obra in self.obras:
               if obra.id == id:
                    return obra
        return None
        
    def buscar_autor(self, nombre): #Recibe parámetro nombre
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

        while True: #While True para que se ejecute el menu hasta que el usuario desee salir del sistema
            
            print("\n===============================")
            print("     BIENVENIDOS A MetroArt")
            print("===============================")

            print("1. Ver lista de obras por Departamento.\n2. Ver lista de obras por Nacionalidad del Autor.\n3. Ver lista de obras por nombre del autor.\n4. Salir")

            option = input("\nIngrese la opcion correspondiente a la accion que desea realizar: ")

            while (not option.isnumeric()) or (not int(option) in range(1,5)): #validar que la opcion sea un numero (isnumeric) y la opcion se encuentre en el rango del 1 al 5 sin incluir el 5.
                print("Error! Opcion invalida")
                option = input("\nIngrese la opcion correspondiente a la accion que desee realizar: ")

            if option == "1":
                self.listar_obras_deptos() #Entra en función listar obras por departamento
            elif option == "2":
                self.listar_obras_nacionalidades() #Entra en función listar obras por nacionalidad
            elif option == "3":
                self.listar_obras_autor() #Entra en función listar obras por nombre del autor
            else:
                print("\n---------- Fin de la Aplicación. Hasta Luego ----------\n")
                break #Salir del Bucle


