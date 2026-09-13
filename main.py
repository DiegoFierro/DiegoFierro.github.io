# main.py
# Traducción a PyScript (Python en el navegador) del antiguo script.js
# Toda la lógica de renderizado del perfil, cambio de idioma y pestañas
# vive ahora aquí, ejecutada con Pyodide dentro del navegador.
#
# Los archivos de idioma (lang/*.yaml) se cargan y parsean en YAML en
# lugar de JSON. La dependencia "pyyaml" se instala automáticamente vía
# PyScript a partir de pyscript.toml.

import asyncio

import yaml
from js import document, window, localStorage
from pyodide.ffi import create_proxy
from pyodide.http import pyfetch

# Configuración unificada de redes sociales e información de contacto
SOCIAL_LINKS_CONFIG = [
    {"nombre": "LinkedIn", "url": "https://ar.linkedin.com/in/diego-esteban-fierro-92b92a103", "icono": "fa-brands fa-linkedin"},
    {"nombre": "GitHub", "url": "https://github.com/DiegoFierro/", "icono": "fa-brands fa-github"},
    {"nombre": "Facebook", "url": "https://www.facebook.com/DiegoFierro.0/", "icono": "fa-brands fa-facebook"},
    {"nombre": "Instagram", "url": "https://www.instagram.com/fierrod3/", "icono": "fa-brands fa-instagram"},
    {"nombre": "X (Twitter)", "url": "https://x.com/DiegoFierro01", "icono": "fa-brands fa-x-twitter"},
    {"nombre": "WhatsApp", "url": "https://wa.me/5492920354677", "icono": "fa-brands fa-whatsapp"},
    {"nombre": "Telegram", "url": "https://t.me/fierro_de", "icono": "fa-brands fa-telegram"},
    {"nombre": "Email", "url": "mailto:diegoefierro@gmail.com", "icono": "fa-solid fa-envelope", "i18nKey": "email_contact"},
]

current_lang_data = None


def change_language(lang):
    """Equivalente a changeLanguage(lang) en script.js"""
    localStorage.setItem("site_lang", lang)
    asyncio.ensure_future(load_language(lang))


async def load_language(lang):
    """Equivalente a loadLanguage(lang) en script.js"""
    global current_lang_data
    try:
        response = await pyfetch(f"lang/{lang}.yaml")
        if not response.ok:
            raise Exception(f"No se pudo cargar el archivo lang/{lang}.yaml")
        text = await response.string()
        data = yaml.safe_load(text)

        current_lang_data = data
        update_static_ui(data)
        render_profile(data["perfil"])
        render_social()  # Renderiza todas las redes incluyendo el Email
        render_proyectos(data["proyectos"])
        render_blogs(data["blogs"])
        render_educacion(data["educacion"])
        render_idiomas(data["idiomas"])
        render_intereses(data["intereses_y_habilidades"])
        render_galeria(data["galeria"])
    except Exception as error:
        print(f"Error al cambiar de idioma: {error}")


def _get_nested(data, key_path):
    """Recorre un diccionario siguiendo un 'a.b.c' -> data['a']['b']['c']"""
    value = data
    for key in key_path.split("."):
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return None
    return value


def update_static_ui(data):
    """Actualizar textos fijos (títulos de pestañas y secciones)"""
    for element in document.querySelectorAll("[data-i18n]"):
        key_path = element.getAttribute("data-i18n")
        value = _get_nested(data, key_path)
        if value:
            element.textContent = value


def render_profile(perfil):
    document.getElementById("nombre").textContent = perfil["nombre"]
    document.getElementById("titulo").textContent = perfil["titulo"]
    document.getElementById("ubicacion").querySelector("span").textContent = perfil["ubicacion"]
    document.getElementById("avatar").src = perfil["avatar"]
    document.getElementById("bio-text").textContent = perfil["bio"]


def render_social():
    """Renderizado de redes sociales e Email"""
    container = document.getElementById("social-links")
    sections = current_lang_data.get("sections", {})

    html_parts = []
    for r in SOCIAL_LINKS_CONFIG:
        i18n_key = r.get("i18nKey")
        label = sections.get(i18n_key) if i18n_key and sections.get(i18n_key) else r["nombre"]
        html_parts.append(
            f'<a href="{r["url"]}" target="_blank" rel="noopener noreferrer">'
            f'<i class="{r["icono"]}"></i> {label}</a>'
        )
    container.innerHTML = "".join(html_parts)


def _build_ext_link(url, link_text):
    """Construye un enlace externo con ícono, o cadena vacía si no hay url."""
    if not url:
        return ""
    return (
        f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="ext-link">'
        f'{link_text} <i class="fa-solid fa-arrow-up-right-from-square"></i></a>'
    )


def render_proyectos(proyectos):
    container = document.getElementById("proyectos-list")
    link_text = current_lang_data["sections"]["view_link"]
    html_parts = []
    for p in proyectos:
        link_html = _build_ext_link(p.get("link"), link_text)
        html_parts.append(f'''
        <article class="card">
            <div class="card-header">
                <h3><i class="{p["icono"]}"></i> {p["titulo"]}</h3>
                <span class="badge">{p["categoria"]}</span>
            </div>
            <p>{p["descripcion"]}</p>
            {link_html}
        </article>
        ''')
    container.innerHTML = "".join(html_parts)


def render_blogs(blogs):
    container = document.getElementById("blogs-list")
    link_text = current_lang_data["sections"]["visit_blog"]
    html_parts = []
    for b in blogs:
        link_html = _build_ext_link(b.get("url"), link_text)
        html_parts.append(f'''
        <article class="card">
            <h3><i class="{b["icono"]}"></i> {b["titulo"]}</h3>
            <p>{b["descripcion"]}</p>
            {link_html}
        </article>
        ''')
    container.innerHTML = "".join(html_parts)


def render_educacion(educacion):
    container = document.getElementById("educacion-list")
    link_text = current_lang_data["sections"]["view_edu"]
    html_parts = []
    for e in educacion:
        link_html = _build_ext_link(e.get("link"), link_text)
        html_parts.append(f'''
        <article class="card">
            <h3>{e["titulo"]}</h3>
            <p class="institution">{e["institucion"]}</p>
            {link_html}
        </article>
        ''')
    container.innerHTML = "".join(html_parts)


def render_idiomas(idiomas):
    container = document.getElementById("idiomas-list")
    container.innerHTML = "".join(
        f'<li><strong>{i["nombre"]}:</strong> {i["nivel"]}</li>' for i in idiomas
    )


def render_intereses(intereses):
    container = document.getElementById("intereses-container")
    html_parts = []
    for grupo in intereses:
        tags = "".join(f'<span class="skill-tag">{item}</span>' for item in grupo["items"])
        html_parts.append(f'''
        <div class="interest-group">
            <h3>{grupo["categoria"]}</h3>
            <div class="skills-grid">
                {tags}
            </div>
        </div>
        ''')
    container.innerHTML = "".join(html_parts)


def render_galeria(galeria):
    container = document.getElementById("galeria-grid")
    html_parts = []
    for img in galeria:
        html_parts.append(f'''
        <a href="{img["src"]}" target="_blank" rel="noopener noreferrer" class="gallery-card" title="{img["caption"]}">
            <img src="{img["src"]}" alt="{img["caption"]}">
            <p class="caption">{img["caption"]}</p>
        </a>
        ''')
    container.innerHTML = "".join(html_parts)


def open_tab(evt, tab_name):
    for el in document.getElementsByClassName("tab-content"):
        el.classList.remove("active")
    for el in document.getElementsByClassName("tab-btn"):
        el.classList.remove("active")

    document.getElementById(tab_name).classList.add("active")
    evt.currentTarget.classList.add("active")


# Exponer las funciones al ámbito global de JS para que los atributos
# onclick="..." / onchange="..." del HTML sigan funcionando tal cual.
window.changeLanguage = create_proxy(change_language)
window.openTab = create_proxy(open_tab)


async def main():
    # Idioma por defecto o recuperado de la sesión anterior
    saved_lang = localStorage.getItem("site_lang") or "es"
    document.getElementById("language-select").value = saved_lang
    await load_language(saved_lang)


asyncio.ensure_future(main())
