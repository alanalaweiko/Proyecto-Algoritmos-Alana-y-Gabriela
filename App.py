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
        #Respuesta que se recibira de la API
        response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")

        #Validar el status de la respuesta. Si es 200 es correcto si no avisar que hubo un error 
        if response.status_code == 200:
            #Transformo la respuesta de la API en json
            data = response.json()

            #Obtengo la lista de IDs de Obras del json anterior
            lista_obrasIDs = data["objectIDs"]

            pausa = 2
            indice = 1
            faltantes = []

            for index in range(0, 20):
                #A partir de los IDs llamo a API que obtendra la informacion correspondiente a la obra

                #Configuro el link para obtener una obra dado el  id
                link = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{lista_obrasIDs[index]}"


                response2 = requests.get(link)
                if response2.status_code == 200:
                    data = response2.json()

                    #Obtengo los datos referentes al autor
                    nombre = data["artistDisplayName"]
                    autor = None

                    if self.buscar_autor(nombre) != None:
                        autor = self.buscar_autor(nombre)
                    else:
                        nacionalidad = data["artistNationality"]
                        fecha_nac = data["artistBeginDate"]
                        fecha_muerte = data["artistEndDate"]
                        autor = Autor(nombre, nacionalidad, fecha_nac, fecha_muerte)
                        self.autores.append(autor)

                    titulo = data["title"]
                    depto = self.buscar_depto(data["department"])
                    tipo = data["classification"]
                    anio_creacion = data["objectDate"]
                    imagen = data["primaryImage"]


                    obra = Obra(titulo, depto, autor, tipo, anio_creacion, imagen)
                    print("Obra creada")
                    print(obra.titulo)
                    print("\n\n")
                    self.obras.append(obra)
                elif response2.status_code in (403, 429):
                    faltantes.append(id)
                    print(f"\nFalto el {id}\n")

                print(f"\nIntento {indice}\n")
                indice+=1


                for intento in range(5):
                    time.sleep(pausa)

                    #Respuesta recibida por la API
                    response2 = requests.get(link)
                    if response2.status_code == 200:
                        data = response2.json()

                        #Obtengo los datos referentes al autor
                        nombre = data["artistDisplayName"]

                        autor = None

                        if self.buscar_autor(nombre) != None:
                            autor= self.buscar_autor(nombre)
                        else:
                            nacionalidad = data["artistNationality"]
                            fecha_nac = data["artistBeginDate"]
                            fecha_muerte = data["artistEndDate"]  

                            autor = Autor(nombre, nacionalidad, fecha_nac, fecha_muerte)
                            self.autores.append(autor)

                        titulo = data["title"]
                        depto = self.buscar_depto(data["department"])
                        tipo = data["classification"]
                        anio_creacion = data["objectDate"]
                        imagen = data["primaryImage"]


                        obra = Obra(titulo,depto, autor, tipo, anio_creacion,imagen)
                        print("Obra creada")
                        print(obra.titulo)
                        print("\n\n")
                        self.obras.append(obra)
                        break

                    elif response2.status_code in (403, 429):
                        espera = 2 ** intento       #1 s, luego 2 s, luego 4 s...
                        print(f"\n  Bloqueo temporal (intento {intento+1}); "
                           f"esperando {espera} s…")
                        time.sleep(espera)

                    else:
                        print("\nHubo algun error al intentar obtener los datos de la API")
                        break

                indice+=1
                if indice % 500 ==0:
                    print(f"\n{indice:,} obras procesadas...")

        else:
            print("Hubo algun error al intentar obtener los datos de la API")
            

    def buscar_autor(self, nombre):
        if len(self.autores) != 0:
            for autor in self.autores:
                if autor.nombre == nombre:
                    return autor
        else:
            return None
        
    def buscar_depto(self,nombre):
        if len(self.deptos)!= 0:
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
        self.cargar_obras_autores()
        self.cargar_nacionalidades()
        print("... Informacion cargada Exitosamente")


    def listar_obras_deptos(self):
        """
        Mostrar al usuario una lista de los departamentos del museo, para luego seleccionar un departamento y mostrar las obras de ese departamento y seguido de eso que el usuario tenga la opcion de visualizar los detalles de la obra deseada.
        """
        print("\n==============================")
        print("    SELECCIONE UN DEPARTAMENTO")
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

                if len(lista_obras) == 0:
                    print("\nNo hay obras en el depto selccionado.")
                else:
                    print("\n==============================================================")
                    print(f" SELECCIONE LA OBRA DEL DEPARTAMENTO {depto_select.nombre}")
                    print("=============================================================")

                    count = 1
                    for obra in lista_obras:
                        print(f"{count}. {obra.titulo}")
                        count+=1

                    print(f"{count}. Salir")

                    option = input("\nIngrese la opcion deseada:")
                    while (not option.isnumeric) or (not int(option) in range(1, count+1)):
                        print("\nError! Opcion invalida")
                        option = input("Ingrese la opcion deseada: ")

                    if int(option) != count:
                        indice = int(option) - 1
                        obra_select = lista_obras[indice]

                        print("\n======================================")
                        print(f"DETALLE DE LA OBRA {obra_select.titulo}")
                        print("=======================================")
                        
                        print(f"\n{obra_select.mostrar()}")



    def buscar_obras_deptos(self, depto):
        obras = []
        for obra in self.obras:
            if obra.depto.id == depto.id:
                obras.append(obra)

        return obras




    def iniciar(self):
        """
        Inicializar la aplicacion cargando la info en el sistema y presentando al usuario un menu.
        """
        self.cargar() #Cargar informacion

        print(len(self.obras))
        print("\n")

        for autor in self.autores:
            print(autor.mostrar())


        for obra in self.obras:
            print(obra.mostrar())

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


