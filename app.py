import streamlit as st
import random
import json
import os
import numpy as np

st.set_page_config(page_title="Derivative Arcade Universe", page_icon="🏎️", layout="centered")

DATA_FILE = "users_progress.json"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_users(users_data):
    with open(DATA_FILE, "w") as f:
        json.dump(users_data, f)

if "users" not in st.session_state: st.session_state.users = load_users()
if "current_user" not in st.session_state: st.session_state.current_user = None
if "screen" not in st.session_state: st.session_state.screen = "login"
if "active_block" not in st.session_state: st.session_state.active_block = 1

# ================= PANTALLA 0: APODO =================
if st.session_state.current_user is None:
    st.markdown("## 🏎️ DERIVATIVE ARCADE UNIVERSE")
    st.write("Introduce tu apodo de piloto:")
    nickname = st.text_input("Tu apodo:")
    if st.button("🏁 ¡Arrancar Motor!", use_container_width=True):
        if nickname.strip() != "":
            clean_name = nickname.strip()
            st.session_state.current_user = clean_name
            if clean_name not in st.session_state.users:
                st.session_state.users[clean_name] = {"score": 0, "streak": 0, "corrects": 0, "errors": 0}
                save_users(st.session_state.users)
            st.session_state.screen = "map"
            st.rerun()
else:
    u_data = st.session_state.users[st.session_state.current_user]

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"🏎️ Piloto: `{st.session_state.current_user}`")
        if st.button("🔄 Cambiar"):
            st.session_state.current_user = None
            st.session_state.screen = "login"
            st.rerun()
    with col2: st.metric("🔥 Racha", u_data["streak"])
    with col3: st.metric("🏆 Pts", u_data["score"])
    with col4:
        if st.button("📊 Informe"):
            st.session_state.screen = "summary"
            st.rerun()

    st.markdown("---")

    # ================= MAPA DE MUNDOS Y EXPLICACIÓN INICIAL CON SLIDER =================
    if st.session_state.screen == "map":
        st.markdown("## 🗺️ Fase 0: Menú Principal y Explicación de la Derivada")
        st.markdown("### 📈 La Derivada como la Pendiente de la Recta Tangente ($m = f'(x)$)")
        st.write("Antes de entrar a la pista, visualiza cómo la derivada en un punto es exactamente la pendiente de la recta tangente usando el siguiente simulador:")

        # Simulador interactivo al principio con Selectbox y Slider
        func_choice = st.selectbox("Elige una función f(x):", ["x²", "x³", "sin(x)", "eˣ"])
        x_val = st.slider("Mueve el punto x en la curva:", -3.0, 3.0, 1.0, 0.1)

        # Cálculo matemático de la función, valor y derivada (pendiente m)
        if func_choice == "x²":
            y_val = x_val ** 2
            deriv_val = 2 * x_val
            func_name_str = f"f(x) = x²"
        elif func_choice == "x³":
            y_val = x_val ** 3
            deriv_val = 3 * (x_val ** 2)
            func_name_str = f"f(x) = x³"
        elif func_choice == "sin(x)":
            y_val = float(np.sin(x_val))
            deriv_val = float(np.cos(x_val))
            func_name_str = f"f(x) = sin(x)"
        else: # eˣ
            y_val = float(np.exp(x_val))
            deriv_val = float(np.exp(x_val))
            func_name_str = f"f(x) = eˣ"

        st.info(f"📊 **Función seleccionada:** `{func_name_str}`  \n📍 **Punto x:** `{x_val:.2f}` | **y:** `{y_val:.2f}`  \n🎯 **Pendiente de la recta tangente ($m = f'(x)$):** `{deriv_val:.2f}`")

        st.markdown("---")
        st.write("Selecciona una fase arcade para poner a prueba tus reflejos con 10 funciones:")
        
        worlds = [
            (1, "Fase 1: 🏎️ Gran Premio F1 (Autopista Arcade)"),
            (2, "Fase 2: 🎈 Fragua Polinómica (Cinta de Globos Neutros)"),
            (3, "Fase 3: 🎾 Tenis Trascendente (Juego de Pala y Rebote)"),
            (4, "Fase 4: 🧱 Tetris de Productos (Piezas Geométricas)"),
            (5, "Fase 5: ⚔️ Jefe Final Regla de la Cadena (Combate de 10 Oleadas)")
        ]
        
        for wid, wname in worlds:
            if st.button(f"🎮 Jugar -> {wname}", key=f"w_{wid}", use_container_width=True):
                st.session_state.active_block = wid
                st.session_state.screen = "game"
                st.rerun()

        st.markdown("---")
        if st.button("📊 Ver Informe Final", use_container_width=True):
            st.session_state.screen = "summary"
            st.rerun()

    # ================= ZONA DE JUEGO ARCADE =================
    elif st.session_state.screen == "game":
        b = st.session_state.active_block
        st.markdown(f"## 🏁 Circuito Activo - Fase 0{b}")
        if st.button("⬅️ Volver al Menú Principal (Fase 0)"):
            st.session_state.screen = "map"
            st.rerun()
        st.markdown("---")

        # -------------------------------------------------------------
        # MUNDO 1: F1 ARCADE (10 FUNCIONES)
        # -------------------------------------------------------------
        if b == 1:
            st.subheader("🏎️ Fase 1: Gran Premio F1 (10 Funciones)")
            st.markdown("Calcula la derivada y esquiva los muros incorrectos.")

            f1_code = """
            <!DOCTYPE html>
            <html>
            <head><style>
              body { background: #020617; color: white; text-align: center; font-family: sans-serif; margin: 0; }
              canvas { background: #0f172a; border: 3px solid #38bdf8; border-radius: 10px; display: block; margin: 0 auto; cursor: pointer; }
              .btn { background: #2563eb; color: white; border: none; padding: 10px 16px; font-size: 15px; border-radius: 8px; cursor: pointer; font-weight: bold; margin: 3px; }
            </style></head>
            <body>
              <div style="font-size: 14px; color: #fbbf24; font-weight: bold; margin-bottom: 4px;">Función: <span id="l">1</span>/10 | Pts: <span id="s">0</span></div>
              <div style="background: #1e293b; border: 2px solid #38bdf8; border-radius: 8px; padding: 6px; width: 420px; margin: 0 auto 6px auto;">
                <div style="color: #38bdf8; font-size: 12px; font-weight: bold;" id="ft">f(x) = x² | x = 3</div>
                <div style="color: #f43f5e; font-size: 13px; font-weight: bold;" id="qt">Calcula f'(3)</div>
              </div>
              <canvas id="c" width="450" height="240"></canvas>
              <div style="margin-top: 8px;">
                <button class="btn" onclick="lane=Math.max(0,lane-1)">⬅️ Izq</button>
                <button class="btn" onclick="lane=0">C1</button>
                <button class="btn" onclick="lane=1">C2</button>
                <button class="btn" onclick="lane=2">C3</button>
                <button class="btn" onclick="lane=3">C4</button>
                <button class="btn" onclick="lane=4">C5</button>
                <button class="btn" onclick="lane=Math.min(4,lane+1)">Der ➡️</button>
              </div>
            <script>
              const canvas = document.getElementById("c");
              const ctx = canvas.getContext("2d");
              const lanes = [45, 135, 225, 315, 405];
              let lane = 2, oy = -100, step = 1, pts = 0, offset = 0;
              const questions = [
                { f: "x²", x: 3, corr: "6", opts: ["2", "4", "6", "9", "12"] },
                { f: "x³", x: 2, corr: "12", opts: ["4", "8", "12", "16", "6"] },
                { f: "5x", x: 4, corr: "5", opts: ["20", "10", "5", "25", "0"] },
                { f: "x³ - 3x", x: 2, corr: "9", opts: ["3", "6", "9", "12", "15"] },
                { f: "sin(x)", x: 0, corr: "1", opts: ["-1", "0", "1", "2", "-2"] },
                { f: "2x² + 1", x: 3, corr: "12", opts: ["6", "12", "18", "24", "9"] },
                { f: "x⁴", x: 1, corr: "4", opts: ["1", "2", "3", "4", "8"] },
                { f: "ln(x)", x: 1, corr: "1", opts: ["0", "1", "e", "1/2", "2"] },
                { f: "eˣ", x: 0, corr: "1", opts: ["0", "1", "e", "e²", "inf"] },
                { f: "cos(x)", x: 0, corr: "0", opts: ["-1", "0", "1", "pi", "2"] }
              ];
              let q = questions[0];
              function updateUI() {
                document.getElementById("l").innerText = step;
                document.getElementById("s").innerText =
