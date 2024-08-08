import redis
import json

# Configurar la conexión a Redis
client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def agregar_receta():
    id = client.incr('receta_id')  # Incrementa el ID para crear un nuevo ID único
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes (separados por comas): ")
    pasos = input("Ingrese los pasos: ")
    receta = {
        'nombre': nombre,
        'ingredientes': ingredientes,
        'pasos': pasos
    }
    client.set(f'receta:{id}', json.dumps(receta))
    print("Receta agregada exitosamente.")

def actualizar_receta():
    id = input("Ingrese el ID de la receta que desea actualizar: ")
    receta_str = client.get(f'receta:{id}')
    if receta_str:
        receta = json.loads(receta_str)
        nombre = input("Ingrese el nuevo nombre de la receta: ")
        ingredientes = input("Ingrese los nuevos ingredientes (separados por comas): ")
        pasos = input("Ingrese los nuevos pasos: ")
        receta['nombre'] = nombre
        receta['ingredientes'] = ingredientes
        receta['pasos'] = pasos
        client.set(f'receta:{id}', json.dumps(receta))
        print("Receta actualizada exitosamente.")
    else:
        print("Receta no encontrada.")

def eliminar_receta():
    id = input("Ingrese el ID de la receta que desea eliminar: ")
    result = client.delete(f'receta:{id}')
    if result:
        print("Receta eliminada exitosamente.")
    else:
        print("Receta no encontrada.")

def ver_recetas():
    keys = client.keys('receta:*')
    if keys:
        for key in keys:
            receta_str = client.get(key)
            receta = json.loads(receta_str)
            print(f"ID: {key.split(':')[1]}, Nombre: {receta['nombre']}")
    else:
        print("No hay recetas disponibles.")

def buscar_receta():
    id = input("Ingrese el ID de la receta que desea buscar: ")
    receta_str = client.get(f'receta:{id}')
    if receta_str:
        receta = json.loads(receta_str)
        print(f"Nombre: {receta['nombre']}")
        print(f"Ingredientes: {receta['ingredientes']}")
        print(f"Pasos: {receta['pasos']}")
    else:
        print("Receta no encontrada.")

def main():
    while True:
        print("\nOpciones:")
        print("1) Agregar nueva receta")
        print("2) Actualizar receta existente")
        print("3) Eliminar receta existente")
        print("4) Ver listado de recetas")
        print("5) Buscar ingredientes y pasos de receta")
        print("6) Salir")
        
        opcion = input("Seleccione una opción: ").lower()

        if opcion == '1':
            agregar_receta()
        elif opcion == '2':
            actualizar_receta()
        elif opcion == '3':
            eliminar_receta()
        elif opcion == '4':
            ver_recetas()
        elif opcion == '5':
            buscar_receta()
        elif opcion == '6':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()
    client.close()
