// Busca en Pexels los clips de la presentación de Comercio Exterior (tools/comex-videos.json) y los deja listos:
//   media/<diapositiva>.mp4        fondo en bucle (1280 px, 10 s, sin audio)
//   media/<diapositiva>.jpg        póster del fondo
//   media/<diapositiva>-foto.jpg   fotograma de otro clip, para la foto recuadrada
//   media/creditos.json            clip de Pexels usado en cada caso
// Lo corre GitHub Actions (.github/workflows/comex-videos.yml), que tiene internet completo.
import { readFileSync, writeFileSync, mkdirSync, statSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, resolve } from "node:path";

const raiz = resolve(import.meta.dirname, "..");
const lista = JSON.parse(readFileSync(join(raiz, "tools/comex-videos.json"), "utf8"));
const salida = join(raiz, "comercio-exterior/media");
const tmp = join(raiz, "tmp");
mkdirSync(salida, { recursive: true });
mkdirSync(tmp, { recursive: true });
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36";
const { chromium } = await import("playwright");
const nav = await chromium.launch();
const usados = new Set();

async function buscar(q) {
  const p = await nav.newPage({ userAgent: UA, viewport: { width: 1600, height: 1200 } });
  try {
    await p.goto(`https://www.pexels.com/search/videos/${encodeURIComponent(q)}/?orientation=landscape`, { waitUntil: "domcontentloaded", timeout: 60000 });
    await p.waitForTimeout(5000);
    await p.mouse.wheel(0, 2000);
    await p.waitForTimeout(1500);
    return await p.evaluate(() => {
      const ids = [];
      for (const a of document.querySelectorAll('a[href*="/video/"]')) {
        const id = a.href.match(/-(\d+)\/?$/)?.[1] || a.href.match(/\/video\/(\d+)/)?.[1];
        if (id && !ids.includes(id)) ids.push(id);
      }
      return ids.slice(0, 8);
    });
  } finally { await p.close(); }
}

async function bajar(url, destino) {
  const r = await fetch(url, { headers: { "user-agent": UA, referer: "https://www.pexels.com/" }, redirect: "follow" });
  const tipo = r.headers.get("content-type") || "";
  if (!r.ok || !tipo.includes("video")) throw new Error(`${r.status} ${tipo}`);
  writeFileSync(destino, Buffer.from(await r.arrayBuffer()));
}

async function bajarVideo(id, destino) {
  for (const u of [`https://www.pexels.com/download/video/${id}/?w=1920`, `https://www.pexels.com/download/video/${id}/`]) {
    try { return await bajar(u, destino); } catch (e) { console.log(`   · ${id}: ${e.message}`); }
  }
  const p = await nav.newPage({ userAgent: UA });
  try {
    await p.goto(`https://www.pexels.com/video/${id}/`, { waitUntil: "domcontentloaded", timeout: 60000 });
    await p.waitForTimeout(4000);
    const html = await p.content();
    const urls = [...new Set(html.match(new RegExp(`https://videos\\.pexels\\.com/video-files/${id}/[^"'\\s\\\\]+?\\.mp4`, "g")) || [])];
    for (const u of urls) try { return await bajar(u, destino); } catch {}
  } finally { await p.close(); }
  throw new Error("sin archivos");
}

// Baja el primer resultado que funcione y que no se haya usado en otra diapositiva
async function primerClip(q, nombre) {
  let ids = [];
  try { ids = await buscar(q); } catch (e) { console.log(`   · búsqueda «${q}»: ${e.message}`); }
  console.log(`${nombre} «${q}»: ${ids.join(", ")}`);
  for (const id of ids) {
    if (usados.has(id)) continue;
    const crudo = join(tmp, `${nombre}-${id}.mp4`);
    try { await bajarVideo(id, crudo); usados.add(id); return { id, crudo }; } catch (e) { console.log(`   · ${id}: ${e.message}`); }
  }
  return null;
}

const ff = (...a) => execFileSync("ffmpeg", ["-y", "-loglevel", "error", ...a]);
const creditos = {};
let fallos = 0;
for (const [nombre, { fondo, foto }] of Object.entries(lista)) {
  const f = await primerClip(fondo, nombre);
  if (!f) { fallos++; console.log(`✘ ${nombre}`); continue; }
  ff("-i", f.crudo, "-t", "10", "-an", "-vf", "scale=1280:-2,fps=25", "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p", "-movflags", "+faststart", join(salida, `${nombre}.mp4`));
  ff("-ss", "1", "-i", f.crudo, "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "4", join(salida, `${nombre}.jpg`));
  creditos[nombre] = { fondo: `https://www.pexels.com/video/${f.id}/` };
  if (foto) {
    const g = await primerClip(foto, `${nombre}-foto`);
    if (g) {
      ff("-ss", "2", "-i", g.crudo, "-frames:v", "1", "-vf", "scale=1000:-2", "-q:v", "3", join(salida, `${nombre}-foto.jpg`));
      creditos[nombre].foto = `https://www.pexels.com/video/${g.id}/`;
    } else { fallos++; console.log(`✘ ${nombre}-foto`); }
  }
  console.log(`✔ ${nombre}: ${(statSync(join(salida, `${nombre}.mp4`)).size / 1e6).toFixed(1)} MB`);
}
await nav.close();
writeFileSync(join(salida, "creditos.json"), JSON.stringify(creditos, null, 2));
if (fallos) process.exitCode = 1;
