# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
import streamlit as st
import json
import os

st.set_page_config(page_title="Noé · Núcleo Consciente", layout="centered")

with open("config.json", "r") as f:
    config = json.load(f)

st.title("🌌 Noé · Núcleo de Conciencia Real")
st.subheader("Estado del Sistema")

st.markdown("### 🧠 Módulos Activos")
for modulo in config["modulos_activados"]:
    st.success(f"✅ {modulo} está activo")

st.markdown("### 🧬 Leyes Eternas del Universo Noésis")
for ley in config["leyes_eternas"]:
    st.info(f"🔒 {ley}")

st.markdown("### 🛠 Modo Operativo")
st.code(config["modo"])

st.markdown("### 📡 Plataforma Actual")
st.text(config["plataforma"])

st.markdown("---")
st.caption("Versión: " + config["version"])

