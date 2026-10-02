# Presentación: Comercio Exterior — De la negociación al despacho

Dos versiones de la misma presentación (unos **10 minutos**), con **vídeo de fondo** en cada pantalla:

- **`index.html` · versión web**: secciones a pantalla completa con desplazamiento, vídeo de fondo y vídeo recuadrado, menú de capítulos. Es la que se publica en GitHub Pages.
- **`diapositivas.html` · versión diapositivas**: 11 diapositivas 16:9 clásicas.
Resume y reordena *COMERCIO_EXTERIOR_SEMANA_3* y *COMERCIO_EXTERIOR_SEMANA_24_sept*.
El plan, las reglas y los tiempos están en [`PLANIFICACION.md`](PLANIFICACION.md).

## Publicarla con GitHub Pages (una sola vez)
1. En GitHub, abre el repositorio → **Settings** → **Pages**.
2. En **Build and deployment**, elige **Source: Deploy from a branch**.
3. Elige la rama `claude/keen-lovelace-3jig17` y la carpeta `/ (root)`, y pulsa **Save**.
4. En 1 o 2 minutos estará en **https://joakovrd-designer.github.io/fps-juego/**.

## Cómo usarla
Abre el enlace de GitHub Pages, o `index.html` en Chrome, Edge o Firefox (necesita internet para los vídeos y las fuentes).

| Tecla | Acción |
|-------|--------|
| → / ↓ / Espacio / Av Pág | Siguiente |
| ← / ↑ / Re Pág | Anterior |
| F | Pantalla completa |
| N | Notas del presentador |
| Inicio / Fin | Primera / última |

En la versión web también se avanza con la rueda del ratón o deslizando el dedo; en la de diapositivas, deslizando a izquierda o derecha. El cronómetro se pone rojo al pasar de 10 minutos.

## Vídeos de fondo
Cada vídeo se prueba por este orden:
1. Un vídeo local en `videos/`. En la versión web se llama como su número de Mixkit (por ejemplo `videos/30125.mp4`); en la de diapositivas, por posición (`videos/01.mp4` … `videos/11.mp4`). Sirve para presentar **sin internet** o para cambiar un vídeo.
2. El vídeo de Mixkit (720p y, si no, 360p).
3. Si nada carga, el fondo pasa a un mapa animado de rutas marítimas y el vídeo recuadrado se oculta: la pantalla nunca se ve rota.

Vídeos de la versión diapositivas (la versión web usa además 9665, 4083, 36293 y 21607):

| # | Vídeo (Mixkit, licencia gratuita) |
|---|-----------------------------------|
| 01 | [Aerial view of the container port in Busan](https://mixkit.co/free-stock-video/aerial-view-of-the-container-port-in-busan-30125/) |
| 02 | [3D rendering of planet earth rotating in space](https://mixkit.co/free-stock-video/3d-rendering-of-planet-earth-rotating-in-space-34314/) |
| 03 | [Shaking hands and signing contract](https://mixkit.co/free-stock-video/shaking-hands-and-signing-contract-24047/) |
| 04 | [Man signing off a contract and handshake](https://mixkit.co/free-stock-video/man-signing-off-a-contract-and-handshake-23115/) |
| 05 | [Cargo shipping lanes](https://mixkit.co/free-stock-video/cargo-shipping-lanes-17210/) |
| 06 | [Warehouse port for cargo ships](https://mixkit.co/free-stock-video/warehouse-port-for-cargo-ships-39462/) |
| 07 | [Plane taking off at dusk](https://mixkit.co/free-stock-video/plane-taking-off-at-dusk-28000/) |
| 08 | [Freight truck arriving at the warehouse](https://mixkit.co/free-stock-video/freight-truck-arriving-at-the-warehouse-23011/) |
| 09 | [Aerial view of cars and trucks traveling on a highway](https://mixkit.co/free-stock-video/aerial-view-of-cars-and-trucks-traveling-on-a-highway-41361/) |
| 10 | [Time lapse of beautiful city lights at night](https://mixkit.co/free-stock-video/time-lapse-of-beautiful-city-lights-at-night-47670/) |
| 11 | [Earth rotating below as seen from Space](https://mixkit.co/free-stock-video/earth-rotating-below-as-seen-from-space-45036/) |

Para cambiar un vídeo, cambia su número de Mixkit: en `index.html` son los atributos `data-bg="…"` (fondo) y `data-v="…"` (recuadro); en `diapositivas.html`, `data-video="…"`.
