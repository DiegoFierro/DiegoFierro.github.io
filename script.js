// Configuración unificada de redes sociales e información de contacto
const socialLinksConfig = [
    { nombre: "LinkedIn", url: "https://linkedin.com", icono: "fa-brands fa-linkedin" },
    { nombre: "GitHub", url: "https://github.com", icono: "fa-brands fa-github" },
    { nombre: "Facebook", url: "https://facebook.com", icono: "fa-brands fa-facebook" },
    { nombre: "Instagram", url: "https://instagram.com", icono: "fa-brands fa-instagram" },
    { nombre: "X (Twitter)", url: "https://x.com", icono: "fa-brands fa-x-twitter" },
    { nombre: "WhatsApp", url: "https://wa.me/5491100000000", icono: "fa-brands fa-whatsapp" },
    { nombre: "Telegram", url: "https://t.me/tuusuario", icono: "fa-brands fa-telegram" },
    { nombre: "Email", url: "mailto:tuemail@ejemplo.com", icono: "fa-solid fa-envelope", i18nKey: "email_contact" }
];

let currentLangData = null;

document.addEventListener("DOMContentLoaded", () => {
    // Idioma por defecto o recuperado de la sesión anterior
    const savedLang = localStorage.getItem('site_lang') || 'es';
    document.getElementById('language-select').value = savedLang;
    loadLanguage(savedLang);
});

function changeLanguage(lang) {
    localStorage.setItem('site_lang', lang);
    loadLanguage(lang);
}

function loadLanguage(lang) {
    fetch(`lang/${lang}.json`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar el archivo lang/${lang}.json`);
            }
            return response.json();
        })
        .then(data => {
            currentLangData = data;
            updateStaticUI(data);
            renderProfile(data.perfil);
            renderSocial(); // Renderiza todas las redes incluyendo el Email
            renderProyectos(data.proyectos);
            renderBlogs(data.blogs);
            renderEducacion(data.educacion);
            renderIdiomas(data.idiomas);
            renderIntereses(data.intereses_y_habilidades);
            renderGaleria(data.galeria);
        })
        .catch(error => console.error('Error al cambiar de idioma:', error));
}

// Actualizar textos fijos (títulos de pestañas y secciones)
function updateStaticUI(data) {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const keyPath = element.getAttribute('data-i18n').split('.');
        let value = data;
        keyPath.forEach(key => {
            if (value) value = value[key];
        });
        if (value) {
            element.textContent = value;
        }
    });
}

function renderProfile(perfil) {
    document.getElementById('nombre').textContent = perfil.nombre;
    document.getElementById('titulo').textContent = perfil.titulo;
    document.getElementById('ubicacion').querySelector('span').textContent = perfil.ubicacion;
    document.getElementById('avatar').src = perfil.avatar;
    document.getElementById('bio-text').textContent = perfil.bio;
}

// Renderizado de redes sociales e Email
function renderSocial() {
    const container = document.getElementById('social-links');
    
    container.innerHTML = socialLinksConfig.map(r => {
        // Si tiene i18nKey, busca el nombre traducido en sections (ej: sections.email_contact), si no, usa r.nombre
        const label = r.i18nKey && currentLangData.sections[r.i18nKey] 
            ? currentLangData.sections[r.i18nKey] 
            : r.nombre;

        return `<a href="${r.url}" target="_blank" rel="noopener noreferrer">
            <i class="${r.icono}"></i> ${label}
        </a>`;
    }).join('');
}

function renderProyectos(proyectos) {
    const container = document.getElementById('proyectos-list');
    const linkText = currentLangData.sections.view_link;
    container.innerHTML = proyectos.map(p => `
        <article class="card">
            <div class="card-header">
                <h3><i class="${p.icono}"></i> ${p.titulo}</h3>
                <span class="badge">${p.categoria}</span>
            </div>
            <p>${p.descripcion}</p>
            ${p.link ? `<a href="${p.link}" target="_blank" rel="noopener noreferrer" class="ext-link">${linkText} <i class="fa-solid fa-arrow-up-right-from-square"></i></a>` : ''}
        </article>
    `).join('');
}

function renderBlogs(blogs) {
    const container = document.getElementById('blogs-list');
    const linkText = currentLangData.sections.visit_blog;
    container.innerHTML = blogs.map(b => `
        <article class="card">
            <h3><i class="${b.icono}"></i> ${b.titulo}</h3>
            <p>${b.descripcion}</p>
            <a href="${b.url}" target="_blank" rel="noopener noreferrer" class="ext-link">${linkText} <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
        </article>
    `).join('');
}

function renderEducacion(educacion) {
    const container = document.getElementById('educacion-list');
    const linkText = currentLangData.sections.view_edu;
    container.innerHTML = educacion.map(e => `
        <article class="card">
            <h3>${e.titulo}</h3>
            <p class="institution">${e.institucion}</p>
            ${e.link ? `<a href="${e.link}" target="_blank" rel="noopener noreferrer" class="ext-link">${linkText} <i class="fa-solid fa-arrow-up-right-from-square"></i></a>` : ''}
        </article>
    `).join('');
}

function renderIdiomas(idiomas) {
    const container = document.getElementById('idiomas-list');
    container.innerHTML = idiomas.map(i => 
        `<li><strong>${i.nombre}:</strong> ${i.nivel}</li>`
    ).join('');
}

function renderIntereses(intereses) {
    const container = document.getElementById('intereses-container');
    container.innerHTML = intereses.map(grupo => `
        <div class="interest-group">
            <h3>${grupo.categoria}</h3>
            <div class="skills-grid">
                ${grupo.items.map(item => `<span class="skill-tag">${item}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

function renderGaleria(galeria) {
    const container = document.getElementById('galeria-grid');
    container.innerHTML = galeria.map(img => `
        <a href="${img.src}" target="_blank" rel="noopener noreferrer" class="gallery-card" title="${img.caption}">
            <img src="${img.src}" alt="${img.caption}">
            <p class="caption">${img.caption}</p>
        </a>
    `).join('');
}

function openTab(evt, tabName) {
    let tabcontent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }

    let tablinks = document.getElementsByClassName("tab-btn");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }

    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}