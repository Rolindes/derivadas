import streamlit as st
import random
import json
import os

st.set_page_config(page_title="Derivative F1 Arcade", page_icon="🏎️", layout="centered")

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
    st.markdown("## 🏎️ DERIVATIVE F1 ARCADE")
    st.write("Introduce tu apodo de piloto:")
    nickname = st.text_input("Tu apodo:")
    if st.button("🏁 ¡Arrancar Motor!", use_container_width=True):
        if nickname.strip() != "":
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

    # ================= MAPA DE MUNDOS =================
    if st.session_state.screen == "map":
        st.markdown("## 🗺️ Circuito Mundial - Mapa de Fases")
        worlds = [
            (1, "Fase 1: 🏎️ Gran Premio F1 Arcade Real (7 Vueltas en Pista)"),
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

    # ================= ZONA DE JUEGO =================
    elif st.session_state.screen == "game":
        b = st.session_state.active_block
        st.markdown(f"## 🏁 Circuito Activo - Fase 0{b}")
        if st.button("⬅️ Volver al Mapa"):
            st.session_state.screen = "map"
            st.rerun()
        st.markdown("---")

        # MUNDO 1: VIDEOJUEGO DE F1 REAL (HTML5 CANVAS)
        if b == 1:
            st.subheader("🏎️ Gran Premio F1: Pista Interactiva en Movimiento")
            st.write("Usa los botones o las **flechas del teclado** para mover tu coche de F1 entre los 5 carriles. ¡Esquiva los muros rojos y pilla la derivada correcta para superar las 7 vueltas!")

            f1_arcade_js_html = """
            <!DOCTYPE html>
            <html>
            <head>
            <style>
              body { background-color: #020617; color: white; text-align: center; font-family: sans-serif; margin: 0; }
              canvas { background-color: #090d16; border: 4px solid #38bdf8; border-radius: 12px; box-shadow: 0 0 30px rgba(56,189,248,0.4); display: block; margin: 0 auto; }
              .controls { margin-top: 12px; }
              .btn-arcade { background-color: #2563eb; color: white; border: none; padding: 12px 25px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; margin: 0 8px; }
              .btn-arcade:hover { background-color: #1d4ed8; }
            </style>
            </head>
            <body>
              <div id="hud" style="font-size: 16px; font-weight: bold; color: #fbbf24; margin-bottom: 8px;">
                Vuelta <span id="lapNum">1</span>/7 | Vidas: <span id="livesCount">❤️❤️❤️</span>
              </div>
              <div id="challengeBox" style="font-size: 18px; font-weight: bold; color: #f43f5e; margin-bottom: 8px;">
                Calcula f'(3) para f(x) = x²
              </div>
              
              <canvas id="f1Canvas" width="450" height="320"></canvas>
              
              <div class="controls">
                <button class="btn-arcade" onclick="moveCar(-1)">⬅️ Izquierda</button>
                <button class="btn-arcade" onclick="moveCar(1)">Derecha ➡️</button>
              </div>

            <script>
              const canvas = document.getElementById("f1Canvas");
              const ctx = canvas.getContext("2d");

              // 5 Carriles centrados en X
              const lanes = [65, 155, 245, 335, 425];
              let currentLane = 2; // Empieza en el carril central (índice 2)
              let carY = 250;

              let lap = 1;
              let lives = 3;
              let obstacleY = -120;
              let speed = 2.5;

              // Retos de 7 vueltas
              const challenges = [
                { f: "x²", x: 3, correct: 6, opts: [2, 4, 6, 9, 12] },
                { f: "x³", x: 2, correct: 12, opts: [4, 8, 12, 16, 6] },
                { f: "5x", x: 4, correct: 5, opts: [20, 10, 5, 25, 0] },
                { f: "x³ - 3x", x: 2, correct: 9, opts: [3, 6, 9, 12, 15] },
                { f: "sin(x)", x: 0, correct: 1, opts: [-1, 0, 1, 2, -2] },
                { f: "2x² + 1", x: 3, correct: 12, opts: [6, 12, 18, 24, 9] },
                { f: "x⁴", x: 1, correct: 4, opts: [1, 2, 3, 4, 8] }
              ];

              let currentCh = challenges[0];

              function updateChallengeText() {
                document.getElementById("challengeBox.innerHTML") = `Calcula f'(${currentCh.x}) para f(x) = ${currentCh.f}`;
                document.getElementById("lapNum").innerText = lap;
                let hearts = "";
                for(let i=0; i<lives; i++) hearts += "❤️";
                document.getElementById("livesCount").innerText = hearts;
              }

              function moveCar(dir) {
                currentLane += dir;
                if (currentLane < 0) currentLane = 0;
                if (currentLane > 4) currentLane = 4;
              }

              // Control por teclado (flechas)
              window.addEventListener('keydown', function(e) {
                if (e.key === "ArrowLeft") moveCar(-1);
                if (e.key === "ArrowRight") moveCar(1);
              });

              function resetObstacle() {
                obstacleY = -120;
                // Barajar opciones en los 5 carriles
                currentCh.opts.sort(() => Math.random() - 0.5);
              }

              resetObstacle();

              function update() {
                obstacleY += speed;

                // Cuando el obstáculo llega a la altura del coche
                if (obstacleY >= carY - 20 && obstacleY <= carY + 35) {
                  // Comprobar en qué carril está el coche
                  let winningLane = currentCh.opts.indexOf(currentCh.correct);
                  
                  if (currentLane === winningLane) {
                    // ¡ACIERTO!
                    lap++;
                    if (lap > 7) {
                      alert("🏆 ¡VICTORIA! ¡Has ganado el Gran Premio de 7 Vueltas!");
                      lap = 1; lives = 3;
                    } else {
                      currentCh = challenges[lap - 1];
                    }
                    resetObstacle();
                  } else {
                    // ¡FALLO / ACCIDENTE!
                    lives--;
                    if (lives <= 0) {
                      alert("💥 ¡GAME OVER! Te has estrellado contra el muro del error.");
                      lives = 3; lap = 1;
                      currentCh = challenges[0];
                    }
                    resetObstacle();
                  }
                  updateChallengeText();
                }
              }

              function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Dibujar Carretera de Asfalto
                ctx.fillStyle = "#1e293b";
                ctx.fillRect(20, 0, 410, 320);

                // Líneas divisorias discontinuas de los carriles
                ctx.strokeStyle = "#475569";
                ctx.lineWidth = 2;
                ctx.setLineDash([15, 15]);
                for(let i=1; i<5; i++) {
                  ctx.beginPath();
                  ctx.moveTo(20 + i*82, 0);
                  ctx.lineTo(20 + i*82, 320);
                  ctx.stroke();
                }
                ctx.setLineDash([]);

                // Dibujar los 5 bloques de opciones bajando por los carriles
                for(let i=0; i<5; i++) {
                  let isCorrect = (currentCh.opts[i] === currentCh.correct);
                  ctx.fillStyle = isCorrect ? "#22c55e" : "#ef4444";
                  ctx.fillRect(lanes[i] - 32, obstacleY, 64, 45);
                  
                  ctx.fillStyle = "white";
                  ctx.font = "bold 20px sans-serif";
                  ctx.fillText(currentCh.opts[i], lanes[i] - 10, obstacleY + 28);
                }

                // Dibujar el coche de F1 del jugador
                ctx.fillStyle = "#facc15"; // Chasis amarillo F1
                ctx.fillRect(lanes[currentLane] - 16, carY, 32, 50);
                ctx.fillStyle = "#0f172a"; // Cabina
                ctx.fillRect(lanes[currentLane] - 10, carY + 12, 20, 20);
                // Alerón
                ctx.fillStyle = "#ef4444";
                ctx.fillRect(lanes[currentLane] - 20, carY + 40, 40, 6);
              }

              function loop() {
                update();
                draw();
                requestAnimationFrame(loop);
              }

              updateChallengeText();
              loop();
            </script>
            </body>
            </html>
            """
            st.components.v1.html(f1_arcade_js_html, height=480)

        elif b == 2:
            st.subheader("Bloque 2: Fragua Polinómica")
            # ... resto de bloques ...
