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
            (1, "Fase 1: 🟡 Laberinto Pac-Man (Movimiento Real)"),
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

        # MUNDO 1: LABERINTO PAC-MAN INTERACTIVO EN HTML5/JS
        if b == 1:
            st.subheader("🟡 Minijuego: Pac-Man Laberinto de Derivadas")
            st.write("Usa los botones o muévete por el laberinto para guiar al comecocos hacia la pastilla con la **derivada correcta** y esquivar a los fantasmas.")

            # Componente HTML / Canvas interactivo embebido en Streamlit
            pacman_html = """
            <!DOCTYPE html>
            <html>
            <head>
            <style>
              body { background-color: #020617; color: white; text-align: center; font-family: sans-serif; }
              canvas { background-color: #0f172a; border: 3px solid #38bdf8; border-radius: 10px; box-shadow: 0 0 20px rgba(56,189,248,0.3); }
              .btn-control { background-color: #2563eb; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 8px; cursor: pointer; margin: 5px; font-weight: bold; }
              .btn-control:hover { background-color: #1d4ed8; }
            </style>
            </head>
            <body>
              <h3 id="question" style="color: #fbbf24; margin: 5px;">Reto: Derivada de f(x) = x²</h3>
              <canvas id="gameCanvas" width="400" height="250"></canvas>
              <div>
                <button class="btn-control" onclick="move('UP')">⬆️ Arriba</button><br>
                <button class="btn-control" onclick="move('LEFT')">⬅️ Izda</button>
                <button class="btn-control" onclick="move('RIGHT')">➡️ Dcha</button><br>
                <button class="btn-control" onclick="move('DOWN')">⬇️ Abajo</button>
              </div>
              <p id="status" style="color: #38bdf8; font-weight: bold;"></p>

            <script>
              const canvas = document.getElementById("gameCanvas");
              const ctx = canvas.getContext("2d");

              let pacman = { x: 50, y: 125, size: 15, speed: 15 };
              let ghost = { x: 330, y: 125, size: 15, speed: 2 };
              let targetPill = { x: 330, y: 60, text: "2x", correct: true };
              let wrongPill = { x: 330, y: 190, text: "x²", correct: false };
              let score = 0;

              function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Dibujar Pasillos / Laberinto (líneas decorativas)
                ctx.strokeStyle = "#1e293b";
                ctx.lineWidth = 4;
                ctx.strokeRect(20, 20, 360, 210);

                // Dibujar Pac-Man
                ctx.beginPath();
                ctx.arc(pacman.x, pacman.y, pacman.size, 0.2 * Math.PI, 1.8 * Math.PI);
                ctx.lineTo(pacman.x, pacman.y);
                ctx.fillStyle = "#facc15";
                ctx.fill();
                ctx.closePath();

                // Dibujar Fantasma del Error
                ctx.beginPath();
                ctx.arc(ghost.x, ghost.y, ghost.size, Math.PI, 0, false);
                ctx.lineTo(ghost.x + ghost.size, ghost.y + ghost.size);
                ctx.lineTo(ghost.x - ghost.size, ghost.y + ghost.size);
                ctx.fillStyle = "#f43f5e";
                ctx.fill();
                ctx.closePath();

                // Dibujar Pastilla Correcta (Ganadora)
                ctx.beginPath();
                ctx.arc(targetPill.x, targetPill.y, 18, 0, 2 * Math.PI);
                ctx.fillStyle = "#4ade80";
                ctx.fill();
                ctx.fillStyle = "#020617";
                ctx.font = "bold 14px sans-serif";
                ctx.fillText(targetPill.text, targetPill.x - 10, targetPill.y + 5);

                // Dibujar Pastilla Incorrecta (Trampa)
                ctx.beginPath();
                ctx.arc(wrongPill.x, wrongPill.y, 18, 0, 2 * Math.PI);
                ctx.fillStyle = "#f87171";
                ctx.fill();
                ctx.fillStyle = "#020617";
                ctx.fillText(wrongPill.text, wrongPill.x - 10, wrongPill.y + 5);
              }

              function move(dir) {
                if (dir === 'UP' && pacman.y > 40) pacman.y -= pacman.speed;
                if (dir === 'DOWN' && pacman.y < 210) pacman.y += pacman.speed;
                if (dir === 'LEFT' && pacman.x > 40) pacman.x -= pacman.speed;
                if (dir === 'RIGHT' && pacman.x < 360) pacman.x += pacman.speed;

                checkCollision();
                draw();
              }

              function checkCollision() {
                // Comprobar si choca con la pastilla correcta
                let distCorrect = Math.hypot(pacman.x - targetPill.x, pacman.y - targetPill.y);
                let distWrong = Math.hypot(pacman.x - wrongPill.x, pacman.y - wrongPill.y);

                if (distCorrect < 25) {
                  document.getElementById("status").innerHTML = "🎉 ¡WAKA WAKA! ¡Te comiste la derivada correcta!";
                  document.getElementById("status").style.color = "#4ade80";
                  setTimeout(resetGame, 1500);
                } else if (distWrong < 25) {
                  document.getElementById("status").innerHTML = "❌ ¡CHOCASTE CON EL FANTASMA! Era la trampa.";
                  document.getElementById("status").style.color = "#f43f5e";
                  setTimeout(resetGame, 1500);
                }
              }

              function resetGame() {
                pacman.x = 50; pacman.y = 125;
                document.getElementById("status").innerHTML = "";
                draw();
              }

              draw();
            </script>
            </body>
            </html>
            """
            
            st.components.v1.html(pacman_html, height=420)

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
