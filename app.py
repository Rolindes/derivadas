import streamlit as st
import random
import json
import os
import numpy as np
import matplotlib.pyplot as plt

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
                st.session_state.users[clean_name] = {
                    "score": 0, "streak": 0, "corrects": 0, "errors": 0,
                    "scores_by_game": {"F1": 0, "Globos": 0, "Tenis": 0, "Tetris": 0, "Jefe": 0}
                }
                save_users(st.session_state.users)
            st.session_state.screen = "map"
            st.rerun()
else:
    u_data = st.session_state.users[st.session_state.current_user]
    if "scores_by_game" not in u_data:
        u_data["scores_by_game"] = {"F1": 0, "Globos": 0, "Tenis": 0, "Tetris": 0, "Jefe": 0}

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"🏎️ Piloto: `{st.session_state.current_user}`")
        if st.button("🔄 Cambiar"):
            st.session_state.current_user = None
            st.session_state.screen = "login"
            st.rerun()
    with col2: st.metric("🔥 Racha", u_data["streak"])
    with col3: st.metric("🏆 Pts Total", u_data["score"])
    with col4:
        if st.button("📊 Informe"):
            st.session_state.screen = "summary"
            st.rerun()

    st.markdown("---")

    # ================= FASE 0: MENÚ PRINCIPAL Y GRÁFICA INTERACTIVA =================
    if st.session_state.screen == "map":
        st.markdown("## 🗺️ Fase 0: Menú Principal y Gráfica Interactiva")
        st.markdown("### 📈 La Derivada como la Pendiente de la Recta Tangente ($m = f'(x)$)")
        st.write("Elige una función y mueve el slider para ver cómo la **recta tangente** se desplaza por la curva y cómo cambia su pendiente ($m$) en tiempo real:")

        func_choice = st.selectbox("Elige una función f(x):", ["x²", "x³", "sin(x)", "eˣ"])
        x_val = st.slider("Mueve el punto x en la curva:", -3.0, 3.0, 1.0, 0.1)

        fig, ax = plt.subplots(figsize=(6, 3.5))
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#1e293b')

        x_vals = np.linspace(-3.5, 3.5, 200)
        if func_choice == "x²":
            y_vals = x_vals ** 2
            y_val = x_val ** 2
            deriv_val = 2 * x_val
            func_name_str = "f(x) = x²"
        elif func_choice == "x³":
            y_vals = x_vals ** 3
            y_val = x_val ** 3
            deriv_val = 3 * (x_val ** 2)
            func_name_str = "f(x) = x³"
        elif func_choice == "sin(x)":
            y_vals = np.sin(x_vals)
            y_val = np.sin(x_val)
            deriv_val = np.cos(x_val)
            func_name_str = "f(x) = sin(x)"
        else:
            y_vals = np.exp(x_vals)
            y_val = np.exp(x_val)
            deriv_val = np.exp(x_val)
            func_name_str = "f(x) = eˣ"

        tangent_y = deriv_val * (x_vals - x_val) + y_val

        ax.plot(x_vals, y_vals, color='#38bdf8', linewidth=2.5, label=func_name_str)
        ax.plot(x_vals, tangent_y, color='#f43f5e', linestyle='--', linewidth=2, label=f"Tangente (m = {deriv_val:.2f})")
        ax.scatter([x_val], [y_val], color='#facc15', s=70, zorder=5)

        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(min(y_vals.min() - 2, -5), max(y_vals.max() + 2, 10))
        ax.axhline(0, color='#64748b', linewidth=1)
        ax.axvline(0, color='#64748b', linewidth=1)
        ax.tick_params(colors='white')
        ax.legend(facecolor='#0f172a', edgecolor='none', labelcolor='white')
        
        st.pyplot(fig)

        st.info(f"📊 **Función:** `{func_name_str}` | **Punto x:** `{x_val:.2f}`  \n🎯 **Pendiente de la recta tangente ($m = f'(x)$):** `{deriv_val:.2f}`")

        st.markdown("---")
        st.write("Selecciona una fase arcade (tienes **60 segundos** para completar tus 10 intentos):")
        
        worlds = [
            (1, "Fase 1: 🏎️ Gran Premio F1 (Autopista Arcade)"),
            (2, "Fase 2: 🎈 Fragua Polinómica (Cinta de Globos)"),
            (3, "Fase 3: 🎾 Tenis Trascendente (Juego de Pala)"),
            (4, "Fase 4: 🧱 Tetris de Productos (Piezas Geométricas)"),
            (5, "Fase 5: ⚔️ Jefe Final Regla de la Cadena (Combate)")
        ]
        
        for wid, wname in worlds:
            if st.button(f"🎮 Jugar -> {wname}", key=f"w_{wid}", use_container_width=True):
                st.session_state.active_block = wid
                st.session_state.screen = "game"
                st.rerun()

        st.markdown("---")
        if st.button("📊 Ver Informe y Puntuaciones Finales", use_container_width=True):
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
        # MUNDO 1: F1 ARCADE (Velocidad muy suave + 60 segundos)
        # -------------------------------------------------------------
        if b == 1:
            st.subheader("🏎️ Fase 1: Gran Premio F1 (Límite: 60 segundos)")
            st.markdown("Velocidad muy pausada. ¡Calcula y responde con tiempo de sobra!")

            f1_code = """
            <!DOCTYPE html>
            <html>
            <head><style>
              body { background: #020617; color: white; text-align: center; font-family: sans-serif; margin: 0; }
              canvas { background: #0f172a; border: 3px solid #38bdf8; border-radius: 10px; display: block; margin: 0 auto; cursor: pointer; }
              .btn { background: #2563eb; color: white; border: none; padding: 10px 16px; font-size: 15px; border-radius: 8px; cursor: pointer; font-weight: bold; margin: 3px; }
            </style></head>
            <body>
              <div style="font-size: 14px; color: #fbbf24; font-weight: bold; margin-bottom: 4px;">⏱️ Tiempo: <span id="timer">60</span>s | Pts: <span id="s">0</span></div>
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
              let lane = 2, oy = -100, pts = 0, offset = 0, timeLeft = 60, gameActive = true;
              
              const timerInterval = setInterval(() => {
                if(!gameActive) return;
                timeLeft--;
                document.getElementById("timer").innerText = timeLeft;
                if(timeLeft <= 0) {
                  gameActive = false;
                  alert("⏰ ¡Tiempo agotado! Puntuación final: " + pts);
                }
              }, 1000);

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
                document.getElementById("s").innerText = pts;
                document.getElementById("ft").innerHTML = `f(x) = ${q.f} | x = ${q.x}`;
                document.getElementById("qt").innerText = `Calcula f'(${q.x})`;
              }
              canvas.addEventListener('click', e => {
                if(!gameActive) return;
                let rect = canvas.getBoundingClientRect();
                let x = e.clientX - rect.left;
                lane = Math.floor(x / 90);
                if(lane > 4) lane = 4;
              });
              function resetQ() { oy = -100; q.opts.sort(() => Math.random() - 0.5); }
              resetQ();
              function loop() {
                if(!gameActive) return;
                offset = (offset + 0.3) % 40;
                oy += 0.3;
                if(oy >= 160 && oy <= 210) {
                  let chosen = q.opts[lane];
                  if(chosen === q.corr) {
                    pts += 200;
                  }
                  q = questions[Math.floor(Math.random() * questions.length)];
                  resetQ();
                }
                ctx.clearRect(0,0,450,240);
                ctx.fillStyle = "#1e293b"; ctx.fillRect(15,0,420,240);
                ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 2; ctx.setLineDash([20,20]); ctx.lineDashOffset = -offset;
                for(let i=1; i<5; i++) { ctx.beginPath(); ctx.moveTo(15+i*84,0); ctx.lineTo(15+i*84,240); ctx.stroke(); }
                ctx.setLineDash([]);
                for(let i=0; i<5; i++) {
                  ctx.fillStyle = "#334155"; ctx.fillRect(lanes[i]-30, oy, 60, 35);
                  ctx.strokeStyle = "#64748b"; ctx.strokeRect(lanes[i]-30, oy, 60, 35);
                  ctx.fillStyle = "white"; ctx.font = "bold 16px sans-serif"; ctx.fillText(q.opts[i], lanes[i]-12, oy+23);
                }
                let cx = lanes[lane];
                ctx.fillStyle = "#facc15"; ctx.fillRect(cx-14, 180, 28, 38);
                updateUI();
                requestAnimationFrame(loop);
              }
              loop();
            </script></body></html>
            """
            st.components.v1.html(f1_code, height=400)

        # -------------------------------------------------------------
        # MUNDO 2: FRAGUA POLINÓMICA (Velocidad muy suave + 60 segundos)
        # -------------------------------------------------------------
        elif b == 2:
            st.subheader("🎈 Fase 2: Fragua Polinómica (Límite: 60 segundos)")
            st.markdown("Globos flotando muy despacio. ¡Pincha con calma los correctos!")

            balloons_code = """
            <!DOCTYPE html>
            <html>
            <head><style>
              body { background: #020617; color: white; text-align: center; font-family: sans-serif; margin: 0; }
              canvas { background: #0f172a; border: 3px solid #ec4899; border-radius: 10px; display: block; margin: 0 auto; cursor: pointer; }
            </style></head>
            <body>
              <div style="font-size: 14px; color: #ec4899; font-weight: bold; margin-bottom: 4px;">⏱️ Tiempo: <span id="timer">60</span>s | Puntos: <span id="bs">0</span></div>
              <div style="background: #1e293b; border: 2px solid #ec4899; border-radius: 8px; padding: 6px; width: 420px; margin: 0 auto 6px auto;">
                <div style="color: #ec4899; font-size: 14px; font-weight: bold;" id="bft">f(x) = 4x² + 5x</div>
              </div>
              <canvas id="bc" width="450" height="240"></canvas>
            <script>
              const canvas = document.getElementById("bc");
              const ctx = canvas.getContext("2d");
              let score = 0, timeLeft = 60, gameActive = true;

              const timerInterval = setInterval(() => {
                if(!gameActive) return;
                timeLeft--;
                document.getElementById("timer").innerText = timeLeft;
                if(timeLeft <= 0) {
                  gameActive = false;
                  alert("⏰ ¡Tiempo agotado! Puntuación final: " + score);
                }
              }, 1000);

              const levels = [
                { f: "4x² + 5x", corr: "8x + 5", opts: ["5x", "8x²", "4x + 5", "8x + 5"] },
                { f: "3x³ - 2x", corr: "9x² - 2", opts: ["9x² - 2", "3x² - 2", "9x³", "x² - 2"] },
                { f: "x⁴ + 6x", corr: "4x³ + 6", opts: ["4x³", "4x³ + 6", "x³ + 6", "4x⁴ + 6"] },
                { f: "5x³", corr: "15x²", opts: ["5x²", "15x²", "3x²", "15x³"] },
                { f: "2x⁵ - 4x", corr: "10x⁴ - 4", opts: ["10x⁴", "10x⁴ - 4", "2x⁴ - 4", "5x⁴ - 4"] }
              ];
              let lvl = levels[0], items = [];
              function spawnBalloons() {
                items = [];
                let shuffled = [...lvl.opts].sort(() => Math.random() - 0.5);
                for(let i=0; i<4; i++) {
                  items.push({ text: shuffled[i], x: 75 + i*100, y: 240 + Math.random()*20, speed: 0.2 + Math.random()*0.2, radius: 32 });
                }
              }
              spawnBalloons();
              canvas.addEventListener('click', e => {
                if(!gameActive) return;
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left, my = e.clientY - rect.top;
                for(let item of items) {
                  if(Math.hypot(mx - item.x, my - item.y) < item.radius) {
                    if(item.text === lvl.corr) {
                      score += 150;
                    }
                    lvl = levels[Math.floor(Math.random() * levels.length)];
                    document.getElementById("bft").innerText = `f(x) = ${lvl.f}`;
                    spawnBalloons();
                  }
                }
              });
              function loop() {
                if(!gameActive) return;
                ctx.clearRect(0,0,450,240);
                ctx.fillStyle = "#1e293b"; ctx.fillRect(15,0,420,240);
                for(let item of items) {
                  item.y -= item.speed;
                  if(item.y < -30) item.y = 260;
                  ctx.beginPath(); ctx.arc(item.x, item.y, item.radius, 0, Math.PI*2);
                  ctx.fillStyle = "#334155"; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = "#64748b"; ctx.stroke();
                  ctx.fillStyle = "white"; ctx.font = "bold 12px sans-serif"; ctx.textAlign = "center";
                  ctx.fillText(item.text, item.x, item.y + 4);
                }
                document.getElementById("bs").innerText = score;
                requestAnimationFrame(loop);
              }
              loop();
            </script></body></html>
            """
            st.components.v1.html(balloons_code, height=370)

        # -------------------------------------------------------------
        # MUNDO 3: TENIS TRASCENDENTE (Velocidad muy suave + 60 segundos)
        # -------------------------------------------------------------
        elif b == 3:
            st.subheader("🎾 Fase 3: Tenis Trascendente (Límite: 60 segundos)")
            st.markdown("Pelota a velocidad suave. Golpea con la pala las derivadas correctas.")

            tennis_code = """
            <!DOCTYPE html>
            <html>
            <head><style>
              body { background: #020617; color: white; text-align: center; font-family: sans-serif; margin: 0; }
              canvas { background: #064e3b; border: 3px solid #10b981; border-radius: 10px; display: block; margin: 0 auto; cursor: pointer; }
              .btn-p { background: #059669; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; margin: 5px; }
            </style></head>
            <body>
              <div style="font-size: 14px; color: #10b981; font-weight: bold; margin-bottom: 4px;">⏱️ Tiempo: <span id="timer">60</span>s | Pts: <span id="ts">0</span></div>
              <div style="background: #1e293b; border: 2px solid #10b981; border-radius: 8px; padding: 6px; width: 420px; margin: 0 auto 6px auto;">
                <div style="color: #10b981; font-size: 14px; font-weight: bold;" id="tft">f(x) = 4sin(x)</div>
                <div style="color: white; font-size: 12px;">Golpea solo la derivada correcta</div>
              </div>
              <canvas id="tc" width="450" height="240"></canvas>
              <div style="margin-top: 6px;">
                <button class="btn-p" onclick="paddleX = Math.max(20, paddleX - 40)">⬅️ Izq</button>
                <button class="btn-p" onclick="paddleX = Math.min(360, paddleX + 40)">Der ➡️</button>
              </div>
            <script>
              const canvas = document.getElementById("tc");
              const ctx = canvas.getContext("2d");
              let score = 0, timeLeft = 60, gameActive = true;
              let paddleX = 185, paddleWidth = 90, paddleY = 210;

              const timerInterval = setInterval(() => {
                if(!gameActive) return;
                timeLeft--;
                document.getElementById("timer").innerText = timeLeft;
                if(timeLeft <= 0) {
                  gameActive = false;
                  alert("⏰ ¡Tiempo agotado! Puntuación final: " + score);
                }
              }, 1000);
              
              const rounds = [
                { f: "4sin(x)", corr: "4cos(x)", opts: ["4cos(x)", "-4sin(x)", "4sin(x)"] },
                { f: "3cos(x)", corr: "-3sin(x)", opts: ["3sin(x)", "-3sin(x)", "3cos(x)"] },
                { f: "2tan(x)", corr: "2sec²(x)", opts: ["2sec²(x)", "2csc²(x)", "2tan(x)"] }
              ];
              let currR = rounds[0];
              let ball = { x: 225, y: 30, vx: 0.5, vy: 0.5, text: currR.corr };

              function resetBall() {
                ball.x = Math.random() * 350 + 50;
                ball.y = 30;
                ball.vy = 0.5;
                let choice = Math.random() < 0.5 ? currR.corr : currR.opts[Math.floor(Math.random() * currR.opts.length)];
                ball.text = choice;
              }

              canvas.addEventListener('mousemove', e => {
                if(!gameActive) return;
                let rect = canvas.getBoundingClientRect();
                paddleX = e.clientX - rect.left - paddleWidth / 2;
                if(paddleX < 15) paddleX = 15;
                if(paddleX > 435 - paddleWidth) paddleX = 435 - paddleWidth;
              });

              function loop() {
                if(!gameActive) return;
                ctx.clearRect(0, 0, 450, 240);
                ctx.fillStyle = "#064e3b"; ctx.fillRect(15, 0, 420, 240);

                ball.x += ball.vx;
                ball.y += ball.vy;

                if(ball.x < 30 || ball.x > 420) ball.vx *= -1;
                if(ball.y < 20) ball.vy *= -1;

                if(ball.y >= paddleY - 10 && ball.y <= paddleY + 15 && ball.x >= paddleX && ball.x <= paddleX + paddleWidth) {
                  if(ball.text === currR.corr) {
                    score += 200;
                  }
                  currR = rounds[Math.floor(Math.random() * rounds.length)];
                  document.getElementById("tft").innerText = `f(x) = ${currR.f}`;
                  resetBall();
                }

                if(ball.y > 240) {
                  resetBall();
                }

                ctx.fillStyle = "#334155";
                ctx.beginPath(); ctx.arc(ball.x, ball.y, 22, 0, Math.PI*2); ctx.fill();
                ctx.lineWidth = 2; ctx.strokeStyle = "#64748b"; ctx.stroke();

                ctx.fillStyle = "white"; ctx.font = "bold 11px sans-serif"; ctx.textAlign = "center";
                ctx.fillText(ball.text, ball.x, ball.y + 4);

                ctx.fillStyle = "#facc15";
                ctx.fillRect(paddleX, paddleY, paddleWidth, 12);

                document.getElementById("ts").innerText = score;
                requestAnimationFrame(loop);
              }
              loop();
            </script></body></html>
            """
            st.components.v1.html(tennis_code, height=430)

        # -------------------------------------------------------------
        # MUNDO 4: TETRIS DE PRODUCTOS (Velocidad muy suave + 60 segundos)
        # -------------------------------------------------------------
        elif b == 4:
            st.subheader("🧱 Fase 4: Tetris de Productos (Límite: 60 segundos)")
            st.markdown("Piezas cayendo muy despacio. Haz clic en la correcta.")

            tetris_code = """
            <!DOCTYPE html>
            <html>
            <head><style>
              body { background: #020617; color: white; text-align: center; font-family: sans-serif; margin: 0; }
              canvas { background: #0f172a; border: 3px solid #f59e0b; border-radius: 10px; display: block; margin: 0 auto; cursor: pointer; }
              .btn-tet { background: #d97706; color: white; border: none; padding: 10px 18px; font-size: 15px; border-radius: 8px; cursor: pointer; font-weight: bold; margin: 4px; }
            </style></head>
            <body>
              <div style="font-size: 14px; color: #f59e0b; font-weight: bold; margin-bottom: 4px;">⏱️ Tiempo: <span id="timer">60</span>s | Puntos: <span id="pts">0</span></div>
              <div style="background: #1e293b; border: 2px solid #f59e0b; border-radius: 8px; padding: 6px; width: 420px; margin: 0 auto 6px auto;">
                <div style="color: #f59e0b; font-size: 14px; font-weight: bold;" id="tfunc">f(x) = x² · sin(x)</div>
                <div style="color: white; font-size: 12px;">Haz clic en la figura de Tetris correcta</div>
              </div>
              <canvas id="tc" width="450" height="240"></canvas>
              <div style="margin-top: 6px;">
                <button class="btn-tet" onclick="movePiece(-40)">⬅️ Izq</button>
                <button class="btn-tet" onclick="movePiece(40)">Der ➡️</button>
              </div>
            <script>
              const canvas = document.getElementById("tc");
              const ctx = canvas.getContext("2d");
              let score = 0, timeLeft = 60, gameActive = true;

              const timerInterval = setInterval(() => {
                if(!gameActive) return;
                timeLeft--;
                document.getElementById("timer").innerText = timeLeft;
                if(timeLeft <= 0) {
                  gameActive = false;
                  alert("⏰ ¡Tiempo agotado! Puntuación final: " + score);
                }
              }, 1000);

              const tetrisData = [
                { f: "x² · sin(x)", corr: "2x·sin(x) + x²·cos(x)", opts: ["2x·sin(x) + x²·cos(x)", "2x·cos(x)", "x²·sin(x)", "2x·sin(x) - x²·cos(x)"] },
                { f: "x · eˣ", corr: "eˣ + x·eˣ", opts: ["eˣ", "eˣ + x·eˣ", "x·eˣ", "1 + eˣ"] },
                { f: "x³ · cos(x)", corr: "3x²·cos(x) - x³·sin(x)", opts: ["3x²·cos(x)", "3x²·cos(x) - x³·sin(x)", "x³·sin(x)", "3x²·sin(x)"] }
              ];
              let currTet = tetrisData[0];
              const shapes = ['I', 'L', 'T', 'O'];
              let fallingPieces = [];

              function spawnTetrisPieces() {
                fallingPieces = [];
                let shuffled = [...currTet.opts].sort(() => Math.random() - 0.5);
                for(let i=0; i<4; i++) {
                  fallingPieces.push({
                    text: shuffled[i],
                    x: 50 + i * 100,
                    y: -40 - Math.random() * 40,
                    shape: shapes[i % shapes.length],
                    speed: 0.2 + Math.random() * 0.2
                  });
                }
              }
              spawnTetrisPieces();

              function movePiece(dir) {
                fallingPieces.forEach(p => p.x += dir);
              }

              canvas.addEventListener('click', e => {
                if(!gameActive) return;
                let rect = canvas.getBoundingClientRect();
                let mx = e.clientX - rect.left, my = e.clientY - rect.top;
                for(let p of fallingPieces) {
                  if(mx > p.x - 35 && mx < p.x + 35 && my > p.y - 35 && my < p.y + 35) {
                    if(p.text === currTet.corr) {
                      score += 250;
                    }
                    currTet = tetrisData[Math.floor(Math.random() * tetrisData.length)];
                    document.getElementById("tfunc").innerText = `f(x) = ${currTet.f}`;
                    spawnTetrisPieces();
                  }
                }
              });

              function drawShape(p) {
                ctx.fillStyle = "#334155";
                ctx.strokeStyle = "#64748b";
                ctx.lineWidth = 2;
                let px = p.x, py = p.y;
                
                if(p.shape === 'I') {
                  ctx.fillRect(px - 30, py - 10, 60, 20);
                  ctx.strokeRect(px - 30, py - 10, 60, 20);
                } else if(p.shape === 'L') {
                  ctx.fillRect(px - 20, py - 20, 20, 40);
                  ctx.fillRect(px, py, 20, 20);
                  ctx.strokeRect(px - 20, py - 20, 20, 40);
                  ctx.strokeRect(px, py, 20, 20);
                } else if(p.shape === 'T') {
                  ctx.fillRect(px - 30, py - 10, 60, 20);
                  ctx.fillRect(px - 10, py - 30, 20, 20);
                  ctx.strokeRect(px - 30, py - 10, 60, 20);
                  ctx.strokeRect(px - 10, py - 30, 20, 20);
                } else {
                  ctx.fillRect(px - 20, py - 20, 40, 40);
                  ctx.strokeRect(px - 20, py - 20, 40, 40);
                }

                ctx.fillStyle = "white";
                ctx.font = "bold 10px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText(p.text, px, py + 4);
              }

              function loop() {
                if(!gameActive) return;
                ctx.clearRect(0, 0, 450, 240);
                ctx.fillStyle = "#1e293b"; ctx.fillRect(15, 0, 420, 240);

                for(let p of fallingPieces) {
                  p.y += p.speed;
                  if(p.y > 260) p.y = -30;
                  drawShape(p);
                }

                document.getElementById("pts").innerText = score;
                requestAnimationFrame(loop);
              }
              loop();
            </script></body></html>
            """
            st.components.v1.html(tetris_code, height=430)

        # -------------------------------------------------------------
        # MUNDO 5: JEFE FINAL REGLA DE LA CADENA (60 segundos)
        # -------------------------------------------------------------
        elif b == 5:
            st.subheader("⚔️ Fase 5: Jefe Final - Regla de la Cadena (Límite: 60 segundos)")
            st.markdown("Combate contra el jefe respondiendo con calma antes de que acabe el tiempo.")

            boss_code = """
            <!DOCTYPE html>
            <html>
            <head><style>
              body { background: #020617; color: white; text-align: center; font-family: sans-serif; margin: 0; }
              canvas { background: #18181b; border: 3px solid #ef4444; border-radius: 10px; display: block; margin: 0 auto; }
              .btn-boss { background: #dc2626; color: white; border: none; padding: 10px 14px; font-size: 13px; border-radius: 6px; cursor: pointer; font-weight: bold; margin: 4px; }
              .btn-boss:hover { background: #b91c1c; }
            </style></head>
            <body>
              <div style="font-size: 14px; color: #ef4444; font-weight: bold; margin-bottom: 4px;">⏱️ Tiempo: <span id="timer">60</span>s | Puntos: <span id="bpts">0</span></div>
              <div style="background: #1e293b; border: 2px solid #ef4444; border-radius: 8px; padding: 6px; width: 420px; margin: 0 auto 6px auto;">
                <div style="color: #ef4444; font-size: 14px; font-weight: bold;" id="bof">f(x) = sin(4x²)</div>
              </div>
              <canvas id="bc" width="450" height="120"></canvas>
              <div id="optionsDiv" style="margin-top: 8px;"></div>
            <script>
              const canvas = document.getElementById("bc");
              const ctx = canvas.getContext("2d");
              let bossScore = 0, timeLeft = 60, gameActive = true;

              const timerInterval = setInterval(() => {
                if(!gameActive) return;
                timeLeft--;
                document.getElementById("timer").innerText = timeLeft;
                if(timeLeft <= 0) {
                  gameActive = false;
                  alert("⏰ ¡Tiempo agotado! Puntuación final contra el Jefe: " + bossScore);
                }
              }, 1000);

              const bosses = [
                { f: "sin(4x²)", corr: "cos(4x²) · 8x", opts: ["cos(4x²)", "cos(4x²) · 8x", "-sin(4x²) · 8x", "8x·sin(4x²)"] },
                { f: "(3x + 1)⁵", corr: "5(3x + 1)⁴ · 3", opts: ["5(3x + 1)⁴", "5(3x + 1)⁴ · 3", "(3x + 1)⁴ · 15", "3(3x + 1)⁴"] },
                { f: "e^(5x²)", corr: "e^(5x²) · 10x", opts: ["e^(5x²)", "10x·e^(5x)", "e^(5x²) · 10x", "5x·e^(5x²)"] }
              ];
              let currBoss = bosses[0];

              function renderOptions() {
                let container = document.getElementById("optionsDiv");
                container.innerHTML = "";
                currBoss.opts.forEach(opt => {
                  let btn = document.createElement("button");
                  btn.className = "btn-boss";
                  btn.innerText = opt;
                  btn.onclick = () => checkAttack(opt);
                  container.appendChild(btn);
                });
              }

              function checkAttack(val) {
                if(!gameActive) return;
                if(val === currBoss.corr) {
                  bossScore += 250;
                }
                currBoss = bosses[Math.floor(Math.random() * bosses.length)];
                document.getElementById("bof").innerText = `f(x) = ${currBoss.f}`;
                renderOptions();
                updateBossUI();
              }

              function updateBossUI() {
                document.getElementById("bpts").innerText = bossScore;
              }

              function loop() {
                if(!gameActive) return;
                ctx.clearRect(0,0,450,120);
                ctx.fillStyle = "#1e293b"; ctx.fillRect(15,0,420,120);
                ctx.fillStyle = "#ef4444"; ctx.fillRect(180, 35, 90, 55);
                ctx.fillStyle = "white"; ctx.font = "bold 14px sans-serif"; ctx.fillText("👾 JEFE CADENA", 225, 22);
                requestAnimationFrame(loop);
              }
              renderOptions(); updateBossUI(); loop();
            </script></body></html>
            """
            st.components.v1.html(boss_code, height=390)

    # ================= PANTALLA 3: INFORME Y PUNTUACIÓN FINAL =================
    elif st.session_state.screen == "summary":
        st.markdown(f"## 📊 Informe y Marcador de Piloto: `{st.session_state.current_user}`")
        
        total_score = u_data["score"]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🏆 Puntuación Final Total", f"{total_score} PTS")
        col2.metric("Aciertos", u_data["corrects"])
        col3.metric("Errores", u_data["errors"])
        
        st.markdown("---")
        if st.button("🗺️ Volver al Menú Principal (Fase 0)", use_container_width=True):
            st.session_state.screen = "map"
            st.rerun()
