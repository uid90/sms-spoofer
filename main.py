import os
import sys
import csv
import configparser
import vonage
from time import sleep


def limpiar():
    if (sys.platform == "win32"):
        os.system("cls")
    else:
        os.system("clear")


def imprimir_opciones(*args):
    for i, nombre in enumerate(args):
        print(f"[{i + 1}]", nombre)


def verificar_version_python():
    if sys.version_info < (3, 10):
        print("ERROR: ¡Versión de Python inapropiada!\nPara el funcionamiento correcto del programa, debes instalar Python 3.10 o superior.")
        return False
    
    return True


def principal():
    global config

    config = configparser.ConfigParser()
    
    if not os.path.exists("contacts.csv"):
        with open("contacts.csv", "w", newline="") as archivo_contactos:
            escritor = csv.DictWriter(archivo_contactos, fieldnames=("nombre", "numero_telefono"))
            escritor.writeheader()

    if not os.path.exists("config.ini"):
        api_key = input("Ingresa tu clave de API de Vonage: ")
        api_secret = input("Ingresa tu secreto de API de Vonage: ")

        config.add_section("credenciales_api")

        config.set("credenciales_api", "api_key", api_key)
        config.set("credenciales_api", "api_secret", api_secret)

        with open("config.ini", "w") as archivo_config:
            config.write(archivo_config)

    config.read("config.ini")

    while True:
        sleep(1)
        menu()


def menu():
    limpiar()

    print("Bienvenido al Spoofer de SMS")
    print("Spoofer de SMS creado con fines educativos")
    print("\nby uid90\n")

    imprimir_opciones("Número de teléfono", "Envío masivo", "Contactos", "Cambiar credenciales de API", "Salir")
    tarea_seleccionada = input("Ingresa el número de la tarea: ")
    match tarea_seleccionada:
        case "1":
            marcar_numero()
        case "2":
            numeros_masivos()
        case "3":
            abrir_contactos()
        case "4":
            cambiar_credenciales_api()
        case "5":
            exit()
        case _:
            print("ERROR: Opción inválida, intenta de nuevo")
        

def enviar_sms(numero, remitente, texto):
    cliente = vonage.Client(
        key=config["credenciales_api"]["api_key"],
        secret=config["credenciales_api"]["api_secret"]
    )

    sms = vonage.Sms(cliente)
    datos_respuesta = sms.send_message({
        "from": remitente,
        "to": numero,
        "text": texto,
        "type": "unicode"
    })

    if datos_respuesta["messages"][0]["status"] == "0":
        print("\nMensaje enviado con éxito.")
    else:
        print(f"\nEl mensaje falló con el error: {datos_respuesta['messages'][0]['error-text']}")


def marcar_numero():
    numero = input("\nNúmero de la víctima: ").replace("+", "").replace(" ", "")
    remitente = input("Nombre del remitente: ")
    texto = input("Texto del SMS: ")

    enviar_sms(numero, remitente, texto)


def numeros_masivos():
    limpiar()

    imprimir_opciones("Todos los contactos", "Manual", "Volver")
    tipo_masivo = input("Ingresa el número de la tarea: ")

    numeros = []
    match tipo_masivo:
        case "1":
            with open("contacts.csv", "r") as archivo_contactos:
                lector = csv.DictReader(archivo_contactos)
                for fila in list(lector):
                    numeros.append(fila["numero_telefono"])
        case "2":
            cantidad = int(input("\n¿Cuántos números deseas enviar en masa?: "))
            for i in range(cantidad):
                numero = input(f"Número de víctima #{i + 1}: ").replace("+", "").replace(" ", "")
                numeros.append(numero)
        case "3":
            return
        case _:
            print("ERROR: Opción inválida")
            return

    remitente = input("Nombre del remitente: ")
    texto = input("Texto del SMS: ")

    for numero in numeros:
        enviar_sms(numero, remitente, texto)


def abrir_contactos():
    limpiar()

    with open("contacts.csv", "r") as archivo_contactos:
        lector = csv.DictReader(archivo_contactos)
        for i, fila in enumerate(lector):
            print(f"[{i + 1}]", fila["nombre"])

    print("\n[*] Crear un nuevo contacto")
    print("[X] Volver")

    tarea = input("\nIngresa el número de la tarea: ")
    match tarea:
        case "*":
            nuevo_contacto()
        case "x" | "X":
            menu()
        case _:
            try:
                num_seleccionado = int(tarea) - 1
                with open("contacts.csv", "r") as archivo_contactos:
                    lector = csv.DictReader(archivo_contactos)
                    filas = list(lector)

                numero = filas[num_seleccionado]["numero_telefono"]
                remitente = input("Nombre del remitente: ")
                texto = input("Texto del SMS: ")
                
                enviar_sms(numero, remitente, texto)
            except (ValueError, IndexError):
                print("ERROR: Opción inválida, intenta de nuevo")
                sleep(1)
                abrir_contactos()


def nuevo_contacto():
    nombre_contacto = input("\nNombre del contacto: ")
    numero_contacto = input("Número del contacto: ").replace("+", "").replace(" ", "")
        
    with open("contacts.csv", "a", newline="") as archivo_contactos:
        escritor = csv.DictWriter(archivo_contactos, fieldnames=("nombre", "numero_telefono"))
        escritor.writerow({"nombre": nombre_contacto, "numero_telefono": numero_contacto})


def cambiar_credenciales_api():
    seguro = input("¿Estás seguro de que quieres cambiar las credenciales de la API? (S/N): ")
    if (seguro.lower() == "s"):
        api_key = input("\nIngresa tu nueva clave de API de Vonage: ")
        api_secret = input("Ingresa tu nuevo secreto de API de Vonage: ")

        config.set("credenciales_api", "api_key", api_key)
        config.set("credenciales_api", "api_secret", api_secret)

        with open("config.ini", "w") as archivo_config:
            config.write(archivo_config)
        
        config.read("config.ini")


if __name__ == "__main__":
    if verificar_version_python():
        principal()


