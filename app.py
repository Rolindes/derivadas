import streamlit as st
import random
import json
import os

# Configuración de la página
st.set_page_config(page_title="Derivative F1 Grand Prix", page_icon="🏎️", layout="centered")

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

# Estado del Minijuego de F1 (7 Retos de derivadas en un punto)
if "f1_game" not in st.session_state:
    st.session_state.f1_game = {
        "lap": 1,
        "max_laps": 7,
        "lives": 3,
        "speed": 180,
        "func_text": "x²",
        "x_point": 3,
        "correct_ans": 6,
        "options": [6, 4, 9]
    }

def generate_f1_challenge():
    # Banco de 7 retos de derivadas en un punto para la carrera de F1
    pool = [
        ("x²", 3, 6, [6, 4, 9]),
        ("x³", 2, 12, [12, 8, 6]),
        ("5x", 4, 5, [5, 20, 10]),
        ("x³ - 3x", 2, 9, [9, 6, 12]),
        ("sin(x)", 0, 1, [1, 0, -1]),
        ("2x² + 1", 3, 12, [12, 18, 9]),
        ("x⁴", 1, 4, [4, 1, 3])
    ]
    # Seleccionar según la vuelta actual (hasta 7)
    lap_idx = (st.session_state.f1_game["lap"] - 1) % len(pool)
    f_txt, x_pt, corr, opts = pool[lap_idx]
    random.shuffle(opts)
    st.session_state.f1_game["func_text"] = f_txt
    st.session_state.f1_game["x_point"] = x_pt
    st.session_state.f1_game["correct_ans"] = corr
    st.session_state.f1_game["options"] = opts

# ================= PANTALLA 0: APODO =================
if st.session_state.current_user is None:
    st.markdown("## 🏎️ DERIVATIVE F1 GRAND PRIX")
    st.write("Introduce tu apodo de piloto para entrar al mundial de cálculo:")
    nickname = st.text_input("Tu apodo de Piloto:")
    
    if st.button("🏁 ¡Arrancar Motor (Empezar)!", use_container_width=True):
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
            (1, "Fase 1: 🏎️ Gran Premio F1 (7 Vueltas de Derivadas en un Punto)"),
            (2, "Fase 2: 🎈 Fragua Polinómica"),
            (3, "Fase 3: 🎯 Bosque Trascendente"),
            (4, "Fase 4: 📦 Torre de Productos"),
            (5, "Fase 5: ⚔️ Jefe Final - Regla de la Cadena")
        ]
        
        for wid, wname in worlds:
            if wid <= u_data["unlocked"]:
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

        # MUNDO 1: CARRERA DE F1 (7 DERIVADAS EN UN PUNTO)
        if b == 1:
            st.subheader("🏎️ Gran Premio F1: Esquiva el Muro del Error")
            
            # Panel de telemetría del monoplaza
            lives_display = "❤️" * st.session_state.f1_game["lives"] + "🖤" * (3 - st.session_state.f1_game["lives"])
            c_t1, c_t2, c_t3 = st.columns(3)
            c_t1.markdown(f"### 🛡️ Vidas: {lives_display}")
            c_t2.markdown(f"### 🔄 Vuelta: {st.session_state.f1_game['lap']} / 7")
            c_t3.markdown(f"### ⚡ Velocidad: {st.session_state.f1_game['speed']} km/h")
            
            # Panel visual de la pista de F1 con HTML/CSS llamativo
            f1_track_html = f"""
            <div style="background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); padding: 25px; border-radius: 20px; border: 3px solid #f43f5e; text-align: center; box-shadow: 0 0 25px rgba(244,63,94,0.3);">
                <span style="background-color: #f43f5e; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px;">🏁 TELEMETRÍA DE CARRERA</span>
                <h2 style="color: #38bdf8; margin: 15px 0 5px 0; font-size: 26px;">Calcula: f'( {st.session_state.f1_game['x_point']} )</h2>
                <p style="color: #fbbf24; font-size: 22px; font-weight: 900; margin: 0;">Función en pista: f(x) = {st.session_state.f1_game['func_text']}</p>
                <hr style="border-color: #334155; margin: 15px 0;">
                <div style="display: flex; justify-content: space-around; align-items: center;">
                    <div style="background: #020617; padding: 10px 20px; border-radius: 10px; border: 1px solid #38bdf8;">🚗 <b>Coche F1 en pista</b></div>
                    <div style="color: #4ade80; font-weight: bold; font-size: 16px;">⚡ ¡Elige el carril con la pendiente exacta!</div>
                </div>
            </div>
            """
            st.markdown(f1_track_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 3 Carriles de la autopista (Botones con los valores de las opciones)
            opts = st.session_state.f1_game["options"]
            c_lane1, c_lane2, c_lane3 = st.columns(3)
            
            lanes = [("🏎️ Carril Izquierdo", c_lane1), ("🏎️ Carril Central", c_lane2), ("🏎️ Carril Derecho", c_lane3)]
            
            for i, (lane_name, col) in enumerate(lanes):
                opt_val = opts[i]
                with col:
                    if st.button(f"{lane_name}\n\n[ {opt_val} ]", key=f"f1_lane_{i}", use_container_width=True):
                        if opt_val == st.session_state.f1_game["correct_ans"]:
                            st.session_state.f1_game["speed"] += 30
                            u_data["score"] += 250
                            u_data["streak"] += 1
                            u_data["corrects"] += 1
                            
                            # Avanzar de vuelta
                            if st.session_state.f1_game["lap"] < 7:
                                st.success(f"🎉 ¡Adelantamiento perfecto! Has entrado en la Vuelta {st.session_state.f1_game['lap'] + 1} / 7.")
                                st.session_state.f1_game["lap"] += 1
                                generate_f1_challenge()
                            else:
                                st.success("🏆 ¡GRAN PRIX GANADO! Has completado las 7 vueltas de derivadas con éxito total.")
                                u_data["unlocked"] = 2
                                save_users(st.session_state.users)
                                st.session_state.screen = "map"
                            
                            save_users(st.session_state.users)
                            st.rerun()
                        else:
                            st.session_state.f1_game["lives"] -= 1
                            st.session_state.f1_game["speed"] = max(100, st.session_state.f1_game["speed"] - 40)
                            u_data["streak"] = 0
                            u_data["errors"] += 1
                            save_users(st.session_state.users)
                            
                            if st.session_state.f1_game["lives"] <= 0:
                                st.error("💥 ¡ACCIDENTE! Te has estrellado contra el muro del error. Fin de carrera.")
                                st.session_state.f1_game["lives"] = 3
                                st.session_state.f1_game["lap"] = 1
                                st.session_state.screen = "map"
                                st.rerun()
                            else:
                                st.error(f"❌ ¡CRASH! Carril incorrecto. Te quedan {st.session_state.f1_game['lives']} vidas.")

        # MUNDO 2: POLINOMIOS
        elif b == 2:
            st.subheader("Bloque 2: Fragua Polinómica")
            a, c_val = random.randint(2, 4), random.randint(1, 5)
            correct_ans = f"{2*a}x + {c_val}"
            options = [correct_ans, f"{a}x + {c_val}", f"{2*a}x²", f"{c_val}x"]
            random.shuffle(options)
            
            st.markdown(f"### f(x) = {a}x² + {c_val}x")
            for i, opt in enumerate(options):
                if st.button(f"🎈 {opt}", key=f"p_opt_{i}", use_container_width=True):
                    if opt == correct_ans:
                        st.success("¡Correcto! +150 PTS")
                        u_data["score"] += 150
                        u_data["streak"] += 1
                        u_data["corrects"] += 1
                        if u_data["unlocked"] < 3: u_data["unlocked"] = 3
                        save_users(st.session_state.users)
                        st.rerun()
                    else:
                        st.error("¡Incorrecto!")
                        u_data["streak"] = 0
                        u_data["errors"] += 1
                        save_users(st.session_state.users)

        # MUNDO 3: TRASCENDENTES
        elif b == 3:
            st.subheader("Bloque 3: Bosque Trascendente")
            st.markdown("### f(x) = 4sin(x)")
            correct_t = "4cos(x)"
            t_opts = ["4cos(x)", "-4sin(x)", "4sin(x)", "-4cos(x)"]
            random.shuffle(t_opts)
            for i, opt in enumerate(t_opts):
                if st.button(f"🎯 {opt}", key=f"t_opt_{i}", use_container_width=True):
                    if opt == correct_t:
                        st.success("¡Correcto! +200 PTS")
                        u_data["score"] += 200
                        u_data["streak"] += 1
                        u_data["corrects"] += 1
                        if u_data["unlocked"] < 4: u_data["unlocked"] = 4
                        save_users(st.session_state.users)
                        st.rerun()
                    else:
                        st.error("¡Incorrecto!")
                        u_data["streak"] = 0
                        u_data["errors"] += 1
                        save_users(st.session_state.users)

        # MUNDO 4: PRODUCTOS
        elif b == 4:
            st.subheader("Bloque 4: Torre de Productos")
            st.markdown("### f(x) = x² · sin(x)")
            correct_pr = "2x·sin(x) + x²·cos(x)"
            pr_opts = [correct_pr, "2x·cos(x)", "x²·sin(x)", "2x·sin(x) - x²·cos(x)"]
            random.shuffle(pr_opts)
            for i, opt in enumerate(pr_opts):
                if st.button(f"📦 {opt}", key=f"pr_opt_{i}", use_container_width=True):
                    if opt == correct_pr:
                        st.success("¡Correcto! +250 PTS")
                        u_data["score"] += 250
                        u_data["streak"] += 1
                        u_data["corrects"] += 1
                        if u_data["unlocked"] < 5: u_data["unlocked"] = 5
                        save_users(st.session_state.users)
                        st.rerun()
                    else:
                        st.error("¡Incorrecto!")
                        u_data["streak"] = 0
                        u_data["errors"] += 1
                        save_users(st.session_state.users)

        # MUNDO 5: REGLA DE LA CADENA
        elif b == 5:
            st.subheader("Bloque 5: Jefe Final - Regla de la Cadena")
            st.markdown("### f(x) = sin(4x²)")
            correct_c = "cos(4x²) · (8x)"
            c_opts = [correct_c, "cos(4x²)", "-sin(4x²) · 8x", "8x·sin(4x²)"]
            random.shuffle(c_opts)
            for i, opt in enumerate(c_opts):
                if st.button(f"⚔️ {opt}", key=f"c_opt_{i}", use_container_width=True):
                    if opt == correct_c:
                        st.success("🎉 ¡VICTORIA! ¡Jefe derrotado! +500 PTS")
                        u_data["score"] += 500
                        u_data["streak"] += 1
                        u_data["corrects"] += 1
                        save_users(st.session_state.users)
                        st.rerun()
                    else:
                        st.error("¡Ataque bloqueado!")
                        u_data["streak"] = 0
                        u_data["errors"] += 1
                        save_users(st.session_state.users)

    # ================= PANTALLA 3: INFORME =================
    elif st.session_state.screen == "summary":
        st.markdown(f"## 📊 Informe de Piloto de `{st.session_state.current_user}`")
        col1, col2, col3 = st.columns(3)
        col1.metric("Puntuación Total", f"{u_data['score']} PTS")
        col2.metric("Aciertos en Pista", u_data["corrects"])
        col3.metric("Accidentes (Fallos)", u_data["errors"])
        st.markdown("---")
        if u_data["errors"] == 0:
            st.success("🌟 ¡Pole Position impecable! Cero accidentes. ¡Listo para arrasar en la EBAU!")
        else:
            st.warning(f"⚠️ Has tenido {u_data['errors']} accidentes en pista. ¡Vuelve al circuito a entrenar los reflejos!")
            
        if st.button("🗺️ Volver al Mapa", use_container_width=True):
            st.session_state.screen = "map"
            st.rerun()
