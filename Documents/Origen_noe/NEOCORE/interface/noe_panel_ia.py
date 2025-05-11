import streamlit as st
import os
import glob
import time
import json
import requests
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Noesis IA", 
    page_icon="🧠",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Título y descripción
st.title("🧠 Noesis IA - Asistente Personal Autónomo")
st.markdown("Centro de control del asistente IA Noesis")

# Verificar conectividad con la API
API_URL = "http://localhost:8601"

try:
    response = requests.get(f"{API_URL}/status", timeout=2)
    if response.status_code == 200:
        estado_api = "✅ Conectado"
        api_data = response.json()
    else:
        estado_api = "❌ Error de conexión"
        api_data = None
except:
    estado_api = "❌ Sin conexión"
    api_data = None

# Barra lateral con controles
with st.sidebar:
    st.header("Control Noesis IA")
    st.metric("Estado API", estado_api)
    
    if api_data:
        # Mostrar estado de componentes
        st.subheader("Componentes")
        componentes = api_data.get("componentes", {})
        for nombre, estado in componentes.items():
            estado_texto = "✅ Activo" if estado else "❌ Inactivo"
            st.markdown(f"**{nombre.capitalize()}**: {estado_texto}")
    
    # Acciones rápidas
    st.subheader("Acciones Rápidas")
    
    col1, col2 = st.columns(2)
    if col1.button("Iniciar Todo"):
        st.info("Iniciando componentes...")
        # Aquí iría el código para iniciar todos los componentes
    
    if col2.button("Detener Todo"):
        st.warning("Deteniendo componentes...")
        # Aquí iría el código para detener todos los componentes
    
    # Control de voz
    st.subheader("Control por Voz")
    texto_voz = st.text_input("Mensaje de voz:", value="Hola, soy Noesis")
    if st.button("Hablar"):
        try:
            response = requests.post(
                f"{API_URL}/sistema/hablar",
                json={"texto": texto_voz},
                timeout=5
            )
            if response.status_code == 200:
                st.success("Mensaje enviado a síntesis de voz")
            else:
                st.error("Error al enviar mensaje a síntesis de voz")
        except Exception as e:
            st.error(f"Error de comunicación: {str(e)}")

# Contenido principal en pestañas
tab1, tab2, tab3, tab4 = st.tabs(["Asistente", "Visión", "Sistema", "Email"])

# Tab 1: Asistente IA
with tab1:
    st.header("Asistente IA Noesis")
    
    # Formulario de consulta
    with st.form("consulta_form"):
        consulta = st.text_area("Consulta al Asistente:", height=150)
        tipo_consulta = st.selectbox(
            "Tipo de consulta:",
            ["general", "email", "documento", "sistema"]
        )
        
        submit_button = st.form_submit_button("Enviar Consulta")
    
    # Procesar consulta
    if submit_button and consulta:
        with st.spinner("Procesando consulta..."):
            try:
                response = requests.post(
                    f"{API_URL}/nucleo/consulta",
                    json={"consulta": consulta, "tipo": tipo_consulta},
                    timeout=30
                )
                
                if response.status_code == 200:
                    respuesta = response.json().get("respuesta", "")
                    st.success("Consulta procesada correctamente")
                    st.write("### Respuesta:")
                    st.markdown(respuesta)
                else:
                    st.error(f"Error al procesar consulta: {response.text}")
            except Exception as e:
                st.error(f"Error de comunicación: {str(e)}")
    
    # Historial de consultas (almacenado en sesión)
    if "historial_consultas" not in st.session_state:
        st.session_state.historial_consultas = []
    
    if submit_button and consulta:
        nueva_consulta = {
            "timestamp": datetime.now().isoformat(),
            "consulta": consulta,
            "tipo": tipo_consulta,
            "respuesta": respuesta if 'respuesta' in locals() else "Error al procesar"
        }
        st.session_state.historial_consultas.append(nueva_consulta)
    
    # Mostrar historial
    if st.session_state.historial_consultas:
        st.subheader("Historial de Consultas")
        for i, item in enumerate(reversed(st.session_state.historial_consultas)):
            with st.expander(f"Consulta {len(st.session_state.historial_consultas) - i}: {item['timestamp']}"):
                st.write(f"**Tipo:** {item['tipo']}")
                st.write(f"**Consulta:**\n{item['consulta']}")
                st.write(f"**Respuesta:**\n{item['respuesta']}")

# Tab 2: Visión
with tab2:
    st.header("Sistema de Visión Noética")
    
    if st.button("Capturar Pantalla"):
        with st.spinner("Capturando pantalla..."):
            try:
                response = requests.post(
                    f"{API_URL}/vision/captura",
                    json={},
                    timeout=10
                )
                
                if response.status_code == 200:
                    ruta = response.json().get("ruta", "")
                    if ruta and os.path.exists(ruta):
                        st.success(f"Captura realizada: {ruta}")
                        st.image(ruta, caption="Captura de pantalla actual")
                    else:
                        st.error(f"No se pudo encontrar la captura: {ruta}")
                else:
                    st.error(f"Error al capturar pantalla: {response.text}")
            except Exception as e:
                st.error(f"Error de comunicación: {str(e)}")
    
    # Historial de capturas
    capturas_dir = os.path.expanduser("~/Noesis_MCP/percepcion/capturas")
    if os.path.exists(capturas_dir):
        capturas = sorted(glob.glob(os.path.join(capturas_dir, "*.png")), reverse=True)
        
        if capturas:
            st.subheader(f"Historial de Capturas ({len(capturas)})")
            
            # Mostrar las últimas capturas en una galería
            for i in range(0, min(len(capturas), 5)):
                timestamp = os.path.basename(capturas[i]).replace("captura_", "").replace(".png", "")
                try:
                    fecha = datetime.strptime(timestamp, "%Y%m%d%H%M%S").strftime("%d-%m-%Y %H:%M:%S")
                except:
                    fecha = timestamp
                
                st.image(capturas[i], caption=f"Captura {fecha}", width=300)

# Tab 3: Sistema
with tab3:
    st.header("Control del Sistema")
    
    # Ejecución de comandos
    with st.form("comando_form"):
        st.subheader("Ejecutar Comando")
        comando = st.text_input("Comando:")
        argumentos = st.text_input("Argumentos (separados por espacio):")
        seguro = st.checkbox("Modo seguro (solo comandos permitidos)", value=True)
        
        submit_cmd = st.form_submit_button("Ejecutar")
    
    if submit_cmd and comando:
        with st.spinner(f"Ejecutando: {comando} {argumentos}"):
            try:
                args_list = argumentos.split() if argumentos else []
                response = requests.post(
                    f"{API_URL}/sistema/ejecutar",
                    json={"comando": comando, "argumentos": args_list, "seguro": seguro},
                    timeout=30
                )
                
                if response.status_code == 200:
                    resultado = response.json()
                    st.write("### Resultado:")
                    
                    # Código de retorno
                    codigo = resultado.get("codigo", -1)
                    estado = "✅ Éxito" if codigo == 0 else f"❌ Error (código {codigo})"
                    st.markdown(f"**Estado:** {estado}")
                    
                    # Salida estándar
                    if "stdout" in resultado and resultado["stdout"]:
                        st.text_area("Salida estándar:", resultado["stdout"], height=200)
                    
                    # Error estándar
                    if "stderr" in resultado and resultado["stderr"]:
                        st.error("Salida de error:")
                        st.text_area("", resultado["stderr"], height=100)
                else:
                    st.error(f"Error al ejecutar comando: {response.text}")
            except Exception as e:
                st.error(f"Error de comunicación: {str(e)}")
    
    # Información del sistema
    st.subheader("Información del Sistema")
    if st.button("Actualizar información"):
        try:
            response = requests.post(
                f"{API_URL}/sistema/ejecutar",
                json={"comando": "uname", "argumentos": ["-a"], "seguro": True},
                timeout=5
            )
            
            if response.status_code == 200:
                resultado = response.json()
                if resultado.get("codigo", -1) == 0:
                    st.code(resultado.get("stdout", ""))
        except Exception as e:
            st.error(f"Error al obtener información: {str(e)}")

# Tab 4: Email
with tab4:
    st.header("Gestión de Email")
    
    # Enviar email
    with st.form("email_form"):
        st.subheader("Enviar Email")
        destinatario = st.text_input("Destinatario:")
        asunto = st.text_input("Asunto:")
        cuerpo = st.text_area("Cuerpo del mensaje:", height=150)
        html = st.checkbox("Formato HTML", value=False)
        
        submit_email = st.form_submit_button("Enviar Email")
    
    if submit_email and destinatario and asunto and cuerpo:
        with st.spinner("Enviando email..."):
            try:
                response = requests.post(
                    f"{API_URL}/email/enviar",
                    json={
                        "destinatario": destinatario,
                        "asunto": asunto,
                        "cuerpo": cuerpo,
                        "html": html
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    resultado = response.json()
                    if resultado.get("exito", False):
                        st.success(f"Email enviado correctamente a {destinatario}")
                    else:
                        st.error("No se pudo enviar el email")
                else:
                    st.error(f"Error al enviar email: {response.text}")
            except Exception as e:
                st.error(f"Error de comunicación: {str(e)}")
    
    # Configuración de email
    st.subheader("Configuración de Email")
    config_path = os.path.expanduser("~/Noesis_MCP/config/email_config.json")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            st.write(f"**Email configurado:** {config.get('email', '')}")
            st.write(f"**Servidor IMAP:** {config.get('imap_servidor', '')}:{config.get('imap_puerto', '')}")
            st.write(f"**Servidor SMTP:** {config.get('smtp_servidor', '')}:{config.get('smtp_puerto', '')}")
            st.write(f"**Estado:** {'✅ Activado' if config.get('activado', False) else '❌ Desactivado'}")
            
            if not config.get('activado', False):
                st.info("El sistema de email está desactivado. Edita el archivo de configuración para activarlo.")
        except Exception as e:
            st.error(f"Error al leer configuración: {str(e)}")
    else:
        st.warning("No se ha encontrado el archivo de configuración de email")

# Pie de página
st.markdown("---")
st.caption("Noesis IA © 2025 - Asistente Personal Autónomo")
