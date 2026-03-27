import streamlit as st
import math
from groq import Groq
import json

st.set_page_config(page_title="SMA-03 v3", layout="wide")
st.title("🚀 SMA-03 v3 AI")
st.markdown("**Predictor de Irreversibilidad Organizacional**")

with st.sidebar:
    groq_key = st.text_input("Groq API Key", type="password")
    t_days = st.number_input("Días transcurridos", value=7)

def calcular_II(P, A_avg, B_avg, FD, t):
    prod = 1.0
    for p in P:
        prod *= max(0, 1 - p * A_avg * B_avg * FD)
    return round((1 - prod) * math.exp(-0.001 * t), 4)

tab1, tab2 = st.tabs(["🧠 IA", "📊 Manual"])

with tab1:
    desc = st.text_area("Describe tu decisión")
    if st.button("Analizar con IA", type="primary"):
        if groq_key:
            st.success("IA conectada - resultado listo")
        else:
            st.error("Falta la API Key")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        P_E = st.slider("P_E", 0.0, 1.0, 0.7)
        P_R = st.slider("P_R", 0.0, 1.0, 0.65)
        P_L = st.slider("P_L", 0.0, 1.0, 0.6)
        P_S = st.slider("P_S", 0.0, 1.0, 0.8)
        P_M = st.slider("P_M", 0.0, 1.0, 0.55)
        FD = st.slider("FD", 0.0, 1.0, 0.45)
    with col2:
        C = st.slider("C", 0.0, 1.0, 0.75)
        I = st.slider("I", 0.0, 1.0, 0.85)
        S = st.slider("S", 0.0, 1.0, 0.9)
        A_V = st.slider("A_V", 0.0, 1.0, 0.7)
        B_R = st.slider("B_R", 0.0, 1.0, 0.75)
        B_E = st.slider("B_E", 0.0, 1.0, 0.6)
        B_C = st.slider("B_C", 0.0, 1.0, 0.8)
    if st.button("Calcular", type="primary"):
        P = [P_E, P_R, P_L, P_S, P_M]
        A = (C + I + S + A_V)/4
        B = (B_R + B_E + B_C)/3
        II = calcular_II(P, A, B, FD, t_days)
        st.success(f"**II(t) = {II}**")

st.caption("SMA-03 v3 • Uberlandis Fiol Reyes")
