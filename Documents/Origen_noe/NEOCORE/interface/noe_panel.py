# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
import streamlit as st
import os
import glob
import time
import subprocess
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Sistema Noesis", 
    page_icon="🧠",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Título y descripción
st.title("🧠 Sistema Noético Integral")
st.markdown("Panel de control y monitorización del sistema Noesis")

# Sidebar con información y controles
with st.sidebar:
    st.header("Controles del Sistema")
    
    # Estado actual
    st.subheader("Estado Actual")
    estado_resurreccion = "✅ Activo" if subprocess.run(["pgrep", "-f", "resurreccion_noetica.py"], stdout=subprocess.DEVNULL).returncode == 0 else "❌ Inactivo"
    estado_supervisor = "✅ Activo" if subprocess.run(["pgrep", "-f", "supervisor_dinamico_noetico.py"], stdout=subprocess.DEVNULL).returncode == 0 else "❌ Inactivo"
    
    col1, col2 = st.columns(2)
    col1.metric("Resurrección", estado_resurreccion)
    col2.metric("Supervisor", estado_supervisor)
    
    # Botones de acción
    if st.button("Reiniciar Sistema"):
        try:
            subprocess.run(["killall", "python3"], check=False)
            time.sleep(1)
            subprocess.Popen(["python3", os.path.expanduser("~/Noesis_MCP/supervision/resurreccion_noetica.py")], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            st.success("Sistema reiniciado correctamente")
        except Exception as e:
            st.error(f"Error al reiniciar: {e}")
    
    # Información del sistema
    st.subheader("Información del Sistema")
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    st.info(f"Última actualización: {timestamp}")

# Contenido principal en pestañas
tab1, tab2, tab3 = st.tabs(["Dashboard", "Latidos Noéticos", "Logs"])

# Tab 1: Dashboard
with tab1:
    st.header("Dashboard del Sistema Noético")
    
    # Estado de energía
    latidos_dir = os.path.expanduser("~/Noesis_MCP/latidos_de_noesis")
    nivel_energia = 0
    ultimo_latido = ""
    
    if os.path.exists(latidos_dir):
        latidos = sorted(glob.glob(os.path.join(latidos_dir, "*.txt")), reverse=True)
        if latidos:
            with open(latidos[0], "r") as f:
                ultimo_latido = f.read()
                try:
                    # Extraer nivel de energía de formato "[0.XX]"
                    energia_str = ultimo_latido.split("[")[1].split("]")[0]
                    nivel_energia = float(energia_str)
                except:
                    nivel_energia = 0.5
    
    # Mostrar medidor de energía
    st.subheader("Nivel de Energía Noética")
    st.progress(nivel_energia)
    st.caption(ultimo_latido)
    
    # Estado de componentes
    st.subheader("Componentes del Sistema")
    componentes = {
        "Resurrección Noética": {"estado": estado_resurreccion, "descripción": "Sistema principal de vigilancia"},
        "Supervisor Dinámico": {"estado": estado_supervisor, "descripción": "Controlador adaptativo y evolutivo"},
        "Panel Noético": {"estado": "✅ Activo", "descripción": "Interfaz de visualización actual"},
    }
    
    df = pd.DataFrame.from_dict(componentes, orient='index')
    st.table(df)

# Tab 2: Latidos Noéticos
with tab2:
    st.header("Latidos Noéticos Recientes")
    
    latidos_files = []
    latidos_dir = os.path.expanduser("~/Noesis_MCP/latidos_de_noesis")
    
    if os.path.exists(latidos_dir):
        latidos_files = sorted(glob.glob(os.path.join(latidos_dir, "*.txt")), reverse=True)
        
        for latido_file in latidos_files:
            try:
                with open(latido_file, "r") as f:
                    contenido = f.read().strip()
                timestamp = os.path.basename(latido_file).replace("latido_", "").replace(".txt", "")
                fecha = datetime.fromtimestamp(int(timestamp)).strftime("%d-%m-%Y %H:%M:%S")
                
                with st.expander(f"Latido {fecha}"):
                    st.code(contenido)
            except Exception as e:
                st.error(f"Error al leer latido {latido_file}: {e}")
    else:
        st.warning("No se encontraron latidos noéticos registrados")

# Tab 3: Logs
with tab3:
    st.header("Logs del Sistema")
    
    # Seleccionar archivo de log
    log_dir = os.path.expanduser("~/Noesis_MCP/logs")
    log_files = []
    
    if os.path.exists(log_dir):
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
    
    if log_files:
        selected_log = st.selectbox("Seleccionar archivo de log:", log_files)
        log_path = os.path.join(log_dir, selected_log)
        
        try:
            # Leer las últimas 100 líneas del log
            if os.path.exists(log_path):
                resultado = subprocess.check_output(["tail", "-n", "100", log_path]).decode()
                st.text_area("Contenido (últimas 100 líneas):", resultado, height=400)
            else:
                st.warning(f"Archivo {log_path} no encontrado")
        except Exception as e:
            st.error(f"Error al leer log: {e}")
    else:
        st.warning("No se encontraron archivos de log")

# Pie de página
st.markdown("---")
st.caption("Sistema Noético © 2025 - Sistema Autónomo de Autogestión")
