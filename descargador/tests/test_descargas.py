"""Pruebas del descargador.

Las pruebas de descarga no necesitan internet: generan videos de muestra con
ffmpeg y los sirven desde un servidor HTTP local.
"""

import functools
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import app as servidor_web  # noqa: E402
from descargas import (  # noqa: E402
    ErrorDescarga,
    _formato_video,
    descargar,
    obtener_info,
    validar_url,
)

HAY_FFMPEG = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def formato_contenedor(ruta):
    """Devuelve el nombre de formato que reporta ffprobe, por ejemplo 'mp4' o 'mp3'."""
    salida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=format_name",
         "-of", "default=nw=1:nk=1", str(ruta)],
        capture_output=True, text=True, check=True,
    )
    return salida.stdout.strip()


class ValidarUrlTests(unittest.TestCase):
    def test_acepta_redes_permitidas(self):
        validos = [
            "https://x.com/usuario/status/123",
            "https://twitter.com/usuario/status/123",
            "https://mobile.twitter.com/usuario/status/123",
            "https://www.instagram.com/reel/AbC123/",
            "https://www.tiktok.com/@usuario/video/123456",
            "https://vm.tiktok.com/ZMabc123/",
            "  https://x.com/a/status/1  ",
        ]
        for url in validos:
            with self.subTest(url=url):
                self.assertEqual(validar_url(url), url.strip())

    def test_rechaza_otros_dominios(self):
        invalidos = [
            "https://evil.com/video.mp4",
            "https://x.com.evil.com/video",
            "https://notx.com/video",
            "https://evil.com/?ref=x.com",
            "https://tiktok.com.attacker.net/v",
        ]
        for url in invalidos:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    validar_url(url)

    def test_rechaza_esquemas_y_vacios(self):
        invalidos = ["", "   ", None, 123, "ftp://x.com/a", "javascript:alert(1)", "x.com/a/status/1"]
        for url in invalidos:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    validar_url(url)

    def test_rechaza_links_muy_largos(self):
        with self.assertRaises(ValueError):
            validar_url("https://x.com/" + "a" * 3000)


class FormatoVideoTests(unittest.TestCase):
    def test_sin_altura_prefiere_mp4(self):
        self.assertTrue(_formato_video(None).startswith("bv*[ext=mp4]"))

    def test_con_altura_limita_la_resolucion(self):
        formato = _formato_video(720)
        self.assertIn("[height<=720]", formato)
        self.assertNotIn("1080", formato)
        self.assertTrue(formato.endswith("/b"))


class ServidorLocalMixin:
    """Genera un MP4 y un WebM de prueba y los sirve por HTTP local."""

    @classmethod
    def setUpClass(cls):
        if not HAY_FFMPEG:
            raise unittest.SkipTest("ffmpeg/ffprobe no están instalados")
        cls.carpeta = Path(tempfile.mkdtemp(prefix="media_prueba_"))
        base = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", "testsrc=duration=2:size=320x240:rate=25",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
        ]
        subprocess.run(base + ["-c:v", "libx264", "-c:a", "aac", "-shortest",
                               str(cls.carpeta / "clip.mp4")], check=True)
        subprocess.run(base + ["-c:v", "libvpx-vp9", "-b:v", "200k", "-c:a", "libopus",
                               "-shortest", str(cls.carpeta / "clip.webm")], check=True)

        class Handler(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass

        handler = functools.partial(Handler, directory=str(cls.carpeta))
        cls.servidor = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.hilo = threading.Thread(target=cls.servidor.serve_forever, daemon=True)
        cls.hilo.start()
        cls.base = f"http://127.0.0.1:{cls.servidor.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        cls.servidor.server_close()
        shutil.rmtree(cls.carpeta, ignore_errors=True)


class DescargaRealTests(ServidorLocalMixin, unittest.TestCase):
    def test_obtener_info_devuelve_campos_esperados(self):
        info = obtener_info(f"{self.base}/clip.mp4")
        self.assertTrue(info["titulo"])
        self.assertIsInstance(info["alturas"], list)
        self.assertIn("miniatura", info)

    def test_descarga_video_en_mp4(self):
        ruta = descargar(f"{self.base}/clip.mp4", "video")
        try:
            self.assertEqual(ruta.suffix, ".mp4")
            self.assertIn("mp4", formato_contenedor(ruta))
        finally:
            shutil.rmtree(ruta.parent, ignore_errors=True)

    def test_convierte_webm_a_mp4(self):
        ruta = descargar(f"{self.base}/clip.webm", "video")
        try:
            self.assertEqual(ruta.suffix, ".mp4")
            self.assertIn("mp4", formato_contenedor(ruta))
        finally:
            shutil.rmtree(ruta.parent, ignore_errors=True)

    def test_descarga_solo_audio_en_mp3(self):
        ruta = descargar(f"{self.base}/clip.mp4", "audio")
        try:
            self.assertEqual(ruta.suffix, ".mp3")
            self.assertEqual(formato_contenedor(ruta), "mp3")
        finally:
            shutil.rmtree(ruta.parent, ignore_errors=True)

    def test_tipo_invalido_lanza_value_error(self):
        with self.assertRaises(ValueError):
            descargar(f"{self.base}/clip.mp4", "exe")

    def test_link_inexistente_da_error_amigable(self):
        with self.assertRaises(ErrorDescarga) as contexto:
            descargar(f"{self.base}/no_existe.mp4", "video")
        self.assertIn("No pude obtener el video", str(contexto.exception))


class ApiWebTests(unittest.TestCase):
    URL = "https://x.com/usuario/status/1"

    def setUp(self):
        servidor_web.app.config["TESTING"] = True
        self.cliente = servidor_web.app.test_client()

    def test_inicio_responde_html(self):
        respuesta = self.cliente.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Descargador de videos", respuesta.get_data(as_text=True))

    def test_info_rechaza_dominio_ajeno(self):
        respuesta = self.cliente.post("/api/info", json={"url": "https://evil.com/x"})
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn("error", respuesta.get_json())

    def test_info_sin_cuerpo_da_400(self):
        respuesta = self.cliente.post("/api/info")
        self.assertEqual(respuesta.status_code, 400)

    def test_body_que_no_es_objeto_da_400(self):
        for cuerpo in (["https://x.com/a/status/1"], "x", 42):
            with self.subTest(cuerpo=cuerpo):
                respuesta = self.cliente.post("/api/descargar", json=cuerpo)
                self.assertEqual(respuesta.status_code, 400)

    def test_info_devuelve_datos(self):
        datos = {"titulo": "t", "autor": "a", "duracion": 3, "miniatura": None, "alturas": [720]}
        with mock.patch.object(servidor_web, "obtener_info", return_value=datos):
            respuesta = self.cliente.post("/api/info", json={"url": self.URL})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.get_json(), datos)

    def test_info_error_de_descarga_es_422(self):
        with mock.patch.object(servidor_web, "obtener_info", side_effect=ErrorDescarga("privado")):
            respuesta = self.cliente.post("/api/info", json={"url": self.URL})
        self.assertEqual(respuesta.status_code, 422)
        self.assertEqual(respuesta.get_json()["error"], "privado")

    def test_descargar_valida_tipo_y_altura(self):
        casos = [
            {"url": self.URL, "tipo": "gif"},
            {"url": self.URL, "tipo": "video", "altura": "abc"},
            {"url": self.URL, "tipo": "video", "altura": 99999},
            {"url": self.URL, "tipo": "video", "altura": 10},
        ]
        for datos in casos:
            with self.subTest(datos=datos):
                respuesta = self.cliente.post("/api/descargar", json=datos)
                self.assertEqual(respuesta.status_code, 400)

    def test_descargar_pasa_altura_como_entero(self):
        archivo = self._archivo_falso()
        with mock.patch.object(servidor_web, "descargar", return_value=archivo) as desc:
            respuesta = self.cliente.post(
                "/api/descargar", json={"url": self.URL, "tipo": "video", "altura": "720"}
            )
            respuesta.close()
        desc.assert_called_once_with(self.URL, "video", 720)

    def test_descargar_mejor_calidad_y_audio_no_pasan_altura(self):
        with mock.patch.object(servidor_web, "descargar", side_effect=lambda *a, **k: self._archivo_falso()) as desc:
            self.cliente.post("/api/descargar", json={"url": self.URL, "tipo": "video", "altura": "mejor"}).close()
            self.cliente.post("/api/descargar", json={"url": self.URL, "tipo": "audio", "altura": "720"}).close()
        self.assertEqual(desc.call_args_list[0].args, (self.URL, "video", None))
        self.assertEqual(desc.call_args_list[1].args, (self.URL, "audio", None))

    def test_descargar_devuelve_archivo_y_borra_carpeta(self):
        archivo = self._archivo_falso()
        carpeta = archivo.parent
        with mock.patch.object(servidor_web, "descargar", return_value=archivo):
            respuesta = self.cliente.post(
                "/api/descargar", json={"url": self.URL, "tipo": "video", "altura": "mejor"}
            )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("attachment", respuesta.headers["Content-Disposition"])
        self.assertEqual(respuesta.data, b"0" * 1024)
        respuesta.close()
        self.assertFalse(carpeta.exists())

    def test_descargar_error_de_descarga_es_422(self):
        with mock.patch.object(servidor_web, "descargar", side_effect=ErrorDescarga("sin ffmpeg")):
            respuesta = self.cliente.post("/api/descargar", json={"url": self.URL, "tipo": "audio"})
        self.assertEqual(respuesta.status_code, 422)
        self.assertEqual(respuesta.get_json()["error"], "sin ffmpeg")

    def test_cors_solo_para_origenes_permitidos(self):
        with mock.patch.object(servidor_web, "ORIGENES_PERMITIDOS", {"https://app.web.app"}):
            permitido = self.cliente.post(
                "/api/info", json={"url": "https://evil.com/x"},
                headers={"Origin": "https://app.web.app"},
            )
            ajeno = self.cliente.post(
                "/api/info", json={"url": "https://evil.com/x"},
                headers={"Origin": "https://otro-sitio.com"},
            )
        self.assertEqual(permitido.headers.get("Access-Control-Allow-Origin"), "https://app.web.app")
        self.assertIsNone(ajeno.headers.get("Access-Control-Allow-Origin"))

    def test_cors_preflight_expone_content_disposition(self):
        with mock.patch.object(servidor_web, "ORIGENES_PERMITIDOS", {"https://app.web.app"}):
            respuesta = self.cliente.open(
                "/api/descargar", method="OPTIONS",
                headers={"Origin": "https://app.web.app", "Access-Control-Request-Method": "POST"},
            )
        self.assertEqual(respuesta.headers.get("Access-Control-Allow-Origin"), "https://app.web.app")
        self.assertIn("POST", respuesta.headers.get("Access-Control-Allow-Methods", ""))
        self.assertIn("Content-Disposition", respuesta.headers.get("Access-Control-Expose-Headers", ""))

    def test_sin_origenes_configurados_no_hay_cors(self):
        with mock.patch.object(servidor_web, "ORIGENES_PERMITIDOS", set()):
            respuesta = self.cliente.post(
                "/api/info", json={"url": "https://evil.com/x"},
                headers={"Origin": "https://app.web.app"},
            )
        self.assertIsNone(respuesta.headers.get("Access-Control-Allow-Origin"))

    @staticmethod
    def _archivo_falso():
        carpeta = Path(tempfile.mkdtemp(prefix="descarga_test_"))
        archivo = carpeta / "video de prueba.mp4"
        archivo.write_bytes(b"0" * 1024)
        return archivo


if __name__ == "__main__":
    unittest.main()
