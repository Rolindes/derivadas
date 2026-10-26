import streamlit as st
import random
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Derivative Adventure", page_icon="⚡", layout="centered")

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

# ================= PANTALLA 0: IDENTIFICACIÓN POR APODO =================
if st.session_state.current_user is None:
    st.markdown("## ⚡ DERIVATIVE ADVENTURE")
    st.write("Introduce tu apodo o nombre para empezar a jugar. ¡Sin registros ni correos!")
    
    nickname = st.text_input("Tu apodo / nombre de usuario:")
    
    if st.button("🚀 ¡Entrar a Jugar!", use_container_width=True):
        if nickname.strip() == "":
            st.warning("Por favor, escribe un apodo válido para continuar.")
        else:
            clean_name = nickname.strip()
            st.session_state.current_user = clean_name
            
            if clean_name not in st.session_state.users:
                st.session_state.users[clean_name] = {
                    "score": 0, "streak": 0, "corrects": 0, "errors": 0, "unlocked": 1
                }
                save_users(st.session_state.users)
                
            st.session_state.screen = "map"
            st.rerun()

else:
    u_data = st.session_state.users[st.session_state.current_user]

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"👤 **Jugador:** `{st.session_state.current_user}`")
        if st.button("🔄 Cambiar usuario"):
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
        st.markdown("## 🗺️ Mapa de Avance de Mundos")
        st.write("Selecciona una fase disponible para jugar y practicar derivadas:")
        
        worlds = [
            (1, "Fase 1: Tangentes y Pendientes (Elige tu función y Francotirador)"),
            (2, "Fase 2: Fragua Polinómica (Minijuego de Globos)"),
            (3, "Fase 3: Bosque Trascendente (Disparo Láser)"),
            (4, "Fase 4: Torre de Productos y Cocientes"),
            (5, "Fase 5: Jefe Final - Regla de la Cadena")
        ]
        
        for wid, wname in worlds:
            is_unlocked = wid <= u_data["unlocked"]
            if is_unlocked:
                if st.button(f"🎮 Jugar -> {wname}", key=f"world_btn_{wid}", use_container_width=True):
                    st.session_state.active_block = wid
                    st.session_state.screen = "game"
                    st.rerun()
            else:
                st.button(f"🔒 {wname} (Bloqueado)", key=f"world_btn_{wid}", disabled=True, use_container_width=True)

        st.markdown("---")
        if st.button("📊 Ver Informe de Rendimiento Final", use_container_width=True):
            st.session_state.screen = "summary"
            st.rerun()

    # ================= ZONA DE JUEGO =================
    elif st.session_state.screen == "game":
        b = st.session_state.active_block
        st.markdown(f"## 🚀 Mundo Activo: Fase 0{b}")
        
        if st.button("⬅️ Volver al Mapa de Mundos"):
            st.session_state.screen = "map"
            st.rerun()
            
        st.markdown("---")

        # MUNDO 1: TANGENTES CON FUNCIÓN PERSONALIZADA
        if b == 1:
            st.subheader("Bloque 1: El Significado de la Derivada")
            tab1, tab2 = st.tabs(["💡 Laboratorio Libre (Elige tu función)", "🎯 Minijuego Francotirador"])
            
            with tab1:
                st.write("Escribe la función que quieras investigar (ejemplos: `x**3 - 3*x`, `x**2 - 4`, `sin(x)`):")
                user_func_str = st.text_input("Función f(x):", value="x**3 - 3*x")
                
                try:
                    x = sp.Symbol('x')
                    f_expr = sp.sympify(user_func_str)
                    f_prime_expr = sp.diff(f_expr, x)
                    
                    # Convertir a funciones numéricas de numpy
                    f_num = sp.lambdify(x, f_expr, 'numpy')
                    f_prime_num = sp.lambdify(x, f_prime_expr, 'numpy')
                    
                    x_val = st.slider("Posición X del punto de tangencia", -3.0, 3.0, 0.0, 0.05, key="s_custom")
                    
                    # Evaluar valor y pendiente
                    y_val = float(f_num(x_val))
                    slope = float(f_prime_num(x_val))
                    
                    # Dibujar gráfica con Matplotlib
                    fig, ax = plt.subplots(figsize=(8, 4.5))
                    fig.patch.set_facecolor('#0f172a')
                    ax.set_facecolor('#020617')
                    
                    x_curve = np.linspace(-4, 4, 300)
                    try:
                        y_curve = f_num(x_curve)
                        ax.plot(x_curve, y_curve, color='#22d3ee', linewidth=3, label=f"f(x) = {user_func_str}")
                    except:
                        pass
                    
                    # Recta tangente
                    x_tangent = np.linspace(x_val - 1.5, x_val + 1.5, 50)
                    y_tangent = slope * (x_tangent - x_val) + y_val
                    ax.plot(x_tangent, y_tangent, color='#f43f5e', linewidth=2.5, linestyle='--', label=f"Tangente (m={slope:.2f})")
                    
                    ax.scatter([x_val], [y_val], color='#f43f5e', s=100, zorder=5)
                    
                    ax.axhline(0, color='#334155', linewidth=1)
                    ax.axvline(0, color='#334155', linewidth=1)
                    ax.set_xlim(-4, 4)
                    ax.set_ylim(-10, 10)
                    ax.tick_params(colors='#94a3b8')
                    ax.grid(True, linestyle=':', alpha=0.3, color='#334155')
                    ax.legend(loc='upper left', facecolor='#0f172a', edgecolor='none', labelcolor='white')
                    
                    st.pyplot(fig)
                    st.success(f"📌 Derivada calculada automáticamente: $f'(x) = {f_prime_expr}$")
                    st.info(f"📍 En x = `{x_val:.2f}` ➔ Pendiente instantánea: **{slope:.2f}**")
                    
                except Exception as e:
                    st.error(f"⚠️ Revisa la sintaxis de la función. (Ejemplo correcto: `x**2 - 4` o `sin(x)`). Error: {e}")
                
            with tab2:
                st.write("### Reto: Clava la Pendiente")
                target_x = 1.0
                exact_slope = 3 * (target_x ** 2) - 3
                st.write(f"Calcula la derivada de $f(x) = x^3 - 3x$ en el punto **x = {target_x}**.")
                
                user_slope = st.slider("Ajusta la pendiente objetivo", -6.0, 6.0, 0.0, 0.5, key="sniper_s")
                if st.button("🎯 Disparar con esta pendiente"):
                    if abs(user_slope - exact_slope) < 0.5:
                        st.success("🎉 ¡Impacto perfecto! Has clavado la pendiente exacta.")
                        u_data["score"] += 200
                        u_data["streak"] += 1
                        u_data["corrects"] += 1
                        if u_data["unlocked"] < 2:
                            u_data["unlocked"] = 2
                        save_users(st.session_state.users)
                    else:
                        st.error("❌ Te has quedado lejos. ¡Prueba otra vez!")
                        u_data["streak"] = 0
                        u_data["errors"] += 1
                        save_users(st.session_state.users)

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
        st.markdown(f"## 📊 Informe de Rendimiento de `{st.session_state.current_user}`")
        col1, col2, col3 = st.columns(3)
        col1.metric("Puntuación Total", f"{u_data['score']} PTS")
        col2.metric("Aciertos", u_data["corrects"])
        col3.metric("Fallos", u_data["errors"])
        st.markdown("---")
        if u_data["errors"] == 0:
            st.success("🌟 ¡Impecable! Cero fallos registrados. ¡Estás listo para la EBAU!")
        else:
            st.warning(f"⚠️ Has tenido {u_data['errors']} fallos. ¡Vuelve al mapa para practicar!")
            
        if st.button("🗺️ Volver al Mapa de Mundos", use_container_width=True):
            st.session_state.screen = "map"
            st.rerun()
