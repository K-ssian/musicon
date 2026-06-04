import yt_dlp
import os
import sys

ruta = os.path.expanduser("~/MiMusica")

def buscador(peticion):
    if peticion.startswith(("http://", "https://")):
        return peticion

    opciones = {
            'extract_flat': True,
            'skip_download': True,
            'quiet': True,
            'js_runtimes': {'quickjs': {}},
            }

    len_resultados = 5
    query = f"ytsearch{len_resultados}:{peticion}"

    print(f"Opciones para '{peticion}'...")

    with yt_dlp.YoutubeDL(opciones) as ydl:
        try:
            resultado = ydl.extract_info(query, download=False)

            if 'entries' not in resultado or not resultado['entries']:
                print(f"No se hallaron resultados para {peticion}")
                return None

            # Caso contrario, se hallaron resultados
            entries = resultado['entries']
            
            # Seleccion
            print("\n--- Seleccion de Musica ---")
            for i, entry in enumerate(entries, start=1):
                titulo=entry.get('title', 'Titulo desconocido')
                canal=entry.get('uploader', 'Canal desconocido')
                
                duracion_msj = ""
                if entry.get('duratiob'):
                    mins, segs = divmod(int(entry['duration']), 60)
                    duracion_msj = f"({mins}:{secs:02d})"

                print(f" [{i}] {titulo} - [{canal}] {duracion_msj}")

            print(" [0] Ninguna.")

            # Validacion
            while True:
                try:
                    eleccion = int(input(": "))
                    if eleccion == 0:
                        print("Busqueda cancelada.")
                        return None
                    
                    if 1 <= eleccion <= len(entries):
                        # descargar
                        video_elegido = entries[eleccion - 1]
                        return video_elegido.get('url') or video_elegido.get('webpage_url')
                    else:
                        print(f"Número fuera de rnago, escoge entre 1 y {len(entries)}")

                except ValueError:
                    print("Entrada no valida.")

        except Exception as e:
            print("Error durante la busqueda:")
            print(e)
            return None


def descargar_audio(url):
    if not url:
        return

    opciones = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(ruta, '%(title)s.%(ext)s'), # Guardar en carpeta
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
                }],
            'noplaylist': True,
            'quiet': False,
            'js_runtimes': {'quickjs': {}},
            }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            print("Conectando con el servidor...")
            ydl.download([url])
            print("Descarga completada.")
    except Exception as e:
        print("Se ha presentado el siguiente error:")
        print(e)

if __name__ == "__main__":
    os.makedirs(ruta, exist_ok=True)

    if len(sys.argv) > 1:
        entrada = " ".join(sys.argv[1:])
    
    else:
        print("--- Descargas de 'Musicon' ---")
        entrada = input("Busqueda: ").strip()

    if entrada:
        enlace = buscador(entrada)
        descargar_audio(enlace)
    else:
        print("¡No haz introducido nada!")
