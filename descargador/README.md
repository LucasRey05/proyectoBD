# Descargador de videos

Pegás un link de X/Twitter, Instagram Reels o TikTok y te devuelve el video en MP4 (elegís la calidad) o solo el audio en MP3.

## Requisitos

- Python 3.10 o superior
- [ffmpeg](https://ffmpeg.org/download.html) instalado y disponible en el PATH. yt-dlp lo usa para unir audio y video y para convertir a MP3.

## Cómo correrlo

```bash
cd descargador
python -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abrí http://127.0.0.1:5000 en el navegador.

Para cambiar host o puerto: `HOST=0.0.0.0 PORT=8080 python app.py`.

## Desplegar en Firebase

La página va a Firebase Hosting (carpeta `public/`) y el backend a Cloud Run, un contenedor con Python y ffmpeg. Hosting reenvía `/api/**` al backend, así que la página y la API quedan bajo el mismo dominio. No usamos Cloud Functions porque su runtime no trae ffmpeg, y yt-dlp lo necesita.

Requisitos, una sola vez:

1. Crear un proyecto en la [consola de Firebase](https://console.firebase.google.com) y pasarlo al plan Blaze (pago por uso). Cloud Run y Cloud Build lo exigen. Tiene cuota gratuita, pero pide tarjeta.
2. Instalar las herramientas: `npm install -g firebase-tools` y el [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
3. Iniciar sesión: `gcloud auth login` y `firebase login`.

Desplegar:

```bash
cd descargador
PROYECTO=tu-proyecto-firebase ./deploy.sh
```

El script ejecuta `gcloud run deploy` (backend con 2 GiB de memoria, timeout de 300 s y hasta 3 instancias) y después `firebase deploy --only hosting`.

Notas:

- La región por defecto es `southamerica-east1`. Si la cambiás con `REGION=...`, cambiá también `region` en `firebase.json`.
- Cloud Run guarda `/tmp` en memoria, por eso el límite de memoria. Un video grande ocupa bastante.
- Instagram y TikTok pueden bloquear IPs de datacenter, como las de Google Cloud. Si un link funciona en tu PC pero no en la nube, esa es la causa más probable.
- `firebase emulators:start --only hosting` sirve la página para probarla, pero la ruta `/api` solo funciona desplegada.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas no necesitan internet: generan videos de muestra con ffmpeg y los sirven desde un servidor local. Si ffmpeg no está instalado, las pruebas de descarga se saltean.

## Notas

- Solo acepta links de `x.com`, `twitter.com`, `instagram.com` y `tiktok.com`. Cualquier otro dominio se rechaza antes de hacer ninguna petición.
- Las plataformas cambian seguido y yt-dlp se queda atrás. Si algo deja de funcionar, actualizalo con `pip install -U yt-dlp`.
- Instagram y X a veces piden sesión para ciertos contenidos. Los videos privados o restringidos no se pueden bajar.
- Los archivos se guardan en carpetas temporales y se borran cuando termina la descarga.
- Para uso fuera de tu computadora, corré la app con un servidor WSGI con hilos (por ejemplo `gunicorn --threads 4 app:app`) en vez de `python app.py`.
- Usala solo con contenido propio o con permiso. Respetá los derechos de autor y los términos de cada plataforma.

## Estructura

- `app.py`: rutas Flask (`/`, `/api/info`, `/api/descargar`).
- `descargas.py`: validación de links, lectura de calidades y descarga con yt-dlp.
- `public/index.html`: la página (HTML, CSS y JS sin dependencias). La sirve Firebase Hosting, y Flask cuando corre en local.
- `tests/test_descargas.py`: pruebas.
- `Dockerfile`: imagen del backend para Cloud Run (Python, ffmpeg y gunicorn).
- `firebase.json`: Hosting sirve `public/` y reenvía `/api/**` a Cloud Run.
- `deploy.sh`: despliega el backend y la página.
