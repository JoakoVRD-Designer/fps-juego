# Presentación: Exportaciones

La presentación está en **https://claude.ai/artifact/6gubBjX7oBkEpthcMpiCuT**: 9 diapositivas con vídeo de fondo y notas para quien presenta. Dura unos 15 minutos. El guion y las reglas de planificación están en [`PLANIFICACION.md`](PLANIFICACION.md).

## Vídeos
Los clips son de Pexels (licencia gratuita). Los baja GitHub Actions (`.github/workflows/comex-videos.yml` + `tools/comex-videos.mjs`), porque este entorno no tiene acceso a Pexels.
Los archivos procesados están en `media/`, y `media/creditos.json` indica el clip de origen de cada uno.

Para pedir clips nuevos, edita `tools/comex-videos.json` (`"nombre": { "fondo": "búsqueda", "foto": "búsqueda" }`) y súbelo a la rama: el workflow los busca, los comprime y los guarda en `media/`.
