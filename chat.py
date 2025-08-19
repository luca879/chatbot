import streamlit as st
import groq

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192']

# ==========================
# BASE DE CONOCIMIENTOS
# ==========================
knowledge_base = """
Mi nombre es Luca Garrera Buschiazzo, nací el 3 de junio de 2008 y vivo en San Isidro, Buenos Aires, Argentina.
Actualmente curso el último año en el Colegio San José de Martínez, en la orientación Bachiller en Economía y Gestión,
con egreso previsto en 2026.

En cuanto a mi formación complementaria, realicé un curso en programación con Python aplicado a la Inteligencia Artificial
y actualmente me estoy preparando para rendir el First Certificate de Cambridge en inglés, alcanzando un nivel B2.

Respecto a mi experiencia laboral, trabajé en atención al cliente y ventas en una empresa familiar, y también
como asistente administrativo en una empresa de administración de consorcios.

Logros académicos: obtuve el primer puesto en el certamen de Administración Empresarial “Formando Emprendedores” (regional 2024).
Además participé en la organización de ferias americanas escolares y realicé mi confirmación en la Parroquia Santa Teresa de Martínez.

Habilidades técnicas: inglés nivel B2, manejo de Excel, conocimientos en Python (incluyendo generación de scripts para IA).
Competencias personales: comunicación efectiva, trabajo en equipo, orientación a resultados, liderazgo, proactividad, adaptabilidad y organización.

Intereses profesionales: planeo estudiar Administración de Empresas en la UBA, con el objetivo de desarrollarme en el área de
ventas y gestión comercial, aspirando a cargos como gerente de ventas.
"""

# ==========================
# CONFIGURACIÓN PÁGINA
# ==========================
def configurar_pagina():
    st.set_page_config(page_title="MI CHATBOT PERSONAL", page_icon="😀")
    st.title("Bienvenidos a mi chatbot")

    # Mensaje de bienvenida
    st.info("👋 Hola, soy el chatbot de **Luca Garrera Buschiazzo**. Podés preguntarme sobre mis estudios, experiencia, habilidades o intereses profesionales.")

    # Opciones sugeridas
    st.write("### Ejemplos de preguntas que me podés hacer:")
    st.markdown("""
    - 📘 ¿Dónde estudias?  
    - 💼 ¿Qué experiencia laboral tenés?  
    - 🏆 ¿Qué logros académicos alcanzaste?  
    - 🛠️ ¿Cuáles son tus habilidades?  
    - 🎯 ¿Qué carrera pensás estudiar?  
    """)

# ==========================
# SIDEBAR
# ==========================
def mostrar_sidebar():
    st.sidebar.title("ELEJÍ TU MODELO DE IA FAVORITO")
    modelo = st.sidebar.selectbox("¿Cuál elegís?", MODELOS, index=0)
    st.write(f"**ELEJISTE EL MODELO** : {modelo}")
    return modelo

# ==========================
# CREAR CLIENTE GROQ
# ==========================
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)

# ==========================
# ESTADO CHAT
# ==========================
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        # Mensaje de sistema con la base de conocimientos
        st.session_state.mensajes = [
            {"role": "system", "content": f"Eres un chatbot que responde únicamente en base a la siguiente información sobre Luca Garrera Buschiazzo:\n{knowledge_base}"}
        ]

def mostrar_historial_chat():
    for mensajes in st.session_state.mensajes:
        if mensajes["role"] != "system":  # no mostrar system
            with st.chat_message(mensajes["role"]):
                st.markdown(mensajes["content"])

def obtener_mensaje_de_usuario():
    return st.chat_input("Escribí tu pregunta")

def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

# ==========================
# MODELO
# ==========================
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content

# ==========================
# APP
# ==========================
def ejecutar_app():
    configurar_pagina()
    modelo = mostrar_sidebar()
    cliente = crear_cliente_groq()
    inicializacion_estado_chat()
    mostrar_historial_chat()

    mensaje_usuario = obtener_mensaje_de_usuario()
    
    if mensaje_usuario:
        agregar_mensaje_al_historial("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        mensaje_modelo = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)

        agregar_mensaje_al_historial("assistant", mensaje_modelo)
        mostrar_mensaje("assistant", mensaje_modelo)

if __name__ == '__main__':
    ejecutar_app()
