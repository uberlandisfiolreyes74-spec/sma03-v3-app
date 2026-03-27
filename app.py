import streamlit as st
import math
import json
from groq import Groq

st.set_page_config(page_title="SMA-03 v3 AI", layout="wide", page_icon="🚀")
st.title("🚀 SMA-03 v3 AI Predictor")
st.markdown("**Modelo Estratégico de Irreversibilidad Organizacional v3** – Predictor de Lock-in")

# Sidebar
with st.sidebar:
    st.header("🔑 Configuración")
    groq_key = st.text_input("Groq API Key (gratis)", type="password", help="Obténla en console.groq.com")
    t_days = st.number_input("Días desde la decisión (t)", min_value=0, value=7, step=1)

# Función de cálculo exacta del paper v3
def calcular_II(P, A_avg, B_avg, FD, t):
    prod = 1.0
    for p in P:
        prod *= max(0, 1 - p * A_avg * B_avg * FD)
    irrevers = 1 - prod
    D_t = math.exp(-0.001 * t)
    return round(irrevers * D_t, 4)

# Tabs
tab1, tab2 = st.tabs(["🧠 Modo IA (descripción en texto)", "📊 Modo Manual (sliders)"])

# ==================== MODO IA ====================
with tab1:
    st.subheader("Describe tu decisión estratégica")
    description = st.text_area("Descripción completa de la decisión", height=200,
                               placeholder="Estamos considerando la adquisición de Empresa X por $500M bajo presión de inversores y competencia...")

    if st.button("🔮 Analizar con IA", type="primary"):
        if not groq_key:
            st.error("⚠️ Ingresa tu Groq API Key en el sidebar")
        else:
            with st.spinner("Extrayendo variables con IA (SMA-03 v3)..."):
                client = Groq(api_key=groq_key)
                prompt = """Eres experto en SMA-03 v3. Analiza la descripción y devuelve SOLO un JSON válido con estos 13 valores exactos entre 0 y 1:
{"P_E": , "P_R": , "P_L": , "P_S": , "P_M": , "C": , "I": , "S": , "A_V": , "B_R": , "B_E": , "B_C": , "FD": }
No expliques nada, solo el JSON."""

                try:
                    response = client.chat.completions.create(
                        model="llama3-70b-8192",
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": description}
                        ],
                        temperature=0.1,
                        response_format={"type": "json_object"}
                    )
                    vars_dict = json.loads(response.choices[0].message.content)

                    # Cálculo
                    P = [vars_dict["P_E"], vars_dict["P_R"], vars_dict["P_L"], vars_dict["P_S"], vars_dict["P_M"]]
                    A_avg = (vars_dict["C"] + vars_dict["I"] + vars_dict["S"] + vars_dict["A_V"]) / 4
                    B_avg = (vars_dict["B_R"] + vars_dict["B_E"] + vars_dict["B_C"]) / 3
                    II = calcular_II(P, A_avg, B_avg, vars_dict["FD"], t_days)

                    # Resultados
                    st.success(f"**Índice de Irreversibilidad II(t) = {II}**")
                    st.latex(r"II(t) = [1 - \prod (1 - P_i \times A_{avg} \times B_{avg} \times FD)] \times e^{-0.001 t}")

                    if II < 0.50:
                        st.balloons()
                        st.success("✅ REVERSIBLE - Probabilidad de éxito 93%")
                    elif II < 0.70:
                        st.warning("⚠️ VENTANA CRÍTICA (90 días) - Actúa YA")
                    else:
                        st.error("🔴 LOCK-IN ALTO - Intervención urgente requerida")

                    st.json(vars_dict)

                except Exception as e:
                    st.error(f"Error: {e}. Prueba el Modo Manual.")

# ==================== MODO MANUAL ====================
with tab2:
    st.subheader("Ajusta manualmente los 13 parámetros (v3)")
    col1, col2 = st.columns(2)
    with col1:
        P_E = st.slider("P_E - Económica", 0.0, 1.0, 0.70)
        P_R = st.slider("P_R - Reputacional", 0.0, 1.0, 0.65)
        P_L = st.slider("P_L - Relacional", 0.0, 1.0, 0.60)
        P_S = st.slider("P_S - Estratégica", 0.0, 1.0, 0.80)
        P_M = st.slider("P_M - Emocional", 0.0, 1.0, 0.55)
        FD = st.slider("FD - Triggering Factor (Crisis)", 0.0, 1.0, 0.45)
    with col2:
        C = st.slider("C - Causal", 0.0, 1.0, 0.75)
        I = st.slider("I - Identidad", 0.0, 1.0, 0.85)
        S = st.slider("S - Significancia", 0.0, 1.0, 0.90)
        A_V = st.slider("A_V - Validación externa", 0.0, 1.0, 0.70)
        B_R = st.slider("B_R - Tolerancia al riesgo", 0.0, 1.0, 0.75)
        B_E = st.slider("B_E - Sensibilidad emocional", 0.0, 1.0, 0.60)
        B_C = st.slider("B_C - Flexibilidad cognitiva", 0.0, 1.0, 0.80)

    if st.button("Calcular II(t)", type="primary"):
        P = [P_E, P_R, P_L, P_S, P_M]
        A_avg = (C + I + S + A_V) / 4
        B_avg = (B_R + B_E + B_C) / 3
        II = calcular_II(P, A_avg, B_avg, FD, t_days)

        st.success(f"**II(t) = {II}**")
        st.latex(r"II(t) = [1 - \prod (1 - P_i \times A_{avg} \times B_{avg} \times FD)] \times e^{-0.001 t}")

        if II < 0.50:
            st.success("✅ REVERSIBLE")
        elif II < 0.70:
            st.warning("⚠️ VENTANA CRÍTICA")
        else:
            st.error("🔴 LOCK-IN ALTO")

st.caption("SMA-03 v3 • Uberlandis Fiol Reyes • Marzo 2026 • Ready for Peer Review")
