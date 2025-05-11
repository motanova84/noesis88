import streamlit as st
import os
import glob
import time
import json
import requests
import pandas as pd
from datetime import datetime, timedelta

# Configuración de página
st.set_page_config(
    page_title="Sistema Noesis Completo", 
    page_icon="🧠",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Configuración de API
API_BASE_URL = "http://localhost:8700"
MCP_CENTRAL_URL = f"{API_BASE_URL}/mcp/central"

# Función para llamar al MCP central
def mcp_request(target, command, params=None):
    try:
        response = requests.post(
            MCP_CENTRAL_URL,
            json={
                "target": target,
                "query": {
                    "command": command,
                    "params": params or {}
                },
                "context": {}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": f"Error de comunicación: {str(e)}"}

# Verificar conexión con el sistema
def check_system_status():
    try:
        response = requests.get(f"{API_BASE_URL}/mcp/servers", timeout=5)
        if response.status_code == 200:
            return response.json()["servers"]
        return []
    except:
        return []

# Título y descripción
st.title("🧠 Sistema Noesis Completo")
st.markdown("Panel de control y gestión del sistema Noesis con integración MCP")

# Comprobar estado
servidores = check_system_status()
servidores_activos = [s for s in servidores if s.get("status") == "online"]
num_servidores = len(servidores)
num_activos = len(servidores_activos)

# Sidebar
with st.sidebar:
    st.header("Control del Sistema")
    
    # Mostrar estado
    st.subheader("Estado del Sistema")
    status_col1, status_col2 = st.columns(2)
    status_col1.metric("Servidores", f"{num_activos}/{num_servidores}")
    
    if num_activos > 0:
        system_status = "✅ Operativo"
    elif num_servidores > 0:
        system_status = "⚠️ Parcial"
    else:
        system_status = "❌ Sin conexión"
    
    status_col2.metric("Estado", system_status)
    
    # Lista de servidores
    st.subheader("Servidores MCP")
    for servidor in servidores:
        status_icon = "✅" if servidor.get("status") == "online" else "❌"
        st.write(f"{status_icon} {servidor.get('name')} ({servidor.get('id')})")
    
    # Acciones del sistema
    st.subheader("Acciones del Sistema")
    
    if st.button("Refrescar Estado"):
        st.rerun()
    
    # Control de voz
    st.subheader("Control por Voz")
    texto_voz = st.text_input("Mensaje de voz:", value="Hola, soy Noesis")
    if st.button("Hablar"):
        result = mcp_request("workflow", "create_workflow", {
            "name": "Acción: Hablar", 
            "description": "Flujo para sintetizar voz"
        })
        
        if "workflow_id" in result:
            # Añadir tarea
            workflow_id = result["workflow_id"]
            mcp_request("workflow", "add_task", {
                "workflow_id": workflow_id,
                "task_type": "command",
                "task_config": {
                    "name": "Hablar mensaje",
                    "command": "say" if os.name == "posix" else "echo",
                    "arguments": [texto_voz],
                    "shell": False
                }
            })
            
            # Ejecutar workflow
            mcp_request("workflow", "run_workflow", {"workflow_id": workflow_id})
            st.success("Mensaje enviado a síntesis de voz")
        else:
            st.error("Error al iniciar flujo de voz")

# Contenido principal en pestañas
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Documentos", "Flujos de Trabajo", "Calendario", "Domótica"])

# Tab 1: Dashboard
with tab1:
    st.header("Dashboard del Sistema Noesis")
    
    # Mostrar información del sistema
    col1, col2, col3 = st.columns(3)
    
    # Estado de componentes
    with col1:
        st.subheader("Componentes")
        st.write("🧠 **Cerebro IA:** Activo")
        st.write("👁️ **Visión Noética:** Activo")
        st.write("🔄 **Supervisor:** Activo")
        st.write("📅 **Calendario:** Activo")
        st.write("🏠 **Domótica:** Activo")
    
    # Estadísticas
    with col2:
        st.subheader("Estadísticas")
        st.metric("Documentos procesados", "15")
        st.metric("Tareas pendientes", "3")
        st.metric("Flujos activos", "2")
    
    # Acciones rápidas
    with col3:
        st.subheader("Acciones Rápidas")
        if st.button("Procesar Documentos"):
            st.info("Iniciando procesamiento de documentos...")
            
        if st.button("Actualizar Estado Dispositivos"):
            st.info("Actualizando estado de dispositivos...")
    
    # Actividad reciente
    st.subheader("Actividad Reciente")
    actividad = [
        {"fecha": "2025-04-26 00:15", "tipo": "Documento", "descripcion": "Procesado informe.pdf"},
        {"fecha": "2025-04-25 23:45", "tipo": "Email", "descripcion": "Respuesta automática a consulta de cliente"},
        {"fecha": "2025-04-25 22:30", "tipo": "Dispositivo", "descripcion": "Luces de sala apagadas por programación"},
        {"fecha": "2025-04-25 21:15", "tipo": "Tarea", "descripcion": "Recordatorio: Reunión mañana 10:00"}
    ]
    
    st.table(pd.DataFrame(actividad))

# Tab 2: Documentos
with tab2:
    st.header("Gestión de Documentos")
    
    # Opciones
    opciones_doc = st.selectbox(
        "Seleccione operación:",
        ["Buscar Documentos", "Procesar Nuevos", "Ver Estadísticas"]
    )
    
    if opciones_doc == "Buscar Documentos":
        st.subheader("Búsqueda de Documentos")
        
        # Formulario de búsqueda
        with st.form("busqueda_form"):
            consulta = st.text_input("Consulta semántica:")
            categoria = st.selectbox(
                "Categoría:",
                ["Todas", "Informes", "Facturas", "Contratos", "Manuales"]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                num_resultados = st.slider("Máximo de resultados:", 1, 20, 5)
            with col2:
                st.write("Opciones avanzadas:")
                incluir_texto = st.checkbox("Incluir texto completo", value=False)
            
            buscar = st.form_submit_button("Buscar Documentos")
        
        if buscar and consulta:
            st.info(f"Buscando: {consulta}")
            resultado = mcp_request("documentos", "search_documents", {
                "query": consulta,
                "category": None if categoria == "Todas" else categoria.lower(),
                "num_results": num_resultados
            })
            
            if "error" in resultado:
                st.error(f"Error en búsqueda: {resultado['error']}")
            else:
                documentos = resultado.get("response", [])
                
                if documentos:
                    st.success(f"Se encontraron {len(documentos)} documentos")
                    
                    for i, doc in enumerate(documentos):
                        with st.expander(f"{i+1}. {doc.get('titulo', doc.get('nombre', 'Documento'))} - Similitud: {doc.get('similitud', 0):.2f}"):
                            st.write(f"**ID:** {doc.get('id_documento', '')}")
                            st.write(f"**Tipo:** {doc.get('tipo', 'desconocido')}")
                            
                            if "extracto" in doc:
                                st.markdown("**Extracto relevante:**")
                                st.markdown(f"_{doc['extracto']}_")
                            
                            if incluir_texto and "metadatos" in doc:
                                st.markdown("**Metadatos:**")
                                st.json(doc["metadatos"])
                else:
                    st.warning("No se encontraron documentos que coincidan con la búsqueda")
    
    elif opciones_doc == "Procesar Nuevos":
        st.subheader("Procesamiento de Documentos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Carga Manual:**")
            archivo_subido = st.file_uploader("Seleccione un archivo para procesar", 
                                            type=["pdf", "docx", "xlsx", "txt", "jpg", "png"])
            categoria = st.text_input("Categoría:", "General")
            
            if archivo_subido and st.button("Procesar Archivo"):
                st.info(f"Procesando archivo: {archivo_subido.name}")
                # Aquí procesaríamos el archivo subido
        
        with col2:
            st.write("**Procesamiento por Carpeta:**")
            ruta_carpeta = st.text_input("Ruta de carpeta:", "~/Documents/Pendientes")
            recursivo = st.checkbox("Procesar subcarpetas", value=True)
            
            if st.button("Procesar Carpeta"):
                st.info(f"Procesando carpeta: {ruta_carpeta}")
                resultado = mcp_request("documentos", "process_directory", {
                    "dir_path": os.path.expanduser(ruta_carpeta),
                    "recursive": recursivo,
                    "category": categoria
                })
                
                if "error" in resultado:
                    st.error(f"Error al procesar carpeta: {resultado['error']}")
                else:
                    exito = resultado.get("response", {}).get("exito", [])
                    error = resultado.get("response", {}).get("error", [])
                    
                    st.success(f"Procesados {len(exito)} documentos con éxito")
                    if error:
                        st.warning(f"Errores en {len(error)} documentos")
    
    elif opciones_doc == "Ver Estadísticas":
        st.subheader("Estadísticas de Documentos")
        
        # Gráficos simulados
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Documentos por Tipo:**")
            datos_tipo = {
                "PDF": 45,
                "Word": 23,
                "Excel": 12,
                "Imágenes": 8,
                "Otros": 4
            }
            st.bar_chart(pd.DataFrame(list(datos_tipo.items()), columns=["Tipo", "Cantidad"]).set_index("Tipo"))
        
        with col2:
            st.write("**Documentos por Categoría:**")
            datos_categoria = {
                "General": 35,
                "Informes": 20,
                "Facturas": 15,
                "Contratos": 10,
                "Manuales": 12
            }
            st.bar_chart(pd.DataFrame(list(datos_categoria.items()), columns=["Categoría", "Cantidad"]).set_index("Categoría"))

# Tab 3: Flujos de Trabajo
with tab3:
    st.header("Gestión de Flujos de Trabajo")
    
    # Obtener lista de flujos de trabajo
    resultado_lista = mcp_request("workflow", "list_instances", {})
    flujos = resultado_lista.get("instances", [])
    
    # Obtener plantillas
    resultado_plantillas = mcp_request("workflow", "list_templates", {})
    plantillas = resultado_plantillas.get("templates", [])
    
    # Organizar por pestañas
    subtab1, subtab2, subtab3 = st.tabs(["Flujos Activos", "Crear Nuevo", "Plantillas"])
    
    # Subtab 1: Flujos Activos
    with subtab1:
        st.subheader("Flujos de Trabajo Activos")
        
        if flujos:
            for flujo in flujos:
                estado_icon = {
                    "running": "🔄",
                    "completed": "✅",
                    "failed": "❌",
                    "draft": "📝",
                    "scheduled": "⏰"
                }.get(flujo.get("status", ""), "❓")
                
                with st.expander(f"{estado_icon} {flujo.get('name', 'Flujo sin nombre')} ({flujo.get('id', '')})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ID:** {flujo.get('id', '')}")
                        st.write(f"**Estado:** {flujo.get('status', 'desconocido')}")
                        st.write(f"**Inicio:** {flujo.get('start_time', 'N/A')}")
                        st.write(f"**Fin:** {flujo.get('end_time', 'N/A')}")
                    
                    with col2:
                        # Acciones
                        if flujo.get("status") == "draft" or flujo.get("status") == "scheduled":
                            if st.button(f"Ejecutar {flujo.get('id')[:8]}", key=f"run_{flujo.get('id')}"):
                                resultado = mcp_request("workflow", "run_workflow", {"workflow_id": flujo.get("id")})
                                if "error" not in resultado:
                                    st.success("Flujo iniciado correctamente")
                                else:
                                    st.error(f"Error al iniciar flujo: {resultado.get('error')}")
                        
                        if st.button(f"Ver Detalles {flujo.get('id')[:8]}", key=f"details_{flujo.get('id')}"):
                            resultado = mcp_request("workflow", "get_workflow", {"workflow_id": flujo.get("id")})
                            if "error" not in resultado:
                                st.json(resultado)
        else:
            st.info("No hay flujos de trabajo activos")
    
    # Subtab 2: Crear Nuevo
    with subtab2:
        st.subheader("Crear Nuevo Flujo de Trabajo")
        
        with st.form("nuevo_flujo_form"):
            nombre_flujo = st.text_input("Nombre del flujo:")
            descripcion_flujo = st.text_area("Descripción:")
            
            crear_flujo = st.form_submit_button("Crear Flujo")
        
        if crear_flujo and nombre_flujo:
            resultado = mcp_request("workflow", "create_workflow", {
                "name": nombre_flujo,
                "description": descripcion_flujo
            })
            
            if "workflow_id" in resultado:
                st.success(f"Flujo creado con ID: {resultado['workflow_id']}")
            else:
                st.error(f"Error al crear flujo: {resultado.get('error')}")
    
    # Subtab 3: Plantillas
    with subtab3:
        st.subheader("Plantillas de Flujos de Trabajo")
        
        if plantillas:
            for plantilla in plantillas:
                if st.button(f"Cargar plantilla: {plantilla}", key=f"template_{plantilla}"):
                    resultado = mcp_request("workflow", "load_template", {"template_name": plantilla})
                    if "workflow_id" in resultado:
                        st.success(f"Plantilla cargada como flujo {resultado['name']} (ID: {resultado['workflow_id']})")
                    else:
                        st.error(f"Error al cargar plantilla: {resultado.get('error')}")
        else:
            st.info("No hay plantillas disponibles")

# Tab 4: Calendario
with tab4:
    st.header("Gestión de Calendario y Tareas")
    
    # Dividir en pestañas
    cal_tab1, cal_tab2 = st.tabs(["Calendario", "Tareas"])
    
    # Subtab 1: Calendario
    with cal_tab1:
        st.subheader("Calendario")
        
        # Seleccionar rango de fechas
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Fecha inicio:", datetime.now().date())
        with col2:
            fecha_fin = st.date_input("Fecha fin:", (datetime.now() + timedelta(days=7)).date())
        
        if st.button("Obtener Eventos"):
            resultado = mcp_request("calendario", "get_events", {
                "fecha_inicio": fecha_inicio.isoformat(),
                "fecha_fin": fecha_fin.isoformat()
            })
            
            if "error" in resultado:
                st.error(f"Error al obtener eventos: {resultado['error']}")
            else:
                eventos = resultado.get("eventos", [])
                
                if eventos:
                    for evento in eventos:
                        fecha = evento.get("fecha_inicio", "").split("T")[0]
                        hora = evento.get("fecha_inicio", "").split("T")[1][:5] if "T" in evento.get("fecha_inicio", "") else ""
                        
                        with st.expander(f"{fecha} {hora} - {evento.get('titulo', 'Evento sin título')}"):
                            st.write(f"**Calendario:** {evento.get('calendario', 'Personal')}")
                            if evento.get("ubicacion"):
                                st.write(f"**Ubicación:** {evento.get('ubicacion')}")
                            if evento.get("notas"):
                                st.write(f"**Notas:** {evento.get('notas')}")
                else:
                    st.info("No hay eventos en el rango seleccionado")
        
        # Crear nuevo evento
        st.subheader("Crear Nuevo Evento")
        
        with st.form("nuevo_evento_form"):
            titulo_evento = st.text_input("Título:")
            col1, col2 = st.columns(2)
            with col1:
                fecha_evento = st.date_input("Fecha:")
            with col2:
                hora_evento = st.time_input("Hora:")
            ubicacion_evento = st.text_input("Ubicación:")
            notas_evento = st.text_area("Notas:")
            
            crear_evento = st.form_submit_button("Crear Evento")
        
        if crear_evento and titulo_evento:
            # Combinar fecha y hora
            fecha_hora = datetime.combine(fecha_evento, hora_evento).isoformat()
            
            resultado = mcp_request("calendario", "create_event", {
                "evento": {
                    "titulo": titulo_evento,
                    "fecha_inicio": fecha_hora,
                    "fecha_fin": (datetime.combine(fecha_evento, hora_evento) + timedelta(hours=1)).isoformat(),
                    "ubicacion": ubicacion_evento,
                    "notas": notas_evento
                }
            })
            
            if "error" in resultado:
                st.error(f"Error al crear evento: {resultado['error']}")
            else:
                st.success("Evento creado correctamente")
    
    # Subtab 2: Tareas
    with cal_tab2:
        st.subheader("Gestión de Tareas")
        
        # Ver tareas
        mostrar_completadas = st.checkbox("Mostrar tareas completadas")
        
        if st.button("Obtener Tareas"):
            resultado = mcp_request("calendario", "get_tasks", {
                "completadas": mostrar_completadas
            })
            
            if "error" in resultado:
                st.error(f"Error al obtener tareas: {resultado['error']}")
            else:
                tareas = resultado.get("tareas", [])
                
                if tareas:
                    for tarea in tareas:
                        estado = "✅" if tarea.get("completada", False) else "⏳"
                        prioridad = ["🔴 Alta", "🟠 Media", "🟢 Baja"][min(tarea.get("prioridad", 3) - 1, 2)]
                        
                        with st.expander(f"{estado} {tarea.get('titulo', 'Tarea sin título')} - {prioridad}"):
                            if tarea.get("descripcion"):
                                st.write(f"**Descripción:** {tarea.get('descripcion')}")
                            
                            if tarea.get("fecha_vencimiento"):
                                st.write(f"**Vencimiento:** {tarea.get('fecha_vencimiento').split('T')[0]}")
                            
                            if not tarea.get("completada", False):
                                if st.button(f"Completar tarea {tarea.get('id')[:8]}", key=f"complete_{tarea.get('id')}"):
                                    resultado = mcp_request("calendario", "complete_task", {
                                        "tarea_id": tarea.get("id")
                                    })
                                    
                                    if "error" not in resultado:
                                        st.success("Tarea completada")
                                        st.rerun()
                                    else:
                                        st.error(f"Error al completar tarea: {resultado.get('error')}")
                else:
                    st.info("No hay tareas pendientes" if not mostrar_completadas else "No hay tareas")
        
        # Crear nueva tarea
        st.subheader("Crear Nueva Tarea")
        
        with st.form("nueva_tarea_form"):
            titulo_tarea = st.text_input("Título:")
            descripcion_tarea = st.text_area("Descripción:")
            col1, col2 = st.columns(2)
            with col1:
                fecha_venc = st.date_input("Fecha vencimiento:", (datetime.now() + timedelta(days=1)).date())
            with col2:
                prioridad_tarea = st.selectbox("Prioridad:", ["Alta", "Media", "Baja"])
            
            crear_tarea = st.form_submit_button("Crear Tarea")
        
        if crear_tarea and titulo_tarea:
            # Mapear prioridad
            prioridad_map = {"Alta": 1, "Media": 2, "Baja": 3}
            
            resultado = mcp_request("calendario", "create_task", {
                "tarea": {
                    "titulo": titulo_tarea,
                    "descripcion": descripcion_tarea,
                    "fecha_vencimiento": fecha_venc.isoformat(),
                    "prioridad": prioridad_map.get(prioridad_tarea, 3)
                }
            })
            
            if "error" in resultado:
                st.error(f"Error al crear tarea: {resultado['error']}")
            else:
                st.success("Tarea creada correctamente")

# Tab 5: Domótica
with tab5:
    st.header("Control Domótico")
    
    # Verificar estado del servidor de domótica
    servidor_domotica = next((s for s in servidores if s.get("id") == "domotica"), None)
    domotica_activa = servidor_domotica and servidor_domotica.get("status") == "online"
    
    if not domotica_activa:
        st.warning("El servidor de domótica no está disponible. Algunas funciones pueden no estar operativas.")
    
    # Obtener dispositivos
    resultado_disp = mcp_request("domotica", "get_devices", {})
    dispositivos = resultado_disp.get("dispositivos", [])
    
    # Filtrar por tipo
    tipo_filtro = st.selectbox(
        "Filtrar por tipo:",
        ["Todos", "Luces", "Interruptores", "Clima", "Sensores", "Media"]
    )
    
    # Mapeo de tipos en español a inglés
    tipo_map = {
        "Luces": "luz",
        "Interruptores": "interruptor",
        "Clima": "clima",
        "Sensores": "sensor",
        "Media": "media_player"
    }
    
    if tipo_filtro != "Todos":
        dispositivos_filtrados = [d for d in dispositivos if d.get("tipo") == tipo_map.get(tipo_filtro, "")]
    else:
        dispositivos_filtrados = dispositivos
    
    # Dashboard de dispositivos
    if dispositivos_filtrados:
        st.subheader("Dispositivos Domóticos")
        
        # Crear grid de dispositivos
        cols = st.columns(3)
        
        for i, dispositivo in enumerate(dispositivos_filtrados):
            col = cols[i % 3]
            
            with col:
                st.write(f"**{dispositivo.get('nombre', 'Dispositivo')}**")
                
                # Mostrar estado según tipo
                tipo = dispositivo.get("tipo", "")
                estado = dispositivo.get("estado", "desconocido")
                
                if tipo == "luz":
                    if estado == "on":
                        st.write("💡 Encendida")
                        if st.button(f"Apagar {dispositivo.get('id')[:8]}", key=f"off_{dispositivo.get('id')}"):
                            resultado = mcp_request("domotica", "execute_action", {
                                "dispositivo_id": dispositivo.get("id"),
                                "accion": "turn_off"
                            })
                            if "error" not in resultado:
                                st.success("Luz apagada")
                                st.rerun()
                    else:
                        st.write("💡 Apagada")
                        if st.button(f"Encender {dispositivo.get('id')[:8]}", key=f"on_{dispositivo.get('id')}"):
                            resultado = mcp_request("domotica", "execute_action", {
                                "dispositivo_id": dispositivo.get("id"),
                                "accion": "turn_on"
                            })
                            if "error" not in resultado:
                                st.success("Luz encendida")
                                st.rerun()
                
                elif tipo == "interruptor":
                    if estado == "on":
                        st.write("🔌 Activado")
                        if st.button(f"Desactivar {dispositivo.get('id')[:8]}", key=f"off_{dispositivo.get('id')}"):
                            resultado = mcp_request("domotica", "execute_action", {
                                "dispositivo_id": dispositivo.get("id"),
                                "accion": "turn_off"
                            })
                            if "error" not in resultado:
                                st.success("Interruptor desactivado")
                                st.rerun()
                    else:
                        st.write("🔌 Desactivado")
                        if st.button(f"Activar {dispositivo.get('id')[:8]}", key=f"on_{dispositivo.get('id')}"):
                            resultado = mcp_request("domotica", "execute_action", {
                                "dispositivo_id": dispositivo.get("id"),
                                "accion": "turn_on"
                            })
                            if "error" not in resultado:
                                st.success("Interruptor activado")
                                st.rerun()
                
                elif tipo == "clima":
                    atributos = dispositivo.get("atributos", {})
                    temperatura = atributos.get("temperature", "?")
                    
                    st.write(f"🌡️ {estado.capitalize()} - {temperatura}°C")
                    
                    # Control de temperatura
                    nueva_temp = st.slider(
                        f"Temperatura {dispositivo.get('id')[:8]}", 
                        min_value=16, 
                        max_value=30, 
                        value=int(temperatura) if isinstance(temperatura, (int, float)) else 22,
                        key=f"temp_{dispositivo.get('id')}"
                    )
                    
                    if st.button(f"Ajustar temperatura {dispositivo.get('id')[:8]}", key=f"set_{dispositivo.get('id')}"):
                        resultado = mcp_request("domotica", "execute_action", {
                            "dispositivo_id": dispositivo.get("id"),
                            "accion": "set_temperature",
                            "parametros": {"temperature": nueva_temp}
                        })
                        if "error" not in resultado:
                            st.success(f"Temperatura ajustada a {nueva_temp}°C")
                            st.rerun()
                
                elif tipo == "sensor":
                    atributos = dispositivo.get("atributos", {})
                    valor = atributos.get("value", "?")
                    unidad = atributos.get("unit_of_measurement", "")
                    
                    st.write(f"📊 {valor} {unidad}")
                
                elif tipo == "media_player":
                    atributos = dispositivo.get("atributos", {})
                    titulo = atributos.get("media_title", "Nada reproduciendo")
                    
                    st.write(f"🎵 {estado.capitalize()}")
                    st.write(f"**Reproduciendo:** {titulo}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if estado == "playing":
                            if st.button(f"Pausar {dispositivo.get('id')[:8]}", key=f"pause_{dispositivo.get('id')}"):
                                resultado = mcp_request("domotica", "execute_action", {
                                    "dispositivo_id": dispositivo.get("id"),
                                    "accion": "media_pause"
                                })
                        else:
                            if st.button(f"Reproducir {dispositivo.get('id')[:8]}", key=f"play_{dispositivo.get('id')}"):
                                resultado = mcp_request("domotica", "execute_action", {
                                    "dispositivo_id": dispositivo.get("id"),
                                    "accion": "media_play"
                                })
                    
                    with col2:
                        if st.button(f"Siguiente {dispositivo.get('id')[:8]}", key=f"next_{dispositivo.get('id')}"):
                            resultado = mcp_request("domotica", "execute_action", {
                                "dispositivo_id": dispositivo.get("id"),
                                "accion": "media_next_track"
                            })
                
                else:
                    st.write(f"Estado: {estado}")
                
                st.write("---")
    else:
        st.info("No hay dispositivos disponibles")
    
    # Añadir nuevo dispositivo
    with st.expander("Añadir Nuevo Dispositivo"):
        st.subheader("Configurar Nuevo Dispositivo")
        
        with st.form("nuevo_dispositivo_form"):
            nombre_disp = st.text_input("Nombre del dispositivo:")
            tipo_disp = st.selectbox(
                "Tipo de dispositivo:",
                ["luz", "interruptor", "clima", "sensor", "media_player"]
            )
            
            # Para HomeAssistant
            st.write("**Configuración Home Assistant:**")
            entidad_id = st.text_input("ID de entidad:", "light.salon")
            
            agregar_disp = st.form_submit_button("Agregar Dispositivo")
        
        if agregar_disp and nombre_disp and entidad_id:
            resultado = mcp_request("domotica", "add_device", {
                "dispositivo": {
                    "nombre": nombre_disp,
                    "tipo": tipo_disp,
                    "controlador": "home_assistant",
                    "entidad_id": entidad_id
                }
            })
            
            if "error" in resultado:
                st.error(f"Error al agregar dispositivo: {resultado['error']}")
            else:
                st.success(f"Dispositivo {nombre_disp} agregado correctamente")
                st.rerun()

# Pie de página
st.markdown("---")
st.caption("Sistema Noesis MCP © 2025 - Infraestructura Integrada")
