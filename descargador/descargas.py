"""Lógica del descargador: valida el link, lee las calidades disponibles y baja
el video (MP4) o solo el audio (MP3) usando yt-dlp."""

import logging
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp
from yt_dlp.utils import YoutubeDLError

log = logging.getLogger("descargador")

# Solo se aceptan links de estas redes. Cualquier otro dominio se rechaza
# antes de hacer ninguna petición.
DOMINIOS_PERMITIDOS = ("twitter.com", "x.com", "instagram.com", "tiktok.com")

MENSAJE_ERROR_GENERICO = (
    "No pude obtener el video de ese link. Puede ser privado, que ya no exista "
    "o que la plataforma lo esté bloqueando."
)


class ErrorDescarga(Exception):
    """Error con un mensaje pensado para mostrarle al usuario."""


def validar_url(url):
    """Devuelve el link limpio o lanza ValueError si no es de una red permitida."""
    if not isinstance(url, str) or not url.strip():
        raise ValueError("Pegá un link.")
    url = url.strip()
    if len(url) > 2048:
        raise ValueError("El link es demasiado largo.")
    partes = urlparse(url)
    if partes.scheme not in ("http", "https") or not partes.hostname:
        raise ValueError("El link tiene que empezar con https://")
    host = partes.hostname.lower()
    if not any(host == d or host.endswith("." + d) for d in DOMINIOS_PERMITIDOS):
        raise ValueError("Solo acepto links de Twitter/X, Instagram o TikTok.")
    return url


def _opciones_base():
    return {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "playlist_items": "1",
        "socket_timeout": 30,
        "retries": 3,
    }


def _alturas_disponibles(formatos):
    alturas = {
        f["height"]
        for f in formatos or []
        if f.get("height") and f.get("vcodec") != "none"
    }
    return sorted(alturas, reverse=True)


def obtener_info(url):
    """Devuelve título, autor, duración, miniatura y alturas disponibles, sin descargar."""
    opciones = {**_opciones_base(), "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
    except YoutubeDLError as e:
        log.warning("No se pudo leer %s: %s", url, e)
        raise ErrorDescarga(MENSAJE_ERROR_GENERICO) from e

    if not info:
        raise ErrorDescarga(MENSAJE_ERROR_GENERICO)
    if "entries" in info:
        primera = next((e for e in info["entries"] if e), None)
        if primera is None:
            raise ErrorDescarga("No encontré ningún video en ese link.")
        info = primera

    return {
        "titulo": info.get("title") or "video",
        "autor": info.get("uploader") or info.get("channel") or "",
        "duracion": info.get("duration"),
        "miniatura": info.get("thumbnail"),
        "alturas": _alturas_disponibles(info.get("formats")),
    }


def _formato_video(altura):
    """Selector de yt-dlp: prefiere MP4 con audio y, si no hay, cae a otros formatos."""
    if altura is None:
        return "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b"
    tope = f"[height<={altura}]"
    return f"bv*{tope}[ext=mp4]+ba[ext=m4a]/b{tope}[ext=mp4]/bv*{tope}+ba/b{tope}/b"


def descargar(url, tipo="video", altura=None):
    """Descarga el video en MP4 o el audio en MP3 y devuelve la ruta del archivo.

    El archivo queda dentro de una carpeta temporal propia: quien llama es
    responsable de borrar ``ruta.parent`` cuando ya no lo necesite.
    """
    if tipo not in ("video", "audio"):
        raise ValueError("tipo tiene que ser 'video' o 'audio'")
    if shutil.which("ffmpeg") is None:
        raise ErrorDescarga("El servidor no tiene ffmpeg instalado.")

    carpeta = Path(tempfile.mkdtemp(prefix="descarga_"))
    opciones = {
        **_opciones_base(),
        "outtmpl": str(carpeta / "%(title).80s [%(id)s].%(ext)s"),
    }
    if tipo == "audio":
        extension = ".mp3"
        opciones["format"] = "ba/b"
        opciones["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        extension = ".mp4"
        opciones["format"] = _formato_video(altura)
        opciones["merge_output_format"] = "mp4"
        opciones["postprocessors"] = [{
            "key": "FFmpegVideoRemuxer",
            "preferedformat": "mp4",
        }]

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
    except YoutubeDLError as e:
        shutil.rmtree(carpeta, ignore_errors=True)
        log.warning("Falló la descarga de %s: %s", url, e)
        raise ErrorDescarga(MENSAJE_ERROR_GENERICO) from e

    archivos = [p for p in carpeta.iterdir() if p.suffix == extension]
    if not archivos:
        shutil.rmtree(carpeta, ignore_errors=True)
        raise ErrorDescarga("La descarga terminó pero no se generó el archivo.")
    return max(archivos, key=lambda p: p.stat().st_size)
