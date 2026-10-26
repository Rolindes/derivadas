import streamlit as st
import random
import json
import os

# Configuración de la página
st.set_page_config(page_title="Derivative F1 5-Lanes Grand Prix", page_icon="🏎️", layout="centered")

DATA_FILE = "users_progress.json"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_users(users_data):
    with open(DATA_FILE, "w") as f:
        json.dump(users_data, f)

if "users" not in st.session_state:
    st.session_state.users = load_users()

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "screen" not in st.session_state:
    st.session_state.screen = "login"

if "active_block" not in st.session_state:
    st.session_state.active_block = 1

# Estado de la carrera de F1 (5 carriles, 7 vueltas)
if "f1_game" not in st.session_state:
    st.session_state.f1_game = {
        "lap": 1,
        "max_laps": 7,
        "lives": 3,
        "speed": 180,
        "func_text": "x²",
        "x_point": 3,
        "correct_ans": 6,
        "options": [6, 2, 9, 4, 12]
    }

def generate_f1_5lanes_challenge():
    # Banco de 7 retos con 1 respuesta correcta y 4 distractores para los 5 carriles
    pool = [
        ("x²", 3, 6, [6, 2, 9, 4, 12]),
        ("x³", 2, 12, [12, 8, 6, 4, 16]),
        ("5x", 4, 5, [5, 20, 10, 25, 0]),
        ("x³ - 3x", 2, 9, [9, 6, 12, 3, 15]),
        ("sin(x)", 0, 1, [1, 0, -1, 2, -2]),
        ("2x² + 1", 3, 12, [12, 18, 9, 6, 24]),
        ("x⁴", 1, 4, [4, 1, 3, 2, 8])
    ]
    lap_idx = (st.session_state.f1_game["lap"] - 1) % len(pool)
    f_txt, x_pt, corr, opts = pool[lap_idx]
    random.shuffle(opts)
    st.session_state.f1_game["func_text"] = f_txt
    st.session_state.f1_game["x_point"] = x_pt
    st.session_state.f1_game["correct_ans"] = corr
    st.session_state.f1_game["options"] = opts

# ================= PANTALLA 0: APODO =================
if st.session_state.current_user is None:
    st.markdown("## 🏎️ F1 5-LANES GRAND PRIX")
    st.write("Introduce tu apodo de piloto para entrar a la parrilla de salida:")
    nickname = st.text_input("Tu apodo de Piloto:")
    
    if st.button("🏁 ¡Ocupar la Pole Position!", use_container_width=True):
        if nickname.strip() == "":
            st.warning("Escribe un apodo válido.")
        else:
            clean_name = nickname.strip()
            st.session_state.current_user = clean_name
            if clean_name not in st.session_state.users:
                st.session_state.users[clean_name] = {"score": 0, "streak": 0, "corrects": 0, "errors": 0, "unlocked": 1}
                save_users(st.session_state.users)
            st.session_state.screen = "map"
            st.rerun()

else:
    u_data = st.session_state.users[st.session_state.current_user]

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"🏎️ Piloto: `{st.session_state.current_user}`")
        if st.button("🔄 Cambiar Piloto"):
            st.session_state.current_user = None
            st.session_state.screen = "login"
            st.rerun()
    with col2:
        st.metric("🔥 Racha", u_data["streak"])
    with col3:
        st.metric("🏆 Pts", u_data["score"])
    with col4:
        if st.button("📊 Informe"):
            st.session_state.screen = "summary"
            st.rerun()

    st.markdown("---")

    # ================= MAPA DE MUNDOS =================
    if st.session_state.screen == "map":
        st.markdown("## 🗺️ Circuito Mundial - Mapa de Fases")
        worlds = [
            (1, "Fase 1: 🏎️ Gran Premio F1 (5 Carriles - 7 Vueltas de Derivadas)"),
            (2, "Fase 2: 🎈 Fragua Polinómica"),
            (3, "Fase 3: 🎯 Bosque Trascendente"),
            (4, "Fase 4: 📦 Torre de Productos"),
            (5, "Fase 5: ⚔️ Jefe Final - Regla de la Cadena")
        ]
        
        for wid, wname in worlds:
            if wid <= u_data["unlocked"]:
                if wid == 1:
                    if st.button(f"🎮 Jugar -> {wname}", key=f"w_{wid}", use_container_width=True):
                        st.session_state.active_block = wid
                        st.session_state.screen = "game"
                        generate_f1_5lanes_challenge()
                        st.rerun()
                else:
                    if st.button(f"🎮 Jugar -> {wname}", key=f"w_{wid}", use_container_width=True):
                        st.session_state.active_block = wid
                        st.session_state.screen = "game"
                        st.rerun()
            else:
                st.button(f"🔒 {wname} (Bloqueado)", key=f"w_{wid}", disabled=True, use_container_width=True)

        st.markdown("---")
        if st.button("📊 Ver Informe Final", use_container_width=True):
            st.session_state.screen = "summary"
            st.rerun()

    # ================= ZONA DE JUEGO =================
    elif st.session_state.screen == "game":
        b = st.session_state.active_block
        st.markdown(f"## 🏁 Circuito Activo - Fase 0{b}")
        if st.button("⬅️ Volver al Mapa"):
            st.session_state.screen = "map"
            st.rerun()
        st.markdown("---")

        # MUNDO 1: CARRERA DE F1 CON 5 CARRILES Y 7 VUELTAS
        if b == 1:
            st.subheader("🏎️ Gran Premio F1: Elije el Carril Correcto")
            
            # Panel de telemetría de carrera
            lives_display = "❤️" * st.session_state.f1_game["lives"] + "🖤" * (3 - st.session_state.f1_game["lives"])
            c_t1, c_t2, c_t3 = st.columns(3)
            c_t1.markdown(f"### 🛡️ Vidas: {lives_display}")
            c_t2.markdown(f"### 🔄 Vuelta: {st.session_state.f1_game['lap']} / 7")
            c_t3.markdown(f"### ⚡ Velocidad: {st.session_state.f1_game['speed']} km/h")
            
            # Panel visual claro con la función y el punto a calcular
            f1_box = f"""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 25px; border-radius: 20px; border: 3px solid #38bdf8; text-align: center; box-shadow: 0 0 25px rgba(56,189,248,0.3);">
                <span style="background-color: #38bdf8; color: #020617; padding: 5px 15px; border-radius: 20px; font-weight: 900; font-size: 14px;">🏁 ZONA DE CÁLCULO DE PISTA</span>
                <h2 style="color: #f43f5e; margin: 15px 0 5px 0; font-size: 32px;">Calcula la derivada: f'( {st.session_state.f1_game['x_point']} )</h2>
                <p style="color: #fbbf24; font-size: 26px; font-weight: 900; margin: 0;">Función: f(x) = {st.session_state.f1_game['func_text']}</p>
                <p style="color: #94a3b8; font-size: 14px; margin-top: 10px;">Piensa con calma tu resultado y muévete al carril correspondiente abajo.</p>
            </div>
            """
            st.markdown(f1_box, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 5 CARRILES (5 Botones distribuidos equitativamente en columnas)
            opts = st.session_state.f1_game["options"]
            c1, c2, c3, c4, c5 = st.columns(5)
            lanes_ui = [("🚗 Carril 1", c1), ("🚗 Carril 2", c2), ("🚗 Carril 3", c3), ("🚗 Carril 4", c4), ("🚗 Carril 5", c5)]
            
            for i, (lane_title, col) in enumerate(lanes_ui):
                val = opts[i]
                with col:
                    if st.button(f"{lane_title}\n\n**[ {val} ]**", key=f"lane_{i}", use_container_width=True):
                        if val == st.session_state.f1_game["correct_ans"]:
                            st.session_state.f1_game["speed"] += 20
                            u_data["score"] += 200
                            u_data["streak"] += 1
                            u_data["corrects"] += 1
                            
                            if st.session_state.f1_game["lap"] < 7:
                                st.success(f"🎉 ¡Increíble! Has superado la Vuelta {st.session_state.f1_game['lap']} / 7.")
                                st.session_state.f1_game["lap"] += 1
                                generate_f1_5lanes_challenge()
                            else:
                                st.success("🏆 ¡BANDERA A CUADROS! ¡Has ganado el Gran Premio completo de 7 vueltas con éxito!")
                                u_data["unlocked"] = 2
                                st.session_state.screen = "map"
                            
                            save_users(st.session_state.users)
                            st.rerun()
                        else:
                            st.session_state.f1_game["lives"] -= 1
                            st.session_state.f1_game["speed"] = max(100, st.session_state.f1_game["speed"] - 30)
                            u_data["streak"] = 0
                            u_data["errors"] += 1
                            save_users(st.session_state.users)
                            
                            if st.session_state.f1_game["lives"] <= 0:
                                st.error("💥 ¡ACCIDENTE TOTAL! Te has estrellado contra el muro del error. Reiniciando carrera.")
                                st.session_state.f1_game["lives"] = 3
                                st.session_state.f1_game["lap"] = 1
                                st.session_state.screen = "map"
                                st.rerun()
                            else:
