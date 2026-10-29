# -*- coding: utf-8 -*-
"""Cátedra Cafetera: el territorio como aula.
Prototipo (mock) de la página de registro. Proyecto académico Strategy in Action · Grupo CG-1.
No procesa pagos ni guarda datos: todo vive en la sesión del navegador."""
import random
import re
from datetime import date, timedelta

import streamlit as st

st.set_page_config(page_title="Cátedra Cafetera · Registro", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------------------------------------------------------
# Datos (los mismos del modelo financiero del grupo)
# ---------------------------------------------------------------------------
TRM = 3163.76            # COP por USD, TRM del 21-oct-2026 (referencia)
FINCA_COP = 165_000      # tour en finca por persona (Hacienda Venecia, tarifa de mercado)
FAMILIA_COP = 70_000     # noche en finca cafetera con desayuno (Hacienda Guayabal)

PKGS = {
    "inm": dict(icon="☕", price=1700, days=6, nights=5, kind="uni", min=10, max=15, default=12, comp=2, fincas=3, experts=4,
                community=(3 * FINCA_COP) / TRM,
                dates=[(date(2027, 6, 7), date(2027, 6, 12), "pilot"), (date(2027, 10, 4), date(2027, 10, 9), "")]),
    "campo": dict(icon="🌱", price=4500, days=28, nights=27, kind="uni", min=10, max=14, default=12, comp=1, fincas=10, experts=12,
                  community=(10 * FINCA_COP + 27 * FAMILIA_COP) / TRM,
                  dates=[(date(2027, 11, 1), date(2027, 11, 28), "harvest")]),
    "prem": dict(icon="✨", price=3300, days=6, nights=5, kind="trav", min=1, max=4, default=2, comp=0, fincas=3, experts=4,
                 community=(3 * FINCA_COP) / TRM,
                 dates=[(date(2027, 10, 11), date(2027, 10, 16), "harvest"), (date(2027, 12, 6), date(2027, 12, 11), "")]),
}

# ---------------------------------------------------------------------------
# Textos en español e inglés
# ---------------------------------------------------------------------------
T = {
    "es": {
        "by": "Un programa de la", "comp_short": "profesor(es) acompañante(s)",
        "prog": "Programa",
        "fmm_k": "Quiénes somos",
        "fmm_t": "Más de 60 años educando al sector cafetero colombiano",
        "fmm_p": "La Fundación Manuel Mejía ha acompañado a los caficultores colombianos y a sus comunidades desde su sede educativa en Chinchiná, en el corazón del Paisaje Cultural Cafetero. La Cátedra Cafetera abre ese conocimiento a universidades y viajeros de todo el mundo.",
        "facts": [("+700.000", "caficultores acompañados en más de 60 años"), ("19.406", "estudiantes formados en 2025"), ("46.886", "matrículas en 2025"), ("4,8 / 5", "satisfacción promedio de 15.731 participantes")],
        "fmm_src": "Fuente: Fundación Manuel Mejía, Informe de Gestión 2025.",
        "f_t": "Fundación Manuel Mejía", "f_x": "Sede educativa en Chinchiná, Caldas, Colombia. Educación para el sector cafetero desde hace más de 60 años.",
        "f_h1": "La Cátedra", "f_x1": "Inmersión cafetera · Programa de campo · Experiencia premium · Semestre con créditos (próximamente)",
        "f_h2": "Con el conocimiento de", "f_x2": "Caficultores de Chinchiná como docentes y expertos de Cenicafé.",
        "demo": "Prototipo académico · no procesa pagos ni guarda datos",
        "nav_by": "Fundación Manuel Mejía · Chinchiná, Caldas",
        "hero_kick": "Programas inmersivos en el Paisaje Cultural Cafetero",
        "hero_t1": "El territorio", "hero_t2": "como aula",
        "hero_p": "Aprende el café donde nace: en las fincas de Chinchiná, con caficultores como docentes y con los expertos de Cenicafé. Para universidades internacionales y viajeros que quieren entender el café de verdad.",
        "h_s1": "65 años", "h_l1": "formando al sector cafetero",
        "h_s2": "Caficultores", "h_l2": "pagados como docentes",
        "h_s3": "Cenicafé", "h_l3": "ciencia del café a 10 minutos",
        "steps": ["Elige tu programa", "Configura tu grupo", "Tus datos", "Confirmación"],
        "s1_t": "¿Qué experiencia buscas?", "s1_p": "Tres formatos, un mismo propósito: aprender del café con quienes lo cultivan. Precios en dólares, sin costos ocultos.",
        "per_pax": "por participante", "per_trav": "por viajero",
        "days": "días", "nights": "noches", "group": "Grupo",
        "choose": "Elegir este programa", "chosen": "✓ Seleccionado",
        "badge_inm": "Ideal para empezar", "badge_campo": "Inmersión profunda", "badge_prem": "Experiencia premium",
        "name_inm": "Inmersión cafetera", "name_campo": "Programa de campo", "name_prem": "Experiencia premium",
        "for_inm": "Para cursos cortos de universidades", "for_campo": "Para programas de verano de universidades", "for_prem": "Para viajeros que aman el café",
        "size_inm": "10 a 15 estudiantes", "size_campo": "10 a 14 estudiantes", "size_prem": "Grupos de 6 a 10 viajeros",
        "inc_inm": ["Hotel en Chinchiná (habitación doble) y 3 comidas al día", "Transporte terrestre durante todo el programa", "3 fincas anfitrionas y 4 sesiones con expertos de Cenicafé", "Docente de la FMM y guía bilingüe", "Seguro de asistencia en viaje", "2 profesores acompañantes sin costo"],
        "inc_campo": ["27 noches en finca cafetera con familias anfitrionas", "Almuerzo y cena todos los días; desayuno en la finca", "10 días de aprendizaje en fincas y 12 sesiones con expertos", "Proyecto aplicado a un reto real del sector", "Docente de la FMM, guía bilingüe y seguro de 4 semanas", "1 profesor acompañante sin costo"],
        "inc_prem": ["Hoteles boutique y fincas de gama alta", "Gastronomía regional: 3 comidas al día", "Van privada con conductor", "3 fincas, catación guiada y visita a Cenicafé", "Anfitrión de la FMM y guía bilingüe", "Seguro de asistencia en viaje"],
        "soon_t": "Semestre con créditos", "soon_p": "Llegará cuando los dos primeros formatos demuestren demanda y calidad, y con el aval de una universidad colombiana.", "soon_b": "Próximamente",
        "community": "deja cada participante directamente en familias caficultoras", "community_tot": "Para familias caficultoras",
        "explore": "Conoce más antes de decidir",
        "tab_cmp": "Comparar programas", "tab_it": "Así es un día a día", "tab_faq": "Preguntas frecuentes",
        "cmp_rows": ["Duración", "Precio", "Tamaño del grupo", "Alojamiento", "Fincas anfitrionas", "Sesiones con expertos", "Acompañantes sin costo", "Para quién"],
        "lodg_inm": "Hotel en Chinchiná", "lodg_campo": "Finca con familia caficultora", "lodg_prem": "Boutique y fincas de gama alta",
        "it_pick": "Ver itinerario de",
        "it_inm": [("Día 1", "Llegada y bienvenida", "Recogida en el aeropuerto de Pereira o Manizales, llegada a Chinchiná y primera catación en la sede de la FMM."),
                   ("Día 2", "La ciencia del café", "Jornada en Cenicafé: variedades, clima y suelos, con investigadores del centro."),
                   ("Día 3", "Del cultivo a la cosecha", "Primera finca anfitriona: el caficultor enseña a sembrar, cuidar y recolectar."),
                   ("Día 4", "Beneficio y calidad", "Segunda finca: despulpado, fermentación y secado. Taller de catación por la tarde."),
                   ("Día 5", "Reto aplicado", "Tercera finca: los estudiantes trabajan en un problema real que propone el caficultor."),
                   ("Día 6", "Cierre", "Presentación de soluciones a las familias anfitrionas, certificado y traslado al aeropuerto.")],
        "it_campo": [("Semana 1", "Fundamentos", "Llegada, vida en la finca con la familia anfitriona y bases de agronomía en Cenicafé."),
                     ("Semana 2", "Manos en la tierra", "Rotación por fincas en plena cosecha: recolección, beneficio y calidad."),
                     ("Semana 3", "Proyecto aplicado", "Equipos mixtos diseñan una solución para un reto real del sector cafetero."),
                     ("Semana 4", "Resultados", "Validación con caficultores y expertos, presentación final y cierre.")],
        "it_prem": [("Día 1", "Bienvenida", "Traslado privado, hotel boutique y cena de bienvenida con café de origen."),
                    ("Día 2", "Cenicafé", "Visita privada al centro de investigación del café colombiano."),
                    ("Día 3", "Finca de altura", "Recorrido por el cafetal con el caficultor y almuerzo campesino."),
                    ("Día 4", "Catación", "Catación guiada para aprender a distinguir perfiles y calidades."),
                    ("Día 5", "Del grano a la taza", "Tercera finca: tostión y preparación con métodos de especialidad."),
                    ("Día 6", "Despedida", "Desayuno en la finca y traslado al aeropuerto.")],
        "faq": [("¿Qué no está incluido?", "Los tiquetes aéreos hasta Colombia y los gastos personales. Todo lo demás (alojamiento, comidas, transporte, actividades, seguro y guías) está incluido en el precio."),
                ("¿Cómo se paga?", "En dólares, por transferencia internacional o tarjeta. Se paga 50% como anticipo dos meses antes del inicio y 50% un mes antes. No pedimos ningún pago al registrarte."),
                ("¿Qué pasa si el grupo no se completa?", "Los programas universitarios se confirman con un mínimo de 10 estudiantes. Si no se alcanza, reprogramamos la fecha o devolvemos el 100% del anticipo."),
                ("¿Se otorgan créditos académicos?", "En esta fase no, pero entregamos el plan de estudios y las horas de trabajo para que tu universidad pueda reconocerlas. El semestre con créditos llegará en una segunda fase."),
                ("¿En qué idioma son las actividades?", "En inglés y español. Cada grupo tiene un guía bilingüe durante todo el programa."),
                ("¿Es seguro?", "Usamos transporte especial habilitado, cada participante tiene seguro de asistencia en viaje y la Fundación tiene registro nacional de turismo y póliza de responsabilidad civil."),
                ("¿Atienden dietas especiales?", "Sí. Indícalo en el registro y lo coordinamos con los restaurantes y las familias anfitrionas.")],
        "s2_t": "Configura tu grupo", "s2_p": "Elige la fecha y cuántas personas viajan. El resumen se actualiza en tiempo real.",
        "date": "Fecha", "pilot": "Grupo piloto", "harvest": "Temporada de cosecha",
        "n_uni": "Estudiantes que participan", "n_trav": "Viajeros en esta reserva",
        "min_note": "El grupo se confirma con mínimo 10 estudiantes.", "comp_note": "profesor(es) acompañante(s) viajan sin costo",
        "summary": "Resumen de tu reserva", "subtotal": "Total del programa", "per_day": "por persona al día",
        "pay_plan": "Plan de pagos", "deposit": "Anticipo 50%", "balance": "Saldo 50%", "due": "antes del",
        "today": "Hoy", "today_v": "US$0 · registrarse no tiene costo",
        "cop_ref": "Referencia en pesos con TRM de $3.164 (21-oct-2026)",
        "back": "← Volver", "next": "Continuar →",
        "s3_t": "Cuéntanos quién eres", "s3_p": "Con estos datos te contactamos en menos de 48 horas para confirmar la fecha y el convenio.",
        "inst": "Universidad o institución", "inst_ph": "Ej.: University of Florida", "name": "Nombre completo", "role": "Cargo",
        "role_ph": "Ej.: Profesor(a) de Agronomía", "email": "Correo electrónico", "phone": "Teléfono o WhatsApp (opcional)", "country": "País",
        "diet": "Alimentación especial o accesibilidad (opcional)", "notes": "¿Algo más que debamos saber? (opcional)",
        "terms": "Entiendo que este registro es una solicitud de reserva y que no genera ningún cobro.",
        "submit": "Enviar solicitud de reserva",
        "err_req": "Completa los campos obligatorios.", "err_mail": "Revisa el correo electrónico.", "err_terms": "Debes aceptar las condiciones para continuar.",
        "s4_t": "¡Solicitud recibida!", "s4_p": "Gracias, {name}. Reservamos tu cupo de forma provisional mientras confirmamos los detalles.",
        "code": "Código de reserva", "next_t": "Lo que sigue",
        "nx": ["Te escribimos en menos de 48 horas para resolver dudas y ajustar el itinerario.", "Firmamos el convenio con tu institución.", "Pagas el anticipo del 50% antes del {d1}.", "Pagas el saldo antes del {d2}.", "¡Bienvenidos a Chinchiná el {d3}!"],
        "dl": "Descargar resumen", "again": "Hacer otra reserva",
        "foot": "Cátedra Cafetera · Fundación Manuel Mejía · Prototipo del grupo CG-1, Strategy in Action, Pontificia Universidad Javeriana. Precios de referencia 2027.",
        "months": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
        "to": "al", "persons": "personas", "free": "sin costo", "countries": ["Estados Unidos", "Países Bajos", "Canadá", "Reino Unido", "Alemania", "España", "Colombia", "Otro"],
    },
    "en": {
        "by": "A program by", "comp_short": "accompanying faculty",
        "prog": "Program",
        "fmm_k": "Who we are",
        "fmm_t": "Over 60 years educating Colombia's coffee sector",
        "fmm_p": "Fundación Manuel Mejía has supported Colombian coffee growers and their communities from its campus in Chinchiná, in the heart of the Coffee Cultural Landscape. The Cátedra Cafetera opens that knowledge to universities and travelers from around the world.",
        "facts": [("700,000+", "coffee growers supported over 60 years"), ("19,406", "students trained in 2025"), ("46,886", "course enrollments in 2025"), ("4.8 / 5", "average satisfaction from 15,731 participants")],
        "fmm_src": "Source: Fundación Manuel Mejía, 2025 Management Report.",
        "f_t": "Fundación Manuel Mejía", "f_x": "Campus in Chinchiná, Caldas, Colombia. Education for the coffee sector for over 60 years.",
        "f_h1": "The Cátedra", "f_x1": "Coffee immersion · Field program · Premium experience · Semester with credits (coming soon)",
        "f_h2": "With the knowledge of", "f_x2": "Chinchiná coffee growers as teachers and the experts of Cenicafé.",
        "demo": "Academic prototype · no payments are processed and no data is stored",
        "nav_by": "Fundación Manuel Mejía · Chinchiná, Colombia",
        "hero_kick": "Immersive programs in Colombia's Coffee Cultural Landscape",
        "hero_t1": "The land", "hero_t2": "as a classroom",
        "hero_p": "Learn coffee where it is born: on the farms of Chinchiná, with coffee growers as teachers and the scientists of Cenicafé. For international universities and travelers who want to truly understand coffee.",
        "h_s1": "65 years", "h_l1": "training the coffee sector",
        "h_s2": "Coffee growers", "h_l2": "paid as teachers",
        "h_s3": "Cenicafé", "h_l3": "coffee science 10 minutes away",
        "steps": ["Choose your program", "Set up your group", "Your details", "Confirmation"],
        "s1_t": "What experience are you looking for?", "s1_p": "Three formats, one purpose: learning coffee from the people who grow it. Prices in US dollars, no hidden costs.",
        "per_pax": "per participant", "per_trav": "per traveler",
        "days": "days", "nights": "nights", "group": "Group",
        "choose": "Choose this program", "chosen": "✓ Selected",
        "badge_inm": "Best place to start", "badge_campo": "Deep immersion", "badge_prem": "Premium experience",
        "name_inm": "Coffee immersion", "name_campo": "Field program", "name_prem": "Premium experience",
        "for_inm": "For short university courses", "for_campo": "For university summer programs", "for_prem": "For coffee-loving travelers",
        "size_inm": "10 to 15 students", "size_campo": "10 to 14 students", "size_prem": "Groups of 6 to 10 travelers",
        "inc_inm": ["Hotel in Chinchiná (double room) and 3 meals a day", "Ground transportation throughout the program", "3 host farms and 4 sessions with Cenicafé experts", "FMM instructor and bilingual guide", "Travel assistance insurance", "2 accompanying faculty free of charge"],
        "inc_campo": ["27 nights on a coffee farm with host families", "Lunch and dinner every day; breakfast at the farm", "10 learning days on farms and 12 expert sessions", "Applied project on a real challenge of the sector", "FMM instructor, bilingual guide and 4-week insurance", "1 accompanying faculty member free of charge"],
        "inc_prem": ["Boutique hotels and high-end coffee farms", "Regional cuisine: 3 meals a day", "Private van with driver", "3 farms, guided cupping and a visit to Cenicafé", "FMM host and bilingual guide", "Travel assistance insurance"],
        "soon_t": "Semester with credits", "soon_p": "Coming once the first two formats prove demand and quality, with the endorsement of a Colombian university.", "soon_b": "Coming soon",
        "community": "goes from each participant directly to coffee-growing families", "community_tot": "To coffee-growing families",
        "explore": "Learn more before you decide",
        "tab_cmp": "Compare programs", "tab_it": "Day by day", "tab_faq": "FAQ",
        "cmp_rows": ["Length", "Price", "Group size", "Lodging", "Host farms", "Expert sessions", "Free accompanying faculty", "Best for"],
        "lodg_inm": "Hotel in Chinchiná", "lodg_campo": "Farm stay with a coffee family", "lodg_prem": "Boutique hotels and high-end farms",
        "it_pick": "See the itinerary of",
        "it_inm": [("Day 1", "Arrival and welcome", "Pick-up at Pereira or Manizales airport, arrival in Chinchiná and a first cupping at the FMM campus."),
                   ("Day 2", "The science of coffee", "A day at Cenicafé: varieties, climate and soils, with the center's researchers."),
                   ("Day 3", "From planting to harvest", "First host farm: the grower teaches how to plant, tend and pick coffee."),
                   ("Day 4", "Processing and quality", "Second farm: pulping, fermentation and drying. Cupping workshop in the afternoon."),
                   ("Day 5", "Applied challenge", "Third farm: students work on a real problem proposed by the grower."),
                   ("Day 6", "Closing", "Solutions presented to the host families, certificate and airport transfer.")],
        "it_campo": [("Week 1", "Foundations", "Arrival, farm life with the host family and agronomy basics at Cenicafé."),
                     ("Week 2", "Hands in the soil", "Rotation across farms at the peak of harvest: picking, processing and quality."),
                     ("Week 3", "Applied project", "Mixed teams design a solution to a real challenge of the coffee sector."),
                     ("Week 4", "Results", "Validation with growers and experts, final presentation and closing.")],
        "it_prem": [("Day 1", "Welcome", "Private transfer, boutique hotel and a welcome dinner with single-origin coffee."),
                    ("Day 2", "Cenicafé", "Private visit to Colombia's coffee research center."),
                    ("Day 3", "High-altitude farm", "A walk through the coffee fields with the grower and a farm-style lunch."),
                    ("Day 4", "Cupping", "Guided cupping to learn to tell profiles and qualities apart."),
                    ("Day 5", "Bean to cup", "Third farm: roasting and specialty brewing methods."),
                    ("Day 6", "Farewell", "Breakfast at the farm and airport transfer.")],
        "faq": [("What is not included?", "International flights to Colombia and personal expenses. Everything else (lodging, meals, transportation, activities, insurance and guides) is included in the price."),
                ("How do I pay?", "In US dollars, by international transfer or card. 50% is paid as a deposit two months before the start and 50% one month before. Registering is free."),
                ("What if the group is not full?", "University programs are confirmed with at least 10 students. If that minimum is not reached, we reschedule or refund 100% of the deposit."),
                ("Do students earn academic credit?", "Not in this phase, but we provide the syllabus and contact hours so your university can recognize them. The semester with credits will come in a second phase."),
                ("What language are activities in?", "English and Spanish. Every group has a bilingual guide throughout the program."),
                ("Is it safe?", "We use licensed transportation, every participant has travel assistance insurance, and the Foundation holds a national tourism registration and liability insurance."),
                ("Do you handle special diets?", "Yes. Let us know in the form and we will coordinate with restaurants and host families.")],
        "s2_t": "Set up your group", "s2_p": "Pick a date and how many people are coming. The summary updates in real time.",
        "date": "Date", "pilot": "Pilot group", "harvest": "Harvest season",
        "n_uni": "Participating students", "n_trav": "Travelers in this booking",
        "min_note": "The group is confirmed with at least 10 students.", "comp_note": "accompanying faculty travel free of charge",
        "summary": "Your booking summary", "subtotal": "Program total", "per_day": "per person per day",
        "pay_plan": "Payment plan", "deposit": "50% deposit", "balance": "50% balance", "due": "due by",
        "today": "Today", "today_v": "US$0 · registering is free",
        "cop_ref": "Colombian peso reference at 3,164 COP/USD (Oct 21, 2026)",
        "back": "← Back", "next": "Continue →",
        "s3_t": "Tell us about you", "s3_p": "We will contact you within 48 hours to confirm the date and the agreement.",
        "inst": "University or institution", "inst_ph": "e.g. University of Florida", "name": "Full name", "role": "Role",
        "role_ph": "e.g. Professor of Agronomy", "email": "Email", "phone": "Phone or WhatsApp (optional)", "country": "Country",
        "diet": "Dietary or accessibility needs (optional)", "notes": "Anything else we should know? (optional)",
        "terms": "I understand this is a booking request and no charge will be made.",
        "submit": "Send booking request",
        "err_req": "Please fill in the required fields.", "err_mail": "Please check the email address.", "err_terms": "Please accept the terms to continue.",
        "s4_t": "Request received!", "s4_p": "Thank you, {name}. Your spot is provisionally held while we confirm the details.",
        "code": "Booking code", "next_t": "What happens next",
        "nx": ["We will write to you within 48 hours to answer questions and fine-tune the itinerary.", "We sign the agreement with your institution.", "You pay the 50% deposit by {d1}.", "You pay the balance by {d2}.", "Welcome to Chinchiná on {d3}!"],
        "dl": "Download summary", "again": "Make another booking",
        "foot": "Cátedra Cafetera · Fundación Manuel Mejía · Prototype by group CG-1, Strategy in Action, Pontificia Universidad Javeriana. 2027 reference prices.",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "to": "to", "persons": "people", "free": "free", "countries": ["United States", "Netherlands", "Canada", "United Kingdom", "Germany", "Spain", "Colombia", "Other"],
    },
}

# ---------------------------------------------------------------------------
# Estado
# ---------------------------------------------------------------------------
ss = st.session_state
ss.setdefault("lang", "es")
ss.setdefault("step", 1)
ss.setdefault("pkg", "inm")
ss.setdefault("date_i", 0)
ss.setdefault("n", PKGS["inm"]["default"])
ss.setdefault("form", {})
ss.setdefault("code", "")


def t(k):
    return T[ss.lang][k]


def usd(x):
    s = f"{x:,.0f}"
    return "US$" + (s.replace(",", ".") if ss.lang == "es" else s)


def cop(x):
    s = f"{x:,.0f}"
    return "$" + (s.replace(",", ".") if ss.lang == "es" else s) + " COP"


def fdate(d):
    m = t("months")[d.month - 1]
    return f"{d.day} {m} {d.year}" if ss.lang == "es" else f"{m} {d.day}, {d.year}"


def H(s):
    """Inserta HTML sin la sangría que Markdown confundiría con código."""
    st.markdown("\n".join(line.strip() for line in s.splitlines()), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------
H("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Source+Sans+3:wght@400;500;600;700&display=swap');
:root{--paper:#fbf8f3;--white:#ffffff;--sand:#f1e9dd;--ink:#1f1a16;--ink2:#5f544b;--mute:#8a7e73;--line:#e4dccf;--coffee:#2a1d15;--accent:#8a3b1e;--accent2:#6f2f17;--leaf:#2f5d3a;--gold:#b08a4f;}
html, body, .stApp, .stMarkdown, button, input, textarea, select, label, p, li, span, div{font-family:'Source Sans 3',-apple-system,'Segoe UI',sans-serif !important;}
.stApp{background:var(--paper);}
#MainMenu, footer, header[data-testid="stHeader"]{visibility:hidden;height:0;}
.block-container{padding-top:0;padding-bottom:3rem;max-width:1180px;}
p, li, label, span, div{color:var(--ink);}
.serif, h1, h2, h3, h4, .sec-t{font-family:'Source Serif 4',Georgia,serif !important;}
h1 *, h2 *, h3 *, h4 *, .sec-t *{font-family:inherit !important;}
.demo{background:var(--sand);color:var(--ink2) !important;text-align:center;font-size:13px;padding:7px 12px;margin:12px 0 0;border:1px solid var(--line);border-radius:4px}
.nav{display:flex;align-items:center;justify-content:space-between;padding:22px 0 18px;margin-bottom:6px}
.logo{display:flex;align-items:center;gap:16px}
.logo .by{font-size:11px;font-weight:600;letter-spacing:1.6px;text-transform:uppercase;color:var(--mute) !important;line-height:1.3}
.logo .by b{display:block;color:var(--ink) !important;font-size:13px;letter-spacing:1.2px}
.logo .sep{width:1px;height:38px;background:var(--line)}
.logo .t1{font-family:'Source Serif 4',Georgia,serif !important;font-size:26px;font-weight:600;color:var(--ink);line-height:1;letter-spacing:-.2px}
.logo .t2{font-size:13px;color:var(--ink2) !important;margin-top:4px}
.hero{border-radius:4px;padding:64px 64px 52px;background:var(--coffee);border-top:4px solid var(--gold)}
.hero *{color:#f4ede3}
.hero .kick{font-size:13px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#cfb489 !important}
.hero h1{font-family:'Source Serif 4',Georgia,serif !important;font-size:58px;line-height:1.05;margin:16px 0 18px;color:#fbf8f3 !important;font-weight:600;letter-spacing:-.8px}
.hero h1 em{font-style:italic;font-weight:400;color:#e2cba4 !important}
.hero p{font-size:19px;max-width:680px;line-height:1.6;color:#e6dccd !important}
.hstats{display:flex;gap:0;margin-top:36px;flex-wrap:wrap;border-top:1px solid rgba(244,237,227,.18);padding-top:22px}
.hstat{padding:0 34px 0 0;margin-right:34px;border-right:1px solid rgba(244,237,227,.18)}
.hstat:last-child{border-right:none}
.hstat b{display:block;font-family:'Source Serif 4',Georgia,serif !important;font-size:24px;font-weight:600;color:#fbf8f3 !important}
.hstat span{font-size:14px;color:#cfc2b0 !important}
.fmm{display:grid;grid-template-columns:1.25fr 2fr;gap:48px;padding:44px 0 40px;border-bottom:1px solid var(--line)}
.fmm .k{font-size:12px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--accent) !important}
.fmm h3{font-size:28px;line-height:1.2;margin:10px 0 12px;font-weight:600;color:var(--ink)}
.fmm p{font-size:16px;line-height:1.6;color:var(--ink2) !important}
.facts{display:grid;grid-template-columns:repeat(2,1fr);gap:0;border-top:1px solid var(--line);border-left:1px solid var(--line)}
.fact{padding:20px 24px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--white)}
.fact b{display:block;font-family:'Source Serif 4',Georgia,serif !important;font-size:34px;font-weight:600;color:var(--ink);line-height:1.1}
.fact span{font-size:14.5px;color:var(--ink2) !important}
.fsrc{font-size:12.5px;color:var(--mute) !important;margin-top:10px}
.stepper{display:flex;gap:0;margin:38px 0 6px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.st{flex:1;min-width:150px;display:flex;align-items:center;gap:10px;padding:12px 4px 14px;font-size:15px;font-weight:500;color:var(--mute);border-bottom:3px solid transparent;margin-bottom:-1px}
.st .n{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1.5px solid var(--line);color:var(--mute);font-weight:600;font-size:13px;flex:none;background:var(--white)}
.st.on{color:var(--ink);border-bottom-color:var(--accent);font-weight:600}
.st.on .n{background:var(--accent);border-color:var(--accent);color:#fff !important}
.st.done{color:var(--ink2)}
.st.done .n{background:var(--leaf);border-color:var(--leaf);color:#fff !important}
.sec-t{font-size:34px;font-weight:600;margin:30px 0 6px;color:var(--ink);letter-spacing:-.3px}
.sec-p{font-size:17px;color:var(--ink2) !important;margin-bottom:22px}
.pk{background:var(--white);border:1px solid var(--line);border-radius:6px;padding:28px 26px 20px;min-height:860px;margin-bottom:12px;position:relative;display:flex;flex-direction:column}
.pk.sel{border-color:var(--accent);box-shadow:inset 0 3px 0 var(--accent)}
.pk .badge{font-size:12px;font-weight:600;letter-spacing:1.3px;text-transform:uppercase;color:var(--accent) !important}
.pk.prem .badge{color:var(--gold) !important}
.pk .ic{font-family:'Source Serif 4',Georgia,serif !important;font-size:15px;color:var(--mute) !important;margin:16px 0 2px;font-style:italic}
.pk h3{font-size:26px;margin:0 0 4px;min-height:64px;font-weight:600;letter-spacing:-.2px}
.pk .for{font-size:15px;color:var(--ink2) !important}
.pk .price{font-size:36px;font-weight:700;color:var(--ink);margin-top:20px;line-height:1;letter-spacing:-.5px}
.pk .price small{display:block;font-size:15px;font-weight:400;color:var(--ink2) !important;letter-spacing:0;margin-top:6px}
.pk .meta{display:flex;flex-direction:column;gap:2px;margin:14px 0 4px;font-size:14px;color:var(--ink2)}
.chip{font-size:14.5px;color:var(--ink2) !important}
.chip:last-child{border-right:none}
.pk ul{list-style:none;padding:0;margin:16px 0 6px;border-top:1px solid var(--line)}
.pk li{font-size:14.5px;line-height:1.45;padding:7px 0 7px 24px;position:relative;border-bottom:1px solid #f0eae1}
.pk li:last-child{border-bottom:none}
.pk li:before{content:"✓";position:absolute;left:2px;top:7px;font-weight:700;color:var(--leaf)}
.impact{margin-top:auto;border-left:3px solid var(--leaf);background:#f3f6f1;padding:10px 14px;font-size:14px;color:#2c4a31 !important}
.impact b{color:var(--leaf) !important;font-size:16px}
.soon{border-radius:6px;padding:22px 26px;margin-top:18px;border:1px solid var(--line);background:var(--sand);display:flex;align-items:center;justify-content:space-between;gap:18px}
.soon b{font-family:'Source Serif 4',Georgia,serif !important;font-size:20px;font-weight:600}
.soon span.p{font-size:15px;color:var(--ink2) !important}
.soon .tag{font-size:12px;font-weight:600;letter-spacing:1.3px;text-transform:uppercase;color:var(--ink2) !important;white-space:nowrap;border:1px solid var(--ink2);padding:6px 12px;border-radius:3px}
.sum{background:var(--coffee);border-radius:6px;padding:28px 30px;border-top:4px solid var(--gold)}
.sum *{color:#f4ede3 !important}
.sum .lbl{font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:#cfb489 !important;font-weight:600}
.sum h4{font-family:'Source Serif 4',Georgia,serif !important;font-size:24px;font-weight:600;margin:8px 0 4px;color:#fbf8f3 !important}
.sum .d{font-size:15px;color:#d9ccb9 !important}
.sum .tot{font-size:44px;font-weight:700;line-height:1;margin:20px 0 6px;letter-spacing:-.5px}
.sum .row{display:flex;justify-content:space-between;gap:12px;font-size:15px;padding:10px 0;border-bottom:1px solid rgba(244,237,227,.14)}
.sum .row:last-child{border-bottom:none}
.sum .muted{font-size:12.5px;color:#bfb09c !important;margin-top:12px}
.tl{position:relative;margin:6px 0 0 4px}
.tl .it{position:relative;padding:0 0 20px 28px;border-left:1px solid var(--line)}
.tl .it:last-child{border-left:1px solid transparent}
.tl .it:before{content:"";position:absolute;left:-5px;top:4px;width:9px;height:9px;border-radius:50%;background:var(--accent)}
.tl .it .k{font-size:12px;font-weight:600;letter-spacing:1.3px;text-transform:uppercase;color:var(--mute) !important}
.tl .it b{display:block;font-family:'Source Serif 4',Georgia,serif !important;font-size:19px;font-weight:600;margin:2px 0}
.tl .it span{font-size:15.5px;color:var(--ink2) !important;line-height:1.55}
.cmp{width:100%;border-collapse:collapse;background:var(--white);border:1px solid var(--line)}
.cmp th{background:var(--sand);color:var(--ink) !important;font-family:'Source Serif 4',Georgia,serif !important;font-weight:600;font-size:17px;padding:14px 16px;text-align:left;border-bottom:1px solid var(--line)}
.cmp td{padding:12px 16px;font-size:15px;border-top:1px solid #efe8de}
.cmp td:first-child{color:var(--ink2) !important;font-weight:600;width:24%}
.ok{text-align:center;padding:40px 20px 10px}
.ok .big{width:64px;height:64px;border-radius:50%;margin:0 auto 16px;border:2px solid var(--leaf);display:flex;align-items:center;justify-content:center;font-size:30px;color:var(--leaf) !important}
.ok h2{font-family:'Source Serif 4',Georgia,serif !important;font-size:42px;font-weight:600;margin:0;letter-spacing:-.4px}
.code{display:inline-block;margin-top:12px;font-size:20px;font-weight:600;letter-spacing:2px;background:var(--white);border:1px solid var(--line);padding:10px 22px;border-radius:4px;font-family:'Source Sans 3',monospace !important}
.foot{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:32px;margin-top:56px;padding:32px 0 8px;border-top:1px solid var(--line)}
.foot .ft{font-family:'Source Serif 4',Georgia,serif !important;font-size:19px;font-weight:600;margin-bottom:6px}
.foot .fx{font-size:14px;line-height:1.6;color:var(--ink2) !important}
.foot .fh{font-size:12px;font-weight:600;letter-spacing:1.3px;text-transform:uppercase;color:var(--mute) !important;margin-bottom:6px}
.legal{font-size:12.5px;color:var(--mute) !important;text-align:center;margin-top:24px}
/* Widgets */
.stButton>button, .stDownloadButton>button, .stFormSubmitButton>button{border-radius:4px !important;font-weight:600 !important;font-size:15px !important;padding:.6rem 1.2rem !important;border:1px solid var(--ink2) !important;background:var(--white) !important;color:var(--ink) !important;box-shadow:none !important}
.stButton>button:hover, .stDownloadButton>button:hover{border-color:var(--accent) !important;color:var(--accent) !important}
.stButton>button[kind="primary"], .stFormSubmitButton>button{background:var(--accent) !important;color:#fff !important;border:1px solid var(--accent) !important}
.stButton>button[kind="primary"] p, .stFormSubmitButton>button p{color:#fff !important}
.stButton>button[kind="primary"]:hover, .stFormSubmitButton>button:hover{background:var(--accent2) !important;color:#fff !important}
div[data-baseweb="input"], div[data-baseweb="select"]>div, div[data-baseweb="textarea"]{border-radius:4px !important;background:#fff !important}
.stTabs [data-baseweb="tab-list"]{gap:24px;border-bottom:1px solid var(--line)}
.stTabs [data-baseweb="tab"]{background:transparent;padding:10px 0;font-weight:600;font-size:16px}
div[data-testid="stExpander"]{background:var(--white);border-radius:4px;border:1px solid var(--line)}
div[data-testid="stExpander"] summary p{font-size:16px;font-weight:600}
@media (max-width: 760px){.hero{padding:36px 24px}.hero h1{font-size:40px}.fmm,.foot{grid-template-columns:1fr}.hstat{border-right:none;margin-bottom:12px}.st{min-width:46%}}
</style>
""")

# ---------------------------------------------------------------------------
# Encabezado y héroe
# ---------------------------------------------------------------------------
H(f'<div class="demo">{t("demo")}</div>')
c1, c2 = st.columns([4, 1.3], vertical_alignment="center")
with c1:
    H(f"""<div class="nav"><div class="logo"><div class="by">{t('by')}<b>Fundación Manuel Mejía</b></div><div class="sep"></div><div><div class="t1">Cátedra Cafetera</div><div class="t2">{t('nav_by')}</div></div></div></div>""")
with c2:
    lang = st.radio("Idioma", ["Español", "English"], index=0 if ss.lang == "es" else 1, horizontal=True, label_visibility="collapsed")
    if (lang == "English") != (ss.lang == "en"):
        ss.lang = "en" if lang == "English" else "es"
        st.rerun()

H(f"""<div class="hero">
<div class="kick">{t('hero_kick')}</div>
<h1>{t('hero_t1')}<br><em>{t('hero_t2')}</em></h1>
<p>{t('hero_p')}</p>
<div class="hstats">
<div class="hstat"><b>{t('h_s1')}</b><span>{t('h_l1')}</span></div>
<div class="hstat"><b>{t('h_s2')}</b><span>{t('h_l2')}</span></div>
<div class="hstat"><b>{t('h_s3')}</b><span>{t('h_l3')}</span></div>
</div></div>""")
if ss.step == 1:
    facts = "".join(f'<div class="fact"><b>{n}</b><span>{l}</span></div>' for n, l in t("facts"))
    H(f"""<div class="fmm"><div><div class="k">{t('fmm_k')}</div><h3>{t('fmm_t')}</h3><p>{t('fmm_p')}</p></div>
<div><div class="facts">{facts}</div><div class="fsrc">{t('fmm_src')}</div></div></div>""")


def stepper():
    out = '<div class="stepper">'
    for i, lab in enumerate(t("steps"), 1):
        cls = "on" if i == ss.step else ("done" if i < ss.step else "")
        num = "✓" if i < ss.step else str(i)
        out += f'<div class="st {cls}"><div class="n">{num}</div>{lab}</div>'
    H(out + "</div>")


stepper()
P = PKGS[ss.pkg]


def set_pkg(k):
    ss.pkg = k
    ss.date_i = 0
    ss.n = PKGS[k]["default"]


# ---------------------------------------------------------------------------
# Paso 1: paquetes
# ---------------------------------------------------------------------------
if ss.step == 1:
    H(f'<div class="sec-t">{t("s1_t")}</div><div class="sec-p">{t("s1_p")}</div>')
    cols = st.columns(3, gap="medium")
    for col, k in zip(cols, ["inm", "campo", "prem"]):
        p = PKGS[k]
        with col:
            sel = " sel" if ss.pkg == k else ""
            prem = " prem" if k == "prem" else ""
            per = t("per_trav") if p["kind"] == "trav" else t("per_pax")
            lis = "".join(f"<li>{x}</li>" for x in t("inc_" + k))
            H(f"""<div class="pk{sel}{prem}">
<span class="badge">{t('badge_' + k)}</span>
<div class="ic">{t('prog')} {['inm', 'campo', 'prem'].index(k) + 1:02d}</div>
<h3>{t('name_' + k)}</h3><div class="for">{t('for_' + k)}</div>
<div class="price">{usd(p['price'])} <small>{per}</small></div>
<div class="meta"><span class="chip">{p['days']} {t('days')} · {p['nights']} {t('nights')}</span><span class="chip">{t('size_' + k)}</span></div>
<ul>{lis}</ul>
<div class="impact"><b>{usd(p['community'])}</b> {t('community')}</div>
</div>""")
            if st.button(t("chosen") if ss.pkg == k else t("choose"), key="b_" + k, use_container_width=True, type="primary" if ss.pkg == k else "secondary"):
                set_pkg(k)
                ss.step = 2
                st.rerun()
    H(f"""<div class="soon"><div><b>{t('soon_t')}</b><br><span class="p">{t('soon_p')}</span></div><span class="tag">{t('soon_b')}</span></div>""")

    H(f'<div class="sec-t" style="font-size:24px;margin-top:34px">{t("explore")}</div>')
    tab1, tab2, tab3 = st.tabs([t("tab_cmp"), t("tab_it"), t("tab_faq")])
    with tab1:
        rows = t("cmp_rows")
        vals = {k: [f"{PKGS[k]['days']} {t('days')}", usd(PKGS[k]["price"]), t("size_" + k), t("lodg_" + k), str(PKGS[k]["fincas"]), str(PKGS[k]["experts"]),
                    str(PKGS[k]["comp"]) if PKGS[k]["comp"] else "—", t("for_" + k)] for k in PKGS}
        html = f'<table class="cmp"><tr><th></th>' + "".join(f"<th>{t('name_' + k)}</th>" for k in PKGS) + "</tr>"
        for i, rl in enumerate(rows):
            html += f"<tr><td>{rl}</td>" + "".join(f"<td>{vals[k][i]}</td>" for k in PKGS) + "</tr>"
        H(html + "</table>")
    with tab2:
        names = {k: f"{t('name_' + k)}" for k in PKGS}
        pick = st.radio(t("it_pick"), list(PKGS), format_func=lambda k: names[k], horizontal=True, key="itpick")
        tl = '<div class="tl">' + "".join(f'<div class="it"><div class="k">{a}</div><b>{b}</b><span>{c}</span></div>' for a, b, c in t("it_" + pick)) + "</div>"
        H(tl)
    with tab3:
        for q, a in t("faq"):
            with st.expander(q):
                st.write(a)

# ---------------------------------------------------------------------------
# Paso 2: configuración
# ---------------------------------------------------------------------------
elif ss.step == 2:
    H(f'<div class="sec-t">{t("name_" + ss.pkg)}</div><div class="sec-p">{t("s2_p")}</div>')
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        H(f'<div style="font-weight:600;font-size:18px;margin-bottom:6px">{t("date")}</div>')
        opts = list(range(len(P["dates"])))

        def dlabel(i):
            a, b, tag = P["dates"][i]
            extra = f"  ·  {t(tag)}" if tag else ""
            return f"{fdate(a)} {t('to')} {fdate(b)}{extra}"

        ss.date_i = st.radio(t("date"), opts, index=min(ss.date_i, len(opts) - 1), format_func=dlabel, label_visibility="collapsed")
        st.write("")
        lab = t("n_trav") if P["kind"] == "trav" else t("n_uni")
        ss.n = st.slider(lab, P["min"], P["max"], min(max(ss.n, P["min"]), P["max"]))
        if P["kind"] == "uni":
            st.caption(f"{t('min_note')}  ·  {P['comp']} {t('comp_note')}")
        st.write("")
        H(f'<div style="font-weight:600;font-size:18px;margin:10px 0 6px">{t("tab_it")}</div>')
        tl = '<div class="tl">' + "".join(f'<div class="it"><div class="k">{a}</div><b>{b}</b><span>{c}</span></div>' for a, b, c in t("it_" + ss.pkg)) + "</div>"
        H(tl)
    with right:
        a, b, _ = P["dates"][ss.date_i]
        total = P["price"] * ss.n
        people = ss.n + P["comp"]
        dep_d, bal_d = a - timedelta(days=60), a - timedelta(days=30)
        perday = P["price"] / P["days"]
        comp_row = f'<div class="row"><span>{P["comp"]} {t("comp_short")}</span><span>{t("free")}</span></div>' if P["comp"] else ""
        H(f"""<div class="sum">
<div class="lbl">{t('summary')}</div>
<h4>{t('name_' + ss.pkg)}</h4>
<div class="d">{fdate(a)} {t('to')} {fdate(b)} · {people} {t('persons')}</div>
<div class="tot">{usd(total)}</div>
<div class="d">{t('subtotal')} · {usd(perday)} {t('per_day')}</div>
<div style="margin-top:16px">
<div class="row"><span>{ss.n} × {usd(P['price'])}</span><span>{usd(total)}</span></div>
{comp_row}
<div class="row"><span>{t('community_tot')}</span><span>{usd(P['community'] * ss.n)}</span></div>
</div>
<div class="lbl" style="margin-top:20px">{t('pay_plan')}</div>
<div class="row"><span>{t('today')}</span><span>{t('today_v')}</span></div>
<div class="row"><span>{t('deposit')} · {t('due')} {fdate(dep_d)}</span><span>{usd(total / 2)}</span></div>
<div class="row"><span>{t('balance')} · {t('due')} {fdate(bal_d)}</span><span>{usd(total / 2)}</span></div>
<div class="muted">≈ {cop(total * TRM)} · {t('cop_ref')}</div>
</div>""")
        st.write("")
        b1, b2 = st.columns(2)
        if b1.button(t("back"), use_container_width=True):
            ss.step = 1
            st.rerun()
        if b2.button(t("next"), type="primary", use_container_width=True):
            ss.step = 3
            st.rerun()

# ---------------------------------------------------------------------------
# Paso 3: datos
# ---------------------------------------------------------------------------
elif ss.step == 3:
    H(f'<div class="sec-t">{t("s3_t")}</div><div class="sec-p">{t("s3_p")}</div>')
    left, right = st.columns([1.5, 1], gap="large")
    f = ss.form
    with left:
        with st.form("reg", border=False):
            if P["kind"] == "uni":
                inst = st.text_input(t("inst") + " *", f.get("inst", ""), placeholder=t("inst_ph"))
            else:
                inst = ""
            cA, cB = st.columns(2)
            name = cA.text_input(t("name") + " *", f.get("name", ""))
            role = cB.text_input(t("role"), f.get("role", ""), placeholder=t("role_ph")) if P["kind"] == "uni" else ""
            cC, cD = st.columns(2)
            email = cC.text_input(t("email") + " *", f.get("email", ""), placeholder="name@university.edu")
            phone = cD.text_input(t("phone"), f.get("phone", ""))
            countries = t("countries")
            country = st.selectbox(t("country") + " *", countries, index=f.get("country_i", 0))
            diet = st.text_input(t("diet"), f.get("diet", ""))
            notes = st.text_area(t("notes"), f.get("notes", ""), height=90)
            terms = st.checkbox(t("terms"), value=f.get("terms", False))
            sent = st.form_submit_button(t("submit"), use_container_width=True)
        if sent:
            ss.form = dict(inst=inst, name=name, role=role, email=email, phone=phone, country_i=countries.index(country), country=country,
                           diet=diet, notes=notes, terms=terms)
            missing = not name.strip() or not email.strip() or (P["kind"] == "uni" and not inst.strip())
            if missing:
                st.error(t("err_req"))
            elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()):
                st.error(t("err_mail"))
            elif not terms:
                st.error(t("err_terms"))
            else:
                ss.code = f"CC-2027-{random.randint(1000, 9999)}"
                ss.step = 4
                st.rerun()
        if st.button(t("back")):
            ss.step = 2
            st.rerun()
    with right:
        a, b, _ = P["dates"][ss.date_i]
        total = P["price"] * ss.n
        H(f"""<div class="sum">
<div class="lbl">{t('summary')}</div>
<h4>{t('name_' + ss.pkg)}</h4>
<div class="d">{fdate(a)} {t('to')} {fdate(b)}</div>
<div class="d">{ss.n} × {usd(P['price'])}{f' + {P["comp"]} {t("free")}' if P['comp'] else ''}</div>
<div class="tot">{usd(total)}</div>
<div class="row"><span>{t('today')}</span><span>{t('today_v')}</span></div>
<div class="row"><span>{t('deposit')}</span><span>{usd(total / 2)}</span></div>
<div class="row"><span>{t('balance')}</span><span>{usd(total / 2)}</span></div>
<ul style="margin:14px 0 0 18px;padding:0">{''.join(f'<li style="font-size:13px;margin:4px 0">{x}</li>' for x in t('inc_' + ss.pkg))}</ul>
</div>""")

# ---------------------------------------------------------------------------
# Paso 4: confirmación
# ---------------------------------------------------------------------------
else:
    f = ss.form
    a, b, _ = P["dates"][ss.date_i]
    total = P["price"] * ss.n
    dep_d, bal_d = a - timedelta(days=60), a - timedelta(days=30)
    first = (f.get("name") or "").split(" ")[0]
    H(f"""<div class="ok"><div class="big">✓</div><h2>{t('s4_t')}</h2>
<p style="font-size:17px;color:var(--ink2)">{t('s4_p').format(name=first)}</p>
<div style="font-size:13px;letter-spacing:3px;text-transform:uppercase;color:var(--tan);font-weight:600;margin-top:10px">{t('code')}</div>
<div class="code">{ss.code}</div></div>""")
    left, right = st.columns([1.2, 1], gap="large")
    with left:
        H(f'<div style="font-weight:600;font-size:20px;margin:20px 0 10px">{t("next_t")}</div>')
        nx = [x.format(d1=fdate(dep_d), d2=fdate(bal_d), d3=fdate(a)) for x in t("nx")]
        H('<div class="tl">' + "".join(f'<div class="it"><div class="k">{i}</div><span style="color:var(--ink) !important;font-size:15.5px">{x}</span></div>' for i, x in enumerate(nx, 1)) + "</div>")
    with right:
        st.write("")
        H(f"""<div class="sum">
<div class="lbl">{t('summary')}</div>
<h4>{t('name_' + ss.pkg)}</h4>
<div class="d">{fdate(a)} {t('to')} {fdate(b)}</div>
<div class="d">{f.get('inst') or f.get('name')} · {f.get('country')}</div>
<div class="tot">{usd(total)}</div>
<div class="row"><span>{t('deposit')} · {fdate(dep_d)}</span><span>{usd(total / 2)}</span></div>
<div class="row"><span>{t('balance')} · {fdate(bal_d)}</span><span>{usd(total / 2)}</span></div>
<div class="row"><span>{t('community_tot')}</span><span>{usd(P['community'] * ss.n)}</span></div>
</div>""")
        txt = (f"Cátedra Cafetera · {t('code')}: {ss.code}\n{t('name_' + ss.pkg)}\n{fdate(a)} {t('to')} {fdate(b)}\n"
               f"{ss.n} × {usd(P['price'])} = {usd(total)}\n{t('deposit')}: {usd(total / 2)} ({t('due')} {fdate(dep_d)})\n"
               f"{t('balance')}: {usd(total / 2)} ({t('due')} {fdate(bal_d)})\n{f.get('inst', '')} · {f.get('name', '')} · {f.get('email', '')}\n")
        st.write("")
        d1, d2 = st.columns(2)
        d1.download_button(t("dl"), txt, file_name=f"{ss.code}.txt", use_container_width=True)
        if d2.button(t("again"), type="primary", use_container_width=True):
            ss.step, ss.form, ss.code = 1, {}, ""
            st.rerun()

H(f"""<div class="foot"><div><div class="ft">{t('f_t')}</div><div class="fx">{t('f_x')}</div></div>
<div><div class="fh">{t('f_h1')}</div><div class="fx">{t('f_x1')}</div></div>
<div><div class="fh">{t('f_h2')}</div><div class="fx">{t('f_x2')}</div></div></div>
<div class="legal">{t('foot')}</div>""")
