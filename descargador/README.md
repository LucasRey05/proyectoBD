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
- `templates/index.html`: la página (HTML, CSS y JS sin dependencias).
- `tests/test_descargas.py`: pruebas.
