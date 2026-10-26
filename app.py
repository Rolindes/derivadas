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

# Estado seguro de la carrera de F1 (5 carriles, 7 vueltas, posición de carril)
if "f1_game" not in st.session_state:
    st.session_state.f1_game = {
        "lap": 1,
        "max_laps": 7,
        "lives": 3,
        "speed": 180,
        "car_lane": 2,
        "func_text": "x²",
        "x_point": 3,
        "correct_ans": 6,
        "options": [2, 4, 6, 9, 12]
    }
else:
    # Asegurar que si la sesión ya existía, tenga todas las claves necesarias
    if "car_lane" not in st.session_state.f1_game:
        st.session_state.f1_game["car_lane"] = 2
    if "lap" not in st.session_state.f1_game:
        st.session_state.f1_game["lap"] = 1
    if "lives" not in st.session_state:
        st.session_state.f1_game["lives"] = 3

def generate_f1_5lanes_challenge():
    pool = [
        ("x²", 3, 6, [2, 4, 6, 9, 12]),
        ("x³", 2, 12, [4, 6, 8, 12, 16]),
        ("5x", 4, 5, [0, 5, 10, 20, 25]),
        ("x³ - 3x", 2, 9, [3, 6, 9, 12, 15]),
        ("sin(x)", 0, 1, [-2, -1, 0, 1, 2]),
        ("2x² + 1", 3, 12, [6, 9, 12, 18, 24]),
        ("x⁴", 1, 4, [1, 2, 3, 4, 8])
    ]
    lap_idx = (st.session_state.f1_game["lap"] - 1) % len(pool)
    f_txt, x_pt, corr, opts = pool[lap_idx]
    random.shuffle(opts)
    st.session_state.f1_game["func_text"] = f_txt
    st.session_state.f1_game["x_point"] = x_pt
    st.session_state.f1_game["correct_ans"] = corr
    st.session_state.f1_game["options"] = opts
    st.session_state.f1_game["car_lane"] = 2

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
                if st.button(f"🎮 Jugar -> {wname}", key=f"w_{wid}", use_container_width=True):
                    st.session_state.active_block = wid
                    st.session_state.screen = "game"
                    if wid == 1:
                        generate_f1_5lanes_challenge()
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
            st.subheader("🏎️ Gran Premio F1: Conducción en Pista de 5 Carriles")
            
            lives_display = "❤️" * st.session_state.f1_game["lives"] + "🖤" * (3 - st.session_state.f1_game["lives"])
            c_t1, c_t2, c_t3 = st.columns(3)
            c_t1.markdown(f"### 🛡️ Vidas: {lives_display}")
            c_t2.markdown(f"### 🔄 Vuelta: {st.session_state.f1_game['lap']} / 7")
            c_t3.markdown(f"### ⚡ Velocidad: {st.session_state.f1_game['speed']} km/h")
            
            f1_box = f"""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 25px; border-radius: 20px; border: 3px solid #38bdf8; text-align: center; box-shadow: 0 0 25px rgba(56,189,248,0.3);">
                <span style="background-color: #38bdf8; color: #020617; padding: 5px 15px; border-radius: 20px; font-weight: 900; font-size: 14px;">🏁 ZONA DE CÁLCULO DE PISTA</span>
                <h2 style="color: #f43f5e; margin: 15px 0 5px 0; font-size: 32px;">Calcula la derivada: f'( {st.session_state.f1_game['x_point']} )</h2>
                <p style="color: #fbbf24; font-size: 26px; font-weight: 900; margin: 0;">Función: f(x) = {st.session_state.f1_game['func_text']}</p>
                <p style="color: #94a3b8; font-size: 14px; margin-top: 10px;">Usa los botones de dirección o haz clic directamente en el carril correcto.</p>
            </div>
            """
            st.markdown(f1_box, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Controles de movimiento lateral (Izquierda / Derecha)
            col_mv1, col_mv2, col_mv3 = st.columns([1, 2, 1])
            with col_mv1:
                if st.button("⬅️ Mover Izquierda", use_container_width=True):
                    if st.session_state.f1_game["car_lane"] > 0:
                        st.session_state.f1_game["car_lane"] -= 1
                        st.rerun()
            with col_mv3:
                if st.button("Mover Derecha ➡️", use_container_width=True):
                    if st.session_state.f1_game["car_lane"] < 4:
                        st.session_state.f1_game["car_lane"] += 1
                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # Renderizar los 5 carriles visuales
            opts = st.session_state.f1_game["options"]
            c1, c2, c3, c4, c5 = st.columns(5)
            lanes_ui = [c1, c2, c3, c4, c5]
            
            current_car_pos = st.session_state.f1_game["car_lane"]

            for i, col in enumerate(lanes_ui):
                val = opts[i]
                with col:
                    is_here = (i == current_car_pos)
                    label = f"🏎️ **[TÚ]**\n\n**[ {val} ]**" if is_here else f"Carril {i+1}\n\n**[ {val} ]**"
                    
                    if st.button(label, key=f"lane_btn_{i}", use_container_width=True):
                        st.session_state.f1_game["car_lane"] = i
                        
                        if val == st.session_state.f1_game["correct_ans"]:
                            st.session_state.f1_game["speed"] += 20
                            u_data["score"] += 200
                            u_data["streak"] += 1
                            u_data["corrects"] += 1
                            
                            if st.session_state.f1_game["lap"] < 7:
                                st.success(f"🎉 ¡Excelente! Vuelta {st.session_state.f1_game['lap']} / 7 superada.")
                                st.session_state.f1_game["lap"] += 1
                                generate_f1_5lanes_challenge()
                            else:
                                st.success("🏆 ¡BANDERA A CUADROS! ¡Has ganado el Gran Premio completo de 7 vueltas!")
                                u_data["unlocked"] = 2
                                st.session_state.screen = "map"
                            
                            save_users(st.session_state.users)
                            st.rerun()
                        else:
                            st.session_state.f1_game["lives"] -= 1
                            u_data["streak"] = 0
                            u_data["errors"] += 1
                            save_users(st.session_state.users)
                            
                            if st.session_state.f1_game["lives"] <= 0:
                                st.error("💥 ¡CRASH! Te has quedado sin vidas. Reiniciando carrera.")
                                st.session_state.f1_game["lives"] = 3
                                st.session_state.f1_game["lap"] = 1
                                st.session_state.screen = "map"
                                st.rerun()
                            else:
                                st.error(f"❌ ¡Impacto en el muro! Te quedan {st.session_state.f1_game['lives']} vidas.")

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
        col3.metric("Accidentes", u_data["errors"])
        st.markdown("---")
        if u_data["errors"] == 0:
            st.success("🌟 ¡Pole Position impecable! Cero accidentes. ¡Listo para arrasar en la EBAU!")
        else:
            st.warning(f"⚠️ Has tenido {u_data['errors']} accidentes en pista. ¡Vuelve al circuito a entrenar!")
            
        if st.button("🗺️ Volver al Mapa", use_container_width=True):
            st.session_state.screen = "map"
            st.rerun()
