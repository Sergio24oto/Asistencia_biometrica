#simulacion al ESP32/lector desde consola
import requests

#Después cuando usemos el ESP32, va a pasar lo mismo, pero en vez de 127.0.0.1, vamos a usar la IP de nuestra compu.
URL_FLASK = "http://127.0.0.1:5000/api/registrar_huella"


def enviar_huella(id_huella):
    datos = {
        "id_huella": id_huella
    }

    try:
        respuesta = requests.post(URL_FLASK, json=datos)
        resultado = respuesta.json()

        print("--------------------------------")
        print("Respuesta del servidor Flask:")
        print("OK:", resultado.get("ok"))
        print("Mensaje:", resultado.get("mensaje"))

        if resultado.get("alumno"):
            print("Alumno:", resultado.get("alumno"))

        if resultado.get("hora"):
            print("Hora:", resultado.get("hora"))

        print("--------------------------------")

    except requests.exceptions.ConnectionError:
        print("Error: no se pudo conectar con Flask.")
        print("Revisá que app.py esté ejecutándose.")

    except Exception as error:
        print("Ocurrió un error:")
        print(error)


def iniciar_simulador():
    print("Simulador de lector de huellas")
    print("Escribí un ID de huella y presioná Enter.")
    print("Ejemplo: 1")
    print("Para salir, escribí: salir")

    while True:
        valor = input("ID huella: ")

        if valor.lower() == "salir":
            print("Simulador finalizado.")
            break

        if not valor.isdigit():
            print("Tenés que ingresar un número.")
            continue

        id_huella = int(valor)
        enviar_huella(id_huella)


if __name__ == "__main__":
    iniciar_simulador()