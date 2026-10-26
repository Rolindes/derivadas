import streamlit as st
import random
import json
import os

# Configuración de la página
st.set_page_config(page_title="Derivative Arcade", page_icon="⚡", layout="centered")

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

# Estado del Minijuego Comecocos (Cálculo de pendientes)
if "pac_game" not in st.session_state:
    st.session_state.pac_game = {
        "lives": 3,
        "level": 1,
        "func_text": "x²",
        "x_point": 2,
        "correct_val": 4,
        "options": [4, 2, 8, 1]
    }

def reset_pacman_slope_round():
    # Banco de retos de cálculo de pendiente en un punto
    challenges = [
        ("x²", 2, 4, [4, 2, 8, 1]),
        ("x³", 1, 3, [3, 1, 6, 9]),
        ("2x²", 3, 12, [12, 6, 9, 4]),
        ("x³ - 3x", 2, 9, [9, 3, 6, 12]),
        ("5x", 4, 5, [5, 20, 10, 1])
    ]
    f_text, x_pt, correct, opts = random.choice(challenges)
    random.shuffle(opts)
    st.session_state.pac_game["func_text"] = f_text
    st.session_state.pac_game["x_point"] = x_pt
    st.session_state.pac_game["correct_val"] = correct
    st.session_state.pac_game["options"] = opts

# ================= PANTALLA 0: APODO =================
if st.session_state.current_user is None:
    st.markdown("## 🕹️ DERIVATIVE ARCADE PRO")
    st.write("Introduce tu apodo para entrar al salón recreativo de matemáticas:")
    nickname = st.text_input("Tu apodo:")
    
    if st.button("🚀 ¡Insert Coin (Empezar)!", use_container_width=True):
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
        st.markdown(f"👤 `{st.session_state.current_user}`")
        if st.button("🔄 Cambiar"):
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
        st.markdown("## 🗺️ Salón Recreativo - Mapa de Mundos")
        worlds = [
            (1, "Fase 1: 🟡 Comecocos - Come la Pendiente Exacta"),
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
        st.markdown(f"## 🕹️ Arcade - Fase 0{b}")
        if st.button("⬅️ Volver al Mapa"):
            st.session_state.screen = "map"
            st.rerun()
        st.markdown("---")

        # MUNDO 1: COMECOCOS CÁLCULO DE PENDIENTE
        if b == 1:
            st.subheader("🟡 Minijuego: Come la Pendiente Exacta")
            
            lives_display = "❤️" * st.session_state.pac_game["lives"] + "🖤" * (3 - st.session_state.pac_game["lives"])
            col_l1, col_l2 = st.columns([2, 2])
            col_l1.markdown(f"### Vidas: {lives_display}")
            col_l2.markdown(f"### Nivel: {st.session_state.pac_game['level']}")
            
            st.markdown(f"""
            <div style="background-color:#1e1b4b; padding:20px; border-radius:15px; border:2px dashed #fbbf24; text-align:center;">
                <h3 style="color:#f8fafc; margin:0;">🟡 ¡PAC-DERIVATIVE EN EL LABERINTO!</h3>
                <p style="color:#38bdf8; font-size:18px; margin:10px 0;">Calcula la pendiente de <b>f(x) = {st.session_state.pac_game['func_text']}</b> en el punto <b>x = {st.session_state.pac_game['x_point']}</b></p>
                <p style="color:#94a3b8; font-size:14px;">¡Cómete la pastilla numérica correcta y evita a los fantasmas!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            opts = st.session_state.pac_game["options"]
            c1, c2 = st.columns(2)
            
            for i, opt in enumerate(opts):
                target_col = c1 if i % 2 == 0 else c2
                with target_col:
                    if st.button(f"👻 Pasillo {i+1}:  [ {opt} ]", key=f"pac_opt_{i}", use_container_width=True):
                        if opt == st.session_state.pac_game["correct_val"]:
                            st.success("🎉 ¡WAKA WAKA! ¡Te comiste la pendiente exacta! +200 PTS")
                            u_data["score"] += 200
                            u_data["streak"] += 1
                            u_data["corrects"] += 1
                            st.session_state.pac_game["level"] += 1
                            if u_data["unlocked"] < 2:
                                u_data["unlocked"] = 2
                            save_users(st.session_state.users)
                            reset_pacman_slope_round()
                            st.rerun()
                        else:
                            st.session_state.pac_game["lives"] -= 1
                            u_data["streak"] = 0
                            u_data["errors"] += 1
                            save_users(st.session_state.users)
                            
                            if st.session_state.pac_game["lives"] <= 0:
                                st.error("💀 ¡GAME OVER! Te cazaron los fantasmas del error.")
                                st.session_state.pac_game["lives"] = 3
                                st.session_state.screen = "map"
                                st.rerun()
                            else:
                                st.error(f"❌ ¡BITE! Esa no era la pendiente. Vidas restantes: {st.session_state.pac_game['lives']}")

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
        st.markdown(f"## 📊 Informe Arcade de `{st.session_state.current_user}`")
        col1, col2, col3 = st.columns(3)
        col1.metric("Puntuación Total", f"{u_data['score']} PTS")
        col2.metric("Aciertos", u_data["corrects"])
        col3.metric("Fallos", u_data["errors"])
        st.markdown("---")
        if u_data["errors"] == 0:
            st.success("🌟 ¡Puntuación perfecta en el salón recreativo! Listo para la EBAU.")
        else:
            st.warning(f"⚠️ Has tenido {u_data['errors']} fallos. ¡Vuelve a insertar moneda y mejora tu récord!")
            
        if st.button("🗺️ Volver al Mapa", use_container_width=True):
            st.session_state.screen = "map"
            st.rerun()
