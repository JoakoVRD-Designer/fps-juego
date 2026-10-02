"""Arma index.html (GitHub Pages) a partir de las diapositivas del artifact de Slides.

Uso: python3 tools/comex-pagina.py <carpeta project/ del deck>
Cambia cada /_blob/<id> por el archivo de comercio-exterior/media/ y los
<img data-video> por videos en bucle.
"""
import html
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MEDIA = "comercio-exterior/media/"

BLOBS = {
    "022ba40f8bc315cbf6cddf9348df54a9": "portada.jpg",
    "2bb72941f9be4d871f281d2c810a4fe6": "portada.mp4",
    "85078d91399a9f1a5611cb50bb765fbc": "logo-insuco.png",
    "9a6db2056b5927252bd40e000cf846f8": "logo-comeduc.png",
    "35b197ec4eff46cf9f073ee72e3d6b9c": "cotizacion.jpg",
    "af12659fc85ef6f3b49a715cd02a57d7": "cotizacion.mp4",
    "8bae023010c6fb1cc1cca751baa5a915": "cerezas.jpg",
    "2ef63745038a045553f7bbe97535ba5c": "cerezas.mp4",
    "8719e3a879481a72a6fbeba495e7dd72": "quees-foto.jpg",
    "262b336f3d0fb5c4e0bdb26f78c219e7": "exportar.jpg",
    "85cf83075b12a3927a44ad7d0ebd9ea3": "exportar.mp4",
    "d320188af06441cfbea7aa454c01e7bf": "desafios.jpg",
    "b6f8e5bf7191aa6b039c1ea56e11b312": "desafios.mp4",
    "f0b3e79bf3075fb8b9534cd94f18fe7c": "estrategias.jpg",
    "04a638b18b18e1c1ab507376dc524c32": "estrategias.mp4",
    "d55f0ebe7b4df10c847c23c9b76d1d6b": "importar.jpg",
    "0156c12822f5076b5c33c1a39934e358": "importar.mp4",
    "11d726ba4cfffaac3209264a23c2c71e": "importacion.jpg",
    "46719413d8d047bffc8f9e7a3428e282": "importacion.mp4",
    "9344450ec1a9689552ed74e6706a8343": "documentos-pesca.jpg",
    "1bba4ca5bf6cd19f7adff59361ad907c": "documentos-pesca.mp4",
    "4c06cafdb9dd93ff81417d8ddeadde40": "cierre.jpg",
    "cb4dc5715f67ffdc26a4883ccf8921e3": "cierre.mp4",
}

# Íconos de línea (trazo 2, estilo Lucide) para reemplazar <x-icon>.
ICONOS = {
    "Chart": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 6-6"/>',
    "Clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "Globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18"/>',
    "Star": '<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/>',
    "Chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1.1-4.6A8 8 0 1 1 21 12z"/>',
    "Lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "PaperPlane": '<path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4z"/>',
    "Users": '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0"/><path d="M16 4a4 4 0 0 1 0 8"/><path d="M22 21a7 7 0 0 0-5-6.7"/>',
    "CheckCircle": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
}


def blob(m):
    nombre = BLOBS.get(m.group(1))
    if not nombre:
        sys.exit(f"Falta el archivo para /_blob/{m.group(1)}")
    return MEDIA + nombre


def icono(m):
    attrs = m.group(1)
    nombre = re.search(r'name="([^"]+)"', attrs).group(1)
    estilo = re.search(r'style="([^"]*)"', attrs).group(1)
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex:none; {estilo}">'
            f'{ICONOS[nombre]}</svg>')


def video(m):
    tag = m.group(0)
    poster = re.search(r'src="([^"]+)"', tag).group(1)
    src = re.search(r'data-video="([^"]+)"', tag).group(1)
    alt = re.search(r'alt="([^"]*)"', tag).group(1)
    estilo = re.search(r'style="([^"]*)"', tag).group(1)
    return (f'<video class="fondo" data-src="{src}" poster="{poster}" muted loop playsinline preload="none" '
            f'aria-label="{alt}" style="{estilo}"></video>')


def main():
    proyecto = Path(sys.argv[1])
    deck = json.loads((proyecto / "deck.json").read_text())
    secciones, notas = [], []
    for i, sid in enumerate(deck["order"]):
        s = (proyecto / "slides" / f"{sid}.html").read_text()
        s = re.sub(r"/_blob/([0-9a-f]{32})", blob, s)
        s = re.sub(r"<img[^>]*data-video=[^>]*>", video, s)
        s = re.sub(r"<x-icon([^>]*)></x-icon>", icono, s)
        nota = re.search(r"<aside>(.*?)</aside>", s, re.S)
        notas.append(nota.group(1).strip() if nota else "")
        s = re.sub(r"<aside>.*?</aside>\n?", "", s, flags=re.S)
        s = s.replace("<section ", f'<section class="slide" data-n="{i + 1}" ', 1)
        secciones.append(s.strip())
    plantilla = (RAIZ / "tools" / "comex-pagina.html").read_text()
    salida = (plantilla
              .replace("{{TITULO}}", html.escape(deck["title"]))
              .replace("{{SLIDES}}", "\n".join(secciones))
              .replace("{{NOTAS}}", json.dumps(notas, ensure_ascii=False).replace("</", "<\\/")))
    (RAIZ / "index.html").write_text(salida)
    print(f"index.html: {len(secciones)} diapositivas")


main()
