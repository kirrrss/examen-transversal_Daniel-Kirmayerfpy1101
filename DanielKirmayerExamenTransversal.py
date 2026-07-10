def validar_codigo(codigo, planes):
    
    if not codigo.strip():
        return False

    if codigo.upper() in [k.upper() for k in planes.keys()]:
        return False
    return True

def validar_nombre(nombre):

    return bool(nombre.strip())

def validar_tipo(tipo):
  
    return tipo.lower() in ['mensual', 'trimestral', 'anual']

def validar_duracion(duracion):
  
    try:
        val = int(duracion)
        return val > 0
    except ValueError:
        return False

def validar_acceso_piscina(opcion):

    return opcion.lower() in ['s', 'n']

def validar_incluye_clases(opcion):

    return opcion.lower() in ['s', 'n']

def validar_horario(horario):

    return bool(horario.strip())

def validar_precio(precio):

    try:
        val = int(precio)
        return val > 0
    except ValueError:
        return False

def validar_cupos(cupos):

    try:
        val = int(cupos)
        return val >= 0
    except ValueError:
        return False


def leer_opcion():
    """Solicita, valida y retorna una opción entera del menú principal."""
    while True:
        try:
            opcion_str = input("Ingrese opción: ")
            opcion = int(opcion_str)
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")


def cupos_tipo(tipo, planes, inscripciones):
    """Opción 1: Muestra el total de cupos para un tipo de plan específico."""
    total_cupos = 0
    tipo_buscado = tipo.lower()
    
 
    for codigo, datos in planes.items():
        if datos[1].lower() == tipo_buscado:
            if codigo in inscripciones:
                total_cupos += inscripciones[codigo][1]
                
    print(f"El total de cupos disponibles es: {total_cupos}")


def busqueda_precio(p_min, p_max, planes, inscripciones):
    """Opción 2: Busca planes por rango de precio y muestra ordenados alfabéticamente."""
    resultados = []
    
    for codigo, datos_ins in inscripciones.items():
        precio = datos_ins[0]
        cupos = datos_ins[1]
        
        if p_min <= precio <= p_max and cupos > 0:
            if codigo in planes:
                nombre_plan = planes[codigo][0]
                resultados.append(f"{nombre_plan}--{codigo}")
                
    if resultados:
    
        resultados.sort()
        print(f"Los planes encontrados son: {resultados}")
    else:
        print("No hay planes en ese rango de precios.")


def buscar_codigo(codigo, inscripciones):
    """Auxiliar: Retorna True si el código existe en el diccionario (insensible a mayúsculas)."""
    codigo_buscado = codigo.upper()
    for k in inscripciones.keys():
        if k.upper() == codigo_buscado:
            return True
    return False


def obtener_clave_real(codigo, diccionario):
    """Auxiliar: Retorna la clave exacta original guardada en el diccionario."""
    for k in diccionario.keys():
        if k.upper() == codigo.upper():
            return k
    return codigo


def actualizar_precio(codigo, nuevo_precio, inscripciones):
    """Opción 3: Actualiza el precio de un plan si el código existe."""
    if buscar_codigo(codigo, inscripciones):
        clave_real = obtener_clave_real(codigo, inscripciones)
        inscripciones[clave_real][0] = nuevo_precio
        return True
    return False


def agregar_plan(codigo, nombre, tipo, duracion, acceso_piscina, incluye_clases, horario, precio, cupos, planes, inscripciones):
    """Opción 4: Agrega un plan si no existe previamente el código."""
    if buscar_codigo(codigo, inscripciones):
        return False
        

    piscina_bool = True if acceso_piscina.lower() == 's' else False
    clases_bool = True if incluye_clases.lower() == 's' else False
    

    planes[codigo] = [nombre, tipo.lower(), int(duracion), piscina_bool, clases_bool, horario]
   
    inscripciones[codigo] = [int(precio), int(cupos)]
    return True


def eliminar_plan(codigo, planes, inscripciones):
    """Opción 5: Elimina el plan de ambos diccionarios."""
    if buscar_codigo(codigo, inscripciones):
        clave_real_ins = obtener_clave_real(codigo, inscripciones)
        clave_real_pla = obtener_clave_real(codigo, planes)
        
        del inscripciones[clave_real_ins]
        del planes[clave_real_pla]
        return True
    return False


def main():

    planes = {
        'F001': ['Plan Básico', 'mensual', 1, False, False, 'libre'],
        'F002': ['Plan Full', 'mensual', 1, True, True, 'libre'],
        'F003': ['Plan Estudiante', 'trimestral', 3, False, True, 'tarde'],
        'F004': ['Plan Senior', 'trimestral', 3, True, False, 'mañana'],
        'F005': ['Plan Anual Pro', 'anual', 12, True, True, 'libre'],
        'F006': ['Plan Nocturno', 'mensual', 1, False, True, 'noche']
    }

    inscripciones = {
        'F001': [14990, 30],
        'F002': [22990, 10],
        'F003': [39990, 0],
        'F004': [35990, 6],
        'F005': [159990, 2],
        'F006': [18990, 15]
    }

    while True:
print("\n========== MENÚ PRINCIPAL ==========")
print("1. Cupos por tipo de plan")
print("2. Búsqueda de planes por rango de precio")
print("3. Actualizar precio de plan")
print("4. Agregar plan")
print("5. Eliminar plan")
print("6. Salir")
print("====================================")
 


        opcion = leer_opcion()

        if opcion == 1:
            tipo = input("Ingrese tipo de plan a consultar: ")
            cupos_tipo(tipo, planes, inscripciones)

        elif opcion == 2:
            while True:
                try:
                    p_min_str = input("Ingrese precio mínimo: ")
                    p_min = int(p_min_str)
                    p_max_str = input("Ingrese precio máximo: ")
                    p_max = int(p_max_str)
                    
                    if p_min >= 0 and p_max >= 0 and p_min <= p_max:
                        busqueda_precio(p_min, p_max, planes, inscripciones)
                        break
                    else:
                        print("Debe ingresar valores válidos (mayores a cero y p_min <= p_max)")
                except ValueError:
                    print("Debe ingresar valores enteros")

        elif opcion == 3:
            while True:
                codigo = input("Ingrese código del plan: ")
                try:
                    nuevo_precio_str = input("Ingrese nuevo precio: ")
                    nuevo_precio = int(nuevo_precio_str)
                    if nuevo_precio <= 0:
                        print("El precio debe ser un valor entero positivo")
                        continue
                        
                    if actualizar_precio(codigo, nuevo_precio, inscripciones):
                        print("Precio actualizado")
                    else:
                        print("El código no existe")
                except ValueError:
                    print("Debe ingresar un precio entero válido")
                
                resp = input("¿Desea actualizar otro precio (s/n)?: ")
                if resp.lower() == 'n':
                    break

        elif opcion == 4:
            codigo = input("Ingrese código del plan: ")
            nombre = input("Ingrese nombre del plan: ")
            tipo = input("Ingrese tipo (mensual/trimestral/anual): ")
            duracion = input("Ingrese duración (meses): ")
            acceso_piscina = input("¿Incluye acceso a piscina? (s/n): ")
            incluye_clases = input("¿Incluye clases grupales? (s/n): ")
            horario = input("Ingrese horario: ")
            precio = input("Ingrese precio: ")
            cupos = input("Ingrese cupos: ")

            todo_valido = True

            if not validar_codigo(codigo, planes):
                print("Código inválido o ya existente.")
                todo_valido = False
            elif not validar_nombre(nombre):
                print("Nombre inválido.")
                todo_valido = False
            elif not validar_tipo(tipo):
                print("Tipo inválido.")
                todo_valido = False
            elif not validar_duracion(duracion):
                print("Duración inválida.")
                todo_valido = False
            elif not validar_acceso_piscina(acceso_piscina):
                print("Opción de piscina inválida.")
                todo_valido = False
            elif not validar_incluye_clases(incluye_clases):
                print("Opción de clases inválida.")
                todo_valido = False
            elif not validar_horario(horario):
                print("Horario inválido.")
                todo_valido = False
            elif not validar_precio(precio):
                print("Precio inválido.")
                todo_valido = False
            elif not validar_cupos(cupos):
                print("Cupos inválidos.")
                todo_valido = False

            if todo_valido:
                exito = agregar_plan(codigo, nombre, tipo, duracion, acceso_piscina, incluye_clases, horario, precio, cupos, planes, inscripciones)
                if exito:
                    print("Plan agregado")
                else:
                    print("El código ya existe")

        elif opcion == 5:
            codigo = input("Ingrese código del plan que desea eliminar: ")
            if eliminar_plan(codigo, planes, inscripciones):
                print("Plan eliminado")
            else:
                print("El código no existe")

        elif opcion == 6:
            print("Programa finalizado,¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
