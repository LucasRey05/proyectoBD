import os
import shutil
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory

from descargas import ErrorDescarga, descargar, obtener_info, validar_url

# La página vive en public/: es la misma carpeta que sirve Firebase Hosting.
PUBLIC = Path(__file__).resolve().parent / "public"

app = Flask(__name__, static_folder=None)

# Orígenes que pueden llamar a la API desde otro dominio (por ejemplo, Firebase Hosting).
# Se configuran con CORS_ORIGINS, separados por comas. Vacío = solo el mismo origen.
ORIGENES_PERMITIDOS = {
    o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()
}


@app.after_request
def _cors(respuesta):
    origen = request.headers.get("Origin")
    if origen in ORIGENES_PERMITIDOS and request.path.startswith("/api/"):
        respuesta.headers["Access-Control-Allow-Origin"] = origen
        respuesta.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        respuesta.headers["Access-Control-Allow-Headers"] = "Content-Type"
        # Sin esto el navegador no deja leer el nombre del archivo al descargar.
        respuesta.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
        respuesta.headers["Vary"] = "Origin"
    return respuesta

ALTURA_MIN = 144
ALTURA_MAX = 4320


def _error(mensaje, codigo):
    return jsonify(error=mensaje), codigo


def _leer_json():
    """Devuelve el body JSON como dict; si no es un objeto, devuelve un dict vacío."""
    datos = request.get_json(silent=True)
    return datos if isinstance(datos, dict) else {}


@app.get("/")
def inicio():
    return send_from_directory(PUBLIC, "index.html")


@app.post("/api/info")
def api_info():
    datos = _leer_json()
    try:
        url = validar_url(datos.get("url"))
    except ValueError as e:
        return _error(str(e), 400)

    try:
        return jsonify(obtener_info(url))
    except ErrorDescarga as e:
        return _error(str(e), 422)


@app.post("/api/descargar")
def api_descargar():
    datos = _leer_json()
    try:
        url = validar_url(datos.get("url"))
    except ValueError as e:
        return _error(str(e), 400)

    tipo = datos.get("tipo", "video")
    if tipo not in ("video", "audio"):
        return _error("Tipo de descarga inválido.", 400)

    altura = None
    if tipo == "video":
        altura_raw = datos.get("altura")
        if altura_raw not in (None, "", "mejor"):
            try:
                altura = int(altura_raw)
            except (TypeError, ValueError):
                return _error("Calidad inválida.", 400)
            if not ALTURA_MIN <= altura <= ALTURA_MAX:
                return _error("Calidad fuera de rango.", 400)

    try:
        ruta = descargar(url, tipo, altura)
    except ErrorDescarga as e:
        return _error(str(e), 422)

    respuesta = send_file(ruta, as_attachment=True, download_name=ruta.name)
    # Con direct_passthrough (que send_file activa) Werkzeug no llama a close() del
    # response, y el callback de abajo nunca correría. Lo apagamos para que sí corra.
    respuesta.direct_passthrough = False
    # La carpeta temporal se borra recién cuando el servidor terminó de enviar el archivo.
    respuesta.call_on_close(lambda: shutil.rmtree(ruta.parent, ignore_errors=True))
    return respuesta


if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        threaded=True,
    )
