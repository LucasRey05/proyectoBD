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

## Desplegar gratis

Todo el despliegue usa planes gratuitos y no pide tarjeta:

- **Página:** Firebase Hosting, plan Spark. Sirve la carpeta `public/`.
- **Backend:** Render, plan Free, usando el `Dockerfile` de esta carpeta (ya incluye ffmpeg).

Firebase no puede correr el backend en su plan gratuito, porque Cloud Run y Cloud Functions exigen el plan Blaze. Por eso el backend va en Render y la página de Firebase llama a esa URL.

### 1. Backend en Render

1. Creá una cuenta en [render.com](https://render.com), entrando con GitHub.
2. Elegí **New → Web Service → Build and deploy from a Git repository** y seleccioná `LucasRey05/proyectoBD`.
3. Configurá:
   - **Branch:** `claude/laughing-galileo-q7as2h`
   - **Root Directory:** `descargador`
   - **Runtime:** Docker
   - **Instance Type:** Free
4. En **Environment**, agregá la variable `CORS_ORIGINS` con el valor:
   ```
   https://descargador-video-2026.web.app,https://descargador-video-2026.firebaseapp.com
   ```
5. Creá el servicio. Cuando termine, Render muestra la URL del servicio, que termina en `.onrender.com`. Puede llevar un sufijo si el nombre ya está en uso. Ponela en la meta del paso 2.

### 2. Apuntar la página al backend

En `public/index.html`, poné esa URL en la meta `api-base`:

```html
<meta name="api-base" content="https://descargador-api-p6fk.onrender.com">
```

Hacelo antes del paso 3, y subí el cambio a la rama (`git add`, `git commit`, `git push`).

### 3. Página en Firebase Hosting

Desde la carpeta `descargador`:

```powershell
firebase deploy --only hosting --project descargador-video-2026
```

El link queda en **https://descargador-video-2026.web.app**.

### Notas

- El plan Free de Render se apaga después de unos 15 minutos sin uso. La primera descarga después de eso tarda más, aproximadamente 30 a 60 segundos.
- Render Free tiene 512 MB de RAM. Alcanza para reels y TikToks cortos. Videos largos o en alta calidad pueden fallar.
- No verifiqué el tiempo máximo de conexión de Render. Si los videos largos se cortan, ese es el primer punto a revisar.
- Instagram y TikTok pueden bloquear IPs de servidores en la nube. Si un link funciona en tu PC y en Render no, esa es la causa más probable.
- Si cambiás el dominio de la página, actualizá `CORS_ORIGINS` en Render.
- Cloud Run (Google) también puede correr este backend sin costo dentro de su cuota gratuita, pero exige el plan Blaze con tarjeta. El `Dockerfile` sirve para ambos.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas no necesitan internet: generan videos de muestra con ffmpeg y los sirven desde un servidor local. Si ffmpeg no está instalado, las pruebas de descarga se saltean.

## YouTube y cookies

YouTube pide verificación "no soy un bot" a los servidores en la nube. Cuando pasa, la página te dice que hacen falta cookies. Para configurarlas:

1. En tu navegador, con la sesión iniciada en YouTube, exportá las cookies de `youtube.com` en formato Netscape (`cookies.txt`). Hay extensiones como "Get cookies.txt LOCALLY".
2. En Render, abrí tu servicio → **Environment** → **Secret Files** y creá el archivo `/etc/secrets/cookies.txt` con el contenido exportado.
3. En **Environment**, agregá la variable `YTDLP_COOKIES` con el valor `/etc/secrets/cookies.txt`. Render vuelve a desplegar solo.

Para probarlo en tu PC, en PowerShell: `$env:YTDLP_COOKIES="ruta\al\cookies.txt"` y después `python app.py`.

Las cookies dan acceso a tu cuenta. Usá una cuenta secundaria si podés, no las subas al repo y renovalas cuando YouTube vuelva a fallar.

## Notas

- Solo acepta links de `x.com`, `twitter.com`, `instagram.com`, `tiktok.com`, `youtube.com` y `youtu.be`. Cualquier otro dominio se rechaza antes de hacer ninguna petición.
- YouTube suele pedir verificación "no soy un bot" a los servidores en la nube. Si los links de YouTube fallan desde Render pero andan en tu PC, esa es la causa más probable.
- Las plataformas cambian seguido y yt-dlp se queda atrás. Si algo deja de funcionar, actualizalo con `pip install -U yt-dlp`.
- Instagram y X a veces piden sesión para ciertos contenidos. Los videos privados o restringidos no se pueden bajar.
- Los archivos se guardan en carpetas temporales y se borran cuando termina la descarga.
- Usala solo con contenido propio o con permiso. Respetá los derechos de autor y los términos de cada plataforma.

## Estructura

- `app.py`: rutas Flask (`/`, `/api/info`, `/api/descargar`) y CORS configurable con `CORS_ORIGINS`.
- `descargas.py`: validación de links, lectura de calidades y descarga con yt-dlp.
- `public/index.html`: la página (HTML, CSS y JS sin dependencias). La sirve Firebase Hosting, y Flask en local.
- `tests/test_descargas.py`: pruebas.
- `Dockerfile`: imagen del backend (Python, ffmpeg y gunicorn). La usa Render.
- `firebase.json`: Hosting sirve `public/`.
