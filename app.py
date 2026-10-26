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

    # ================= MAPA DE MUNDOS (TODOS DESBLOQUEADOS) =================
    if st.session_state.screen == "map":
        st.markdown("## 🗺️ Circuito Mundial - Acceso Libre a Fases")
        st.write("Selecciona cualquier fase libremente para practicar:")
        
        worlds = [
            (1, "Fase 1: 🏎️ Gran Premio F1 Arcade (Carretera Lenta y Táctil)"),
            (2, "Fase 2: 🎈 Fragua Polinómica"),
            (3, "Fase 3: 🎯 Bosque Trascendente"),
            (4, "Fase 4: 📦 Torre de Productos"),
            (5, "Fase 5: ⚔️ Jefe Final - Regla de la Cadena")
        ]
        
        for wid, wname in worlds:
            if st.button(f"🎮 Entrar a -> {wname}", key=f"w_{wid}", use_container_width=True):
                st.session_state.active_block = wid
                st.session_state.screen = "game"
                st.rerun()

        st.markdown("---")
        if st.button("📊 Ver Informe Final", use_container_width=True):
            st.session_state.screen = "summary"
            st.rerun()

    # ================= ZONA DE JUEGO =================
    elif st.session_state.screen == "game":
        b = st.session_state.active_block
        st.markdown(f"## 🏁 Circuito Activo - Fase 0{b}")
        if st.button("⬅️ Volver al Mapa de Fases"):
            st.session_state.screen = "map"
            st.rerun()
        st.markdown("---")

        # MUNDO 1: CARRERA DE F1 LENTA, TÁCTIL Y UNIFORME
        if b == 1:
            st.subheader("🏎️ Gran Premio F1: Conducción Suave")
            st.markdown("La pista va **despacio** para darte tiempo a pensar. Puedes usar los botones táctiles/ratón, los botones de los carriles inferiores o las flechas.")

            f1_canvas_game = """
            <!DOCTYPE html>
            <html>
            <head>
            <style>
              body { background-color: #020617; color: white; text-align: center; font-family: sans-serif; margin: 0; padding: 0; }
              canvas { background-color: #0f172a; border: 4px solid #38bdf8; border-radius: 12px; box-shadow: 0 0 25px rgba(56,189,248,0.4); display: block; margin: 0 auto; cursor: pointer; }
              .controls { margin-top: 15px; }
              .btn-move { background-color: #2563eb; color: white; border: none; padding: 14px 26px; font-size: 16px; border-radius: 10px; cursor: pointer; font-weight: bold; margin: 0 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
              .btn-move:hover { background-color: #1d4ed8; }
            </style>
            </head>
            <body>
              <div style="margin-bottom: 6px; font-weight: bold; font-size: 15px; color: #fbbf24;">
                Vuelta: <span id="lapDisplay">1</span> / 7 &nbsp;|&nbsp; Vidas: <span id="livesDisplay">❤️❤️❤️</span> &nbsp;|&nbsp; Puntos: <span id="scoreDisplay">0</span>
              </div>
              
              <div style="background: linear-gradient(135deg, #1e293b, #0f172a); border: 3px solid #38bdf8; border-radius: 12px; padding: 12px; width: 440px; margin: 0 auto 10px auto; text-align: center; box-shadow: 0 0 15px rgba(56,189,248,0.2);">
                <div style="color: #38bdf8; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">Reto Activo de Derivada</div>
                <div id="funcText" style="color: #f8fafc; font-size: 22px; font-weight: 900; margin-top: 4px;">f(x) = x² &nbsp;|&nbsp; x = 3</div>
                <div id="questionPrompt" style="color: #f43f5e; font-size: 15px; font-weight: bold; margin-top: 2px;">Calcula f'(3)</div>
                <div id="statusAlert" style="color: #22c55e; font-size: 13px; font-weight: bold; margin-top: 4px; min-height: 18px;"></div>
              </div>

              <canvas id="f1Canvas" width="450" height="280"></canvas>

              <div class="controls">
                <button class="btn-move" onclick="moveCar(-1)">⬅️ Izquierda</button>
                <button class="btn-move" onclick="setLaneByTouch(0)">C1</button>
                <button class="btn-move" onclick="setLaneByTouch(1)">C2</button>
                <button class="btn-move" onclick="setLaneByTouch(2)">C3</button>
                <button class="btn-move" onclick="setLaneByTouch(3)">C4</button>
                <button class="btn-move" onclick="setLaneByTouch(4)">C5</button>
                <button class="btn-move" onclick="moveCar(1)">Derecha ➡️</button>
              </div>

            <script>
              const canvas = document.getElementById("f1Canvas");
              const ctx = canvas.getContext("2d");

              const lanes = [45, 135, 225, 315, 405];
              let currentLane = 2;
              const carY = 200;

              let lap = 1;
              let lives = 3;
              let score = 0;
              let roadOffset = 0;

              let obstacleY = -120;
              let speed = 0.8;

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

              function updateUI(msg = "", isError = false) {
                document.getElementById("lapDisplay").innerText = lap;
                document.getElementById("scoreDisplay").innerText = score;
                let h = "";
                for(let i=0; i<lives; i++) h += "❤️";
                document.getElementById("livesDisplay").innerText = h;
                
                document.getElementById("funcText").innerHTML = `f(x) = ${currentCh.f} &nbsp;|&nbsp; x = ${currentCh.x}`;
                document.getElementById("questionPrompt").innerText = `Calcula f'(${currentCh.x})`;
                
                const alertBox = document.getElementById("statusAlert");
                alertBox.innerText = msg;
                alertBox.style.color = isError ? "#ef4444" : "#22c55e";
              }

              function moveCar(dir) {
                currentLane += dir;
                if (currentLane < 0) currentLane = 0;
                if (currentLane > 4) currentLane = 4;
              }

              function setLaneByTouch(laneIdx) {
                currentLane = laneIdx;
              }

              canvas.addEventListener('click', function(e) {
                const rect = canvas.getBoundingClientRect();
                const clickX = e.clientX - rect.left;
                if (clickX < 90) currentLane = 0;
                else if (clickX < 180) currentLane = 1;
                else if (clickX < 270) currentLane = 2;
                else if (clickX < 360) currentLane = 3;
                else currentLane = 4;
              });

              window.addEventListener('keydown', function(e) {
                if (e.key === "ArrowLeft") moveCar(-1);
                if (e.key === "ArrowRight") moveCar(1);
              });

              function resetObstacles() {
                obstacleY = -140;
                currentCh.opts.sort(() => Math.random() - 0.5);
              }

              resetObstacles();

              function update() {
                roadOffset += speed * 1.5;
                if (roadOffset > 40) roadOffset = 0;

                obstacleY += speed;

                if (obstacleY >= carY - 25 && obstacleY <= carY + 35) {
                  let winningLane = currentCh.opts.indexOf(currentCh.correct);

                  if (currentLane === winningLane) {
                    score += 200;
                    lap++;
                    if (lap > 7) {
                      alert("🏆 ¡VICTORIA! ¡Has completado las 7 vueltas del Gran Premio!");
                      lap = 1; score = 0; lives = 3;
                    } else {
                      currentCh = challenges[lap - 1];
                    }
                    updateUI("🎉 ¡EXCELENTE! ¡Acierto!", false);
                    resetObstacles();
                  } else {
                    lives--;
                    if (lives <= 0) {
                      alert("💥 ¡GAME OVER! Te has estrellado demasiadas veces.");
                      lives = 3; lap = 1; score = 0;
                      currentCh = challenges[0];
                    }
                    updateUI("❌ ¡ERROR! Te has estrellado contra el muro incorrecto.", true);
                    resetObstacles();
                  }
                }
              }

              function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#1e293b";
                ctx.fillRect(15, 0, 420, 280);

                ctx.fillStyle = "#ef4444";
                ctx.fillRect(15, 0, 8, 280);
                ctx.fillRect(427, 0, 8, 280);

                ctx.strokeStyle = "#94a3b8";
                ctx.lineWidth = 3;
                ctx.setLineDash([20, 20]);
                ctx.lineDashOffset = -roadOffset;
                for(let i=1; i<5; i++) {
                  ctx.beginPath();
                  ctx.moveTo(15 + i*84, 0);
                  ctx.lineTo(15 + i*84, 280);
                  ctx.stroke();
                }
                ctx.setLineDash([]);

                for(let i=0; i<5; i++) {
                  let val = currentCh.opts[i];

                  ctx.fillStyle = "#334155";
                  ctx.fillRect(lanes[i] - 32, obstacleY, 64, 40);
                  ctx.strokeStyle = "#64748b";
                  ctx.lineWidth = 1;
                  ctx.strokeRect(lanes[i] - 32, obstacleY, 64, 40);

                  ctx.fillStyle = "#ffffff";
                  ctx.font = "bold 18px sans-serif";
                  ctx.fillText(val, lanes[i] - 10, obstacleY + 26);
                }

                let carX = lanes[currentLane];
                ctx.fillStyle = "#facc15";
                ctx.fillRect(carX - 14, carY, 28, 45);
                ctx.fillStyle = "#0f172a";
                ctx.fillRect(carX - 9, carY + 10, 18, 16);
                ctx.fillStyle = "#38bdf8";
                ctx.fillRect(carX - 20, carY - 2, 40, 6);
                ctx.fillStyle = "#ef4444";
                ctx.fillRect(carX - 18, carY + 42, 36, 6);
              }

              function loop() {
                update();
                draw();
                requestAnimationFrame(loop);
              }

              updateUI();
              loop();
            </script>
            </body>
            </html>
            """

            st.components.v1.html(f1_canvas_game, height=540)

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
                        save_users(st.session_state.users)
                        st.rerun()
                    else:
                        st.error("¡Error! Respuesta incorrecta.")
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
                        save_users(st.session_state.users)
                        st.rerun()
                    else:
                        st.error("¡Error! Respuesta incorrecta.")
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
                        save_users(st.session_state.users)
                        st.rerun()
                    else:
                        st.error("¡Error! Respuesta incorrecta.")
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
                        st.error("¡Error! Ataque bloqueado.")
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
