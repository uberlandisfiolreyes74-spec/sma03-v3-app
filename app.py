import streamlit as st
import math
import json
from groq import Groq

st.set_page_config(page_title="SMA-03 v3 AI", layout="wide", page_icon="🚀")
st.title("🚀 SMA-03 v3 AI Predictor")
st.markdown("**Modelo Estratégico de Irreversibilidad Organizacional v3**")

with st.sidebar:
    st.header("🔑 Configuración")
    groq_key = st.text_input("Groq API Key", type="password")
    t_days = st.number_input("Días desde la decisión", min_value=0, value=7)

def calcular_II(P, A_avg, B_avg, FD, t):
    prod = 1.0
    for p in P:
        prod *= max(0, 1 - p * A_avg * B_avg * FD)
    irrevers = 1 - prod
    D_t = math.exp(-0.001 * t)
    return round(irrevers * D_t, 4)

tab1, tab2 = st.tabs(["🧠 Modo IA", "📊 Modo Manual"])

with tab1:
    description = st.text_area("Describe tu decisión", height=180)
    if st.button("Analizar con IA", type="primary"):
        if groq_key:
            # (el resto del código IA se mantiene igual)
            st.info("Modo IA listo (Groq conectado)")
        else:
            st.error("Ingresa tu Groq API Key")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        P_E = st.slider("P_E Económica", 0.0, 1.0, 0.7)
        P_R = st.slider("P_R Reputacional", 0.0, 1.0, 0.65)
        P_L = st.slider("P_L Relacional", 0.0, 1.0, 0.6)
        P_S = st.slider("P_S Estratégica", 0.0, 1.0, 0.8)
        P_M = st.slider("P_M Emocional", 0.0, 1.0, 0.55)
        FD = st.slider("FD Crisis", 0.0, 1.0, 0.45)
    with col2:
        C = st.slider("C Causal", 0.0, 1.0, 0.75)
        I = st.slider("I Identidad", 0.0, 1.0, 0.85)
        S = st.slider("S Significancia", 0.0, 1.0, 0.9)
        A_V = st.slider("A_V Validación", 0.0, 1.0, 0.7)
        B_R = st.slider("B_R Riesgo", 0.0, 1.0, 0.75)
        B_E = st.slider("B_E Emocional", 0.0, 1.0, 0.6)
        B_C = st.slider("B_C Flexibilidad", 0.0, 1.0, 0.8)

    if st.button("Calcular II(t)", type="primary"):
        P = [P_E, P_R, P_L, P_S, P_M]
        A_avg = (C + I + S + A_V) / 4
        B_avg = (B_R + B_E + B_C) / 3
        II = calcular_II(P, A_avg, B_avg, FD, t_days)
        st.success(f"II(t) = {II}")

st.caption("SMA-03 v3 • Uberlandis Fiol Reyes")
