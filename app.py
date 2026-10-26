import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="Derivative Adventure", page_icon="⚡", layout="centered")

# Estilos CSS modernos (modo oscuro neón)
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; font-family: sans-serif; }
    .neon-title { font-size: 28px; font-weight: 900; background: linear-gradient(90deg, #22d3ee, #818cf8, #f43f5e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .card { background-color: #0f172a; padding: 20px; border-radius: 20px; border: 1px solid #1e293b; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión para puntos, racha y progreso
if "score" not in st.session_state:
    st.session_state.score = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "corrects" not in st.session_state:
    st.session_state.corrects = 0
if "errors" not in st.session_state:
    st.session_state.errors = 0
if "unlocked" not in st.session_state:
    st.session_state.unlocked = 1
if "screen" not in st.session_state:
    st.session_state.screen = "map"
if "active_block" not in st.session_state:
    st.session_state.active_block = 1

# HEADER FIJO
col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
with col_h1:
    st.markdown('<p class="neon-title">⚡ DERIVATIVE ADVENTURE</p>', unsafe_allow_html=True)
with col_h2:
    st.metric("🔥 Racha", st.session_state.streak)
with col_h3:
    st.metric("🏆 Pts", st.session_state.score)

st.markdown("---")

# ================= PANTALLA 1: MAPA DE MUNDOS =================
if st.session_state.screen == "map":
    st.markdown("### 🗺️ Mapa de Avance de Mundos (2º Bachillerato)")
    st.write("Supera los retos de cada fase para desbloquear el siguiente nivel de dificultad.")
    
    cols = st.columns(5)
    worlds = [
        (1, "Tangentes", "Fase 01"),
        (2, "Polinomios", "Fase 02"),
        (3, "Trascendentes", "Fase 03"),
        (4, "Productos", "Fase 04"),
        (5, "Jefe Final", "Fase 05")
    ]
    
    for i, (wid, wname, wdesc) in enumerate(worlds):
        with cols[i]:
            is_unlocked = wid <= st.session_state.unlocked
            if is_unlocked:
                if st.button(f"🎮 {wname}\n({wdesc})", key=f"w_{wid}", use_container_width=True):
                    st.session_state.active_block = wid
                    st.session_state.screen = "game"
                    st.rerun()
            else:
                st.button(f"🔒 {wname}\n(Bloqueado)", key=f"w_{wid}", disabled=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📊 Ver Informe de Rendimiento Final", use_container_width=True):
        st.session_state.screen = "summary"
        st.rerun()

# ================= PANTALLA 2: JUEGO POR BLOQUES =================
elif st.session_state.screen == "game":
    b = st.session_state.active_block
    st.markdown(f"### 🚀 Mundo Activo: Fase 0{b}")
    
    if st.button("⬅️ Volver al Mapa"):
        st.session_state.screen = "map"
        st.rerun()
        
    st.markdown("---")

    # MUNDO 1: TANGENTES Y PENDIENTES (SIMULADOR VISUAL + RETO)
    if b == 1:
        st.subheader("Bloque 1: El Significado de la Derivada")
        tab1, tab2 = st.tabs(["💡 Práctica Visual (Slider)", "🎯 Minijuego Francotirador"])
        
        with tab1:
            st.write("Mueve el selector para ver cómo cambia la pendiente instantánea en la función cúbica $f(x) = x^3 - 3x$.")
            x_val = st.slider("Posición en el Eje X", -2.0, 2.0, 0.0, 0.1, key="s_v1")
            slope = 3 * (x_val ** 2) - 3
            st.info(f"📍 Coordenada X: {x_val} | 📐 Pendiente (Derivada) en este punto: **{slope:.2f}**")
            if abs(slope) < 0.1:
                st.success("¡Estás en un punto crítico (máximo o mínimo local donde la derivada es cero)!")
                
        with tab2:
            st.write("### Minijuego: Clava la Pendiente")
            target_x = 1.0
            exact_slope = 3 * (target_x ** 2) - 3
            st.write(f"Calcula la derivada de $f(x) = x^3 - 3x$ en el punto **x = {target_x}**.")
            
            user_slope = st.slider("Ajusta la pendiente objetivo", -6.0, 6.0, 0.0, 0.5, key="sniper_s")
            if st.button("🎯 Disparar con esta pendiente"):
                if abs(user_slope - exact_slope) < 0.5:
                    st.success("🎉 ¡Impacto perfecto! Has clavado la pendiente exacta.")
                    st.session_state.score += 200
                    st.session_state.streak += 1
                    st.session_state.corrects += 1
                    if st.session_state.unlocked < 2:
                        st.session_state.unlocked = 2
                else:
                    st.error("❌ Te has quedado lejos. ¡Sigue probando!")
                    st.session_state.streak = 0
                    st.session_state.errors += 1

    # MUNDO 2: POLINOMIOS (GLOBOS DE CÁLCULO)
    elif b == 2:
        st.subheader("Bloque 2: Fragua Polinómica")
        st.write("Deriva el siguiente polinomio de forma rápida:")
        
        a, c_val = random.randint(2, 4), random.randint(1, 5)
        correct_ans = f"{2*a}x + {c_val}"
        options = [correct_ans, f"{a}x + {c_val}", f"{2*a}x²", f"{c_val}x"]
        random.shuffle(options)
        
        st.markdown(f'<div class="card"><h2 style="text-align:center; color:#818cf8;">f(x) = {a}x² + {c_val}x</h2></div>', unsafe_allow_html=True)
        
        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                if st.button(f"🎈 {opt}", key=f"p_opt_{i}", use_container_width=True):
                    if opt == correct_ans:
                        st.success("¡Globo correcto! +150 PTS")
                        st.session_state.score += 150
                        st.session_state.streak += 1
                        st.session_state.corrects += 1
                        if st.session_state.unlocked < 3:
                            st.session_state.unlocked = 3
                        st.rerun()
                    else:
                        st.error("¡Globo equivocado!")
                        st.session_state.streak = 0
                        st.session_state.errors += 1

    # MUNDO 3: TRASCENDENTES (DISPARO LÁSER)
    elif b == 3:
        st.subheader("Bloque 3: Bosque Trascendente (Senos y Exponenciales)")
        st.write("Selecciona el cañón láser con la derivada correcta:")
        
        st.markdown(f'<div class="card"><h2 style="text-align:center; color:#34d399;">f(x) = 4sin(x)</h2></div>', unsafe_allow_html=True)
        correct_t = "4cos(x)"
        t_opts = ["4cos(x)", "-4sin(x)", "4sin(x)", "-4cos(x)"]
        random.shuffle(t_opts)
        
        cols = st.columns(2)
        for i, opt in enumerate(t_opts):
            with cols[i % 2]:
                if st.button(f"🎯 {opt}", key=f"t_opt_{i}", use_container_width=True):
                    if opt == correct_t:
                        st.success("¡Disparo exitoso! +200 PTS")
                        st.session_state.score += 200
                        st.session_state.streak += 1
                        st.session_state.corrects += 1
                        if st.session_state.unlocked < 4:
                            st.session_state.unlocked = 4
                        st.rerun()
                    else:
                        st.error("¡Fallo de disparo!")
                        st.session_state.streak = 0
                        st.session_state.errors += 1

    # MUNDO 4: PRODUCTOS Y COCIENTES
    elif b == 4:
        st.subheader("Bloque 4: Torre de Productos")
        st.write("Aplica la regla del producto $[u \cdot v]' = u'v + uv'$:")
        
        st.markdown(f'<div class="card"><h2 style="text-align:center; color:#fbbf24;">f(x) = x² · sin(x)</h2></div>', unsafe_allow_html=True)
        correct_pr = "2x·sin(x) + x²·cos(x)"
        pr_opts = [correct_pr, "2x·cos(x)", "x²·sin(x)", "2x·sin(x) - x²·cos(x)"]
        random.shuffle(pr_opts)
        
        for i, opt in enumerate(pr_opts):
            if st.button(f"📦 {opt}", key=f"pr_opt_{i}", use_container_width=True):
                if opt == correct_pr:
                    st.success("¡Cinta organizada con éxito! +250 PTS")
                    st.session_state.score += 250
                    st.session_state.streak += 1
                    st.session_state.corrects += 1
                    if st.session_state.unlocked < 5:
                        st.session_state.unlocked = 5
                    st.rerun()
                else:
                    st.error("Error en la cinta.")
                    st.session_state.streak = 0
                    st.session_state.errors += 1

    # MUNDO 5: REGLA DE LA CADENA (JEFE FINAL)
    elif b == 5:
        st.subheader("Bloque 5: Jefe Final - Regla de la Cadena")
        st.write("Rompe el escudo de la función compuesta rompiendo sus capas:")
        
        st.markdown(f'<div class="card"><h2 style="text-align:center; color:#f43f5e;">f(x) = sin(4x²)</h2></div>', unsafe_allow_html=True)
        correct_c = "cos(4x²) · (8x)"
        c_opts = [correct_c, "cos(4x²)", "-sin(4x²) · 8x", "8x·sin(4x²)"]
        random.shuffle(c_opts)
        
        for i, opt in enumerate(c_opts):
            if st.button(f"⚔️ {opt}", key=f"c_opt_{i}", use_container_width=True):
                if opt == correct_c:
                    st.success("🎉 ¡VICTORIA! ¡Jefe derrotado con la derivada de la cadena! +500 PTS")
                    st.session_state.score += 500
                    st.session_state.streak += 1
                    st.session_state.corrects += 1
                    st.rerun()
                else:
                    st.error("¡Ataque bloqueado por el jefe!")
                    st.session_state.streak = 0
                    st.session_state.errors += 1

# ================= PANTALLA 3: INFORME Y RESUMEN =================
elif st.session_state.screen == "summary":
    st.markdown("### 📊 Informe de Rendimiento EBAU")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Puntuación Total", f"{st.session_state.score} PTS")
    col2.metric("Aciertos", st.session_state.corrects)
    col3.metric("Fallos", st.session_state.errors)
    
    st.markdown("---")
    if st.session_state.errors == 0:
        st.success("🌟 ¡Impecable! Cero fallos registrados en tu sesión. Estás más que preparado para el examen.")
    else:
        st.warning(f"⚠️ Has registrado {st.session_state.errors} fallos. Repasa los mundos donde perdiste racha para afianzar conceptos.")
        
    if st.button("🗺️ Volver al Mapa de Mundos"):
        st.session_state.screen = "map"
        st.rerun()
