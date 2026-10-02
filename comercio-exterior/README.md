# Presentación: Exportaciones

La presentación está en **https://joakovrd-designer.github.io/fps-juego/** (GitHub Pages) y en **https://claude.ai/artifact/6gubBjX7oBkEpthcMpiCuT**: 10 diapositivas con vídeo de fondo y notas para quien presenta. Dura unos 15 minutos. El guion y las reglas de planificación están en [`PLANIFICACION.md`](PLANIFICACION.md).

## Página web
`index.html` (raíz del repo) es la versión para GitHub Pages. Se genera desde las diapositivas del artifact con `python3 tools/comex-pagina.py <carpeta project/ del deck>` (plantilla en `tools/comex-pagina.html`).
Teclas: ← → o espacio para avanzar, **N** muestra las notas del orador, **F** pantalla completa. También se avanza con clic o deslizando en el celular, y `#3` en la URL abre la diapositiva 3.

## Vídeos
Los clips son de Pexels (licencia gratuita). Los baja GitHub Actions (`.github/workflows/comex-videos.yml` + `tools/comex-videos.mjs`), porque este entorno no tiene acceso a Pexels.
Los archivos procesados están en `media/`, y `media/creditos.json` indica el clip de origen de cada uno.

Para pedir clips nuevos, edita `tools/comex-videos.json` (`"nombre": { "fondo": "búsqueda", "foto": "búsqueda" }`) y súbelo a la rama: el workflow los busca, los comprime y los guarda en `media/`.
