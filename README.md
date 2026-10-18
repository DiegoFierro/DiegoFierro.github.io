# diegofierro.github.io (Hugo)

Portafolio multilingüe (es / en / pt / fr) generado con [Hugo](https://gohugo.io/).
Reemplaza la versión anterior basada en PyScript, que descargaba un intérprete de Python
completo en cada visita. Ahora cada idioma es HTML estático ya renderizado.

## Estructura

```
hugo.toml                 idiomas y configuración
content/_index.<lang>.md  título, descripción y SEO de cada idioma
data/<lang>.yaml          TODO el contenido de cada idioma (antes lang/<lang>.yaml)
data/social.yaml          redes y contacto (comunes a todos los idiomas)
assets/avatar.jpg         foto de perfil (Hugo genera las versiones WebP)
assets/gallery/           fotos de la galería
assets/css/main.css       estilos (se incrustan en el HTML)
assets/icons/             íconos SVG (Font Awesome Free, CC BY 4.0)
layouts/                  plantillas
.github/workflows/        despliegue automático a GitHub Pages
```

## Trabajar en local

Necesitás Hugo **extended** (≥ 0.168): https://gohugo.io/installation/

```bash
hugo server        # http://localhost:1313  (recarga solo)
hugo --minify      # genera ./public
```

## Editar contenido

- Proyectos, blogs, educación, idiomas, intereses: `data/<lang>.yaml`. Los bloques
  comentados con `#` (ejemplos) se activan quitando el `#`.
- Si una lista queda vacía (por ejemplo `blogs`), su pestaña se oculta sola.
- **Galería:** copiá las fotos a `assets/gallery/`, agregá en cada `data/<lang>.yaml`:
  ```yaml
  galeria:
  - src: gallery/foto1.jpg
    caption: Texto de la foto
  ```
  La pestaña aparece cuando hay al menos una foto. Hugo crea miniaturas WebP y
  carga las imágenes de forma diferida.
- Redes / contacto: `data/social.yaml`. Para otro ícono, copiá el SVG de
  Font Awesome Free a `assets/icons/brands/` o `assets/icons/solid/` y usá su nombre
  (`fa-brands fa-mastodon`).
- Agregar un idioma: nuevo bloque en `hugo.toml`, `content/_index.<lang>.md` y `data/<lang>.yaml`.

## Publicar en GitHub Pages

1. En GitHub: **Settings → Pages → Build and deployment → Source: "GitHub Actions"**.
2. En tu clon local del repositorio, borrá lo viejo y copiá esto:
   ```bash
   git rm -r index.html styles.css main.py pyscript.toml lang
   # copiá el contenido de este zip dentro del repo (reemplaza assets/avatar.jpg)
   git add -A
   git commit -m "Migrar a Hugo"
   git push
   ```
3. La pestaña **Actions** compila y publica. Cada `git push` a `main` vuelve a publicar.

`https://diegofierro.github.io/gostack-open/` es otro repositorio y no se ve afectado.
No crees una carpeta `gostack-open` en este proyecto.

## Cambios respecto a la versión PyScript

- `es.yaml` tenía la clave `niveL` (con L mayúscula) en Francés: provocaba un error que
  impedía mostrar "Áreas de Interés" y la galería en español. Corregido.
- "contrucción" → "construcción" en el proyecto GoStack Open (es).
- Se eliminó el bloque `redes` de los YAML: eran enlaces de ejemplo que el sitio nunca usaba
  (los reales estaban en `main.py`, ahora en `data/social.yaml`).
- Font Awesome ya no se carga desde CDN: solo se incrustan los SVG que se usan.
- El idioma ya no es un `<select>` con `localStorage`: son enlaces a `/`, `/en/`, `/pt/`, `/fr/`
  (indexables, compartibles). Se agregaron `hreflang`, canonical, sitemap, robots.txt y JSON-LD.
- Las pestañas funcionan con JavaScript mínimo (~1 KB); sin JS se muestran todas las secciones.
  Cada pestaña tiene URL propia (`/#educacion`).

Los íconos son de Font Awesome Free 6.7.2 (CC BY 4.0), licencia en `assets/icons/LICENSE.txt`.
