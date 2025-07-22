import streamlit as st
import db
import datetime

# --- ESTILO PERSONALIZADO ---
st.markdown("""
<style>
body { background: #10131a !important; }
.main, .block-container { background-color: #181c25 !important; }
.hero-title { font-size: 3.5rem; font-weight: 900; color: #00ffe7; text-shadow: 2px 2px #000;}
.hero-subtitle { font-size: 1.5rem; color: #e6e6e6; margin-bottom: 2rem;}
.section-title { font-size: 2rem; font-weight: bold; color: #00ffe7; margin-top: 3rem;}
.custom-btn {
    padding: 1rem 2rem;
    background: linear-gradient(90deg, #00ffe7, #4169e1);
    color: #181c25;
    border: none;
    border-radius: 50px;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    margin-top: 1rem;
    box-shadow: 0 4px 16px #00ffe788;
    transition: background 0.3s;
}
.custom-btn:hover {
    background: linear-gradient(90deg, #4169e1, #00ffe7);
}
.game-card {
    background: #222532;
    border-radius: 18px;
    box-shadow: 0 2px 20px #00ffe733;
    padding: 1.5rem;
    color: #fff;
    margin-bottom: 2rem;
    min-height: 260px;
    text-align: center;
    transition: transform 0.2s;
    border: 2px solid #1a1d25;
}
.game-card:hover {
    transform: translateY(-10px) scale(1.04);
    box-shadow: 0 8px 32px #00ffe755;
    border: 2px solid #00ffe7;
}
.game-img {
    border-radius: 12px;
    margin-bottom: 1rem;
    max-height: 100px;
    width: 60%;
}
.prize {
    color: #00ffe7;
    font-weight: bold;
    font-size: 1.1rem;
}
.ranking-card {
    background: #181c25;
    border-radius: 18px;
    box-shadow: 0 2px 12px #4169e122;
    padding: 1.2rem;
    color: #fff;
    margin-bottom: 1.2rem;
    transition: transform 0.25s;
    border-left: 6px solid #00ffe7;
}
.ranking-pos {
    font-size: 1.5rem;
    color: #00ffe7;
    font-weight: bold;
    margin-right: 1rem;
}
.user-history-card {
    background: #23263a;
    border-radius: 10px;
    color: #fff;
    padding: 1rem;
    margin-bottom: 1rem;
    border-left: 4px solid #00ffe7;
}
.stButton>button {
    font-size: 1rem;
    font-weight: bold;
    border-radius: 12px;
    background: linear-gradient(90deg, #00ffe7, #4169e1);
    color: #181c25;
    border: none;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    transition: background 0.3s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #4169e1, #00ffe7);
    color: #181c25;
}
</style>
""", unsafe_allow_html=True)

db.setup_db()

# --- ADMIN USER AUTOCREATION ---
admin_nick = "admin"
admin_email = "admin@playwin.mx"
user = db.get_user_by_nickname(admin_nick)
if not user:
    db.register_user(admin_nick, admin_email, admin=1)
else:
    if not user["admin"]:
        with db.get_conn() as conn:
            conn.execute("UPDATE users SET admin=1 WHERE id=?", (user["id"],))

# --- CARGA TORNEOS DE EJEMPLO SI NO HAY NINGUNO ---
if not db.get_torneos(activos_only=False):
    ejemplo_torneos = [
        ("Fortnite", "Fortnite Summer Cup", "2025-08-01", 1500, "¡Construye, dispara y gana!"),
        ("PUBG", "PUBG Battle Masters", "2025-08-05", 1000, "Demuestra tu puntería en el campo de batalla."),
        ("FIFA", "FIFA Kings League", "2025-08-10", 2000, "Conviértete en campeón FIFA."),
    ]
    for j, n, f, p, d in ejemplo_torneos:
        db.add_torneo(j, n, f, p, d)

st.set_page_config(page_title="Play & Win | Torneos Gaming", page_icon="🎮", layout="wide")

if 'user' not in st.session_state:
    st.session_state.user = None

# ------------------ LOGIN/REGISTRO ------------------
def login_widget():
    st.markdown("### Inicia sesión o regístrate para participar")
    nickname = st.text_input("Nickname (visible en rankings)")
    email = st.text_input("Correo electrónico")
    if st.button("Entrar"):
        user = db.authenticate_user(nickname, email)
        if user:
            st.session_state.user = dict(user)
            st.success(f"¡Bienvenido, {nickname}!")
        else:
            ok, msg = db.register_user(nickname, email)
            if ok:
                st.session_state.user = dict(db.authenticate_user(nickname, email))
                st.success(f"¡Registro exitoso, {nickname}!")
            else:
                st.error(msg)

if not st.session_state.user:
    login_widget()
    st.stop()

# ------------------ SIDEBAR ------------------
st.sidebar.markdown(f"**Usuario:** {st.session_state.user['nickname']}")
if st.sidebar.button("Cerrar sesión"):
    st.session_state.user = None
    st.rerun()
if st.session_state.user.get("admin"):
    st.sidebar.page_link("admin.py", label="Panel Admin", icon="🔑")

# ------------------ HERO ------------------
st.image("assets/banner.png", use_column_width=True)  # Asegúrate de tener tu banner en assets/banner.png o cambia el nombre
st.markdown('<div class="hero-title">Compite, Gana y Cobra!</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Participa en torneos de tus juegos favoritos, gana dinero real y sube en el ranking.<br>¡Demuestra tu habilidad y conviértete en leyenda!</div>', unsafe_allow_html=True)

# ------------------ CARDS DE TORNEOS ------------------
st.markdown('<div class="section-title">Partidas Destacadas</div>', unsafe_allow_html=True)
torneos = db.get_torneos()
if torneos:
    cols = st.columns(len(torneos))
    for i, t in enumerate(torneos):
        with cols[i]:
            # Puedes cambiar la imagen por una específica por juego si quieres
            img_path = "assets/{}.jpg".format(t['juego']) if t['juego'] in ["Fortnite", "PUBG", "FIFA"] else None
            if img_path:
                try:
                    st.image(img_path, use_column_width=True)
                except:
                    pass
            st.markdown(
                f"""
                <div class="game-card">
                    <h3>{t['juego']}</h3>
                    <div class="prize">Premio: ${t['premio']} MXN</div>
                    <p>{t['nombre']}<br>Próximo torneo: {t['fecha']}<br>{t['descripcion']}</p>
                </div>
                """, unsafe_allow_html=True
            )
            if st.button("Inscribirse", key=f"insc_card_{t['id']}"):
                ok, msg = db.inscribir_usuario(
                    st.session_state.user['id'], t['id'], datetime.date.today().strftime('%Y-%m-%d')
                )
                if ok:
                    st.success(msg)
                else:
                    st.warning(msg)
else:
    st.info("No hay torneos activos disponibles en este momento. ¡Vuelve pronto!")

# ------------------ HISTORIAL DEL USUARIO ------------------
st.markdown('<div class="section-title">Mi Historial de Torneos</div>', unsafe_allow_html=True)
hist = db.get_inscripciones_usuario(st.session_state.user['id'])
if hist:
    for ins in hist:
        st.markdown(
            f"""
            <div class="user-history-card">
                <b>Torneo:</b> {ins['torneo_nombre']} ({ins['juego']})<br>
                <b>Fecha inscripción:</b> {ins['fecha_insc']}<br>
                <b>Estatus:</b> {ins['status']}<br>
                <b>Premio:</b> ${ins['premio']} MXN
            </div>
            """, unsafe_allow_html=True
        )
else:
    st.info("Aún no te has inscrito a ningún torneo. ¡Participa en uno arriba!")

# ------------------ RANKING GENERAL ------------------
st.markdown('<div class="section-title">Ranking General</div>', unsafe_allow_html=True)
ranking = db.get_ranking()
for pos, r in enumerate(ranking, 1):
    st.markdown(
        f"""
        <div class="ranking-card">
            <span class="ranking-pos">🥇 {pos}</span> <b>{r['nickname']}</b> – ${r['total_ganado'] or 0} MXN ganados | Puntos: {r['points']} | Badges: {r['badges']}
        </div>
        """,
        unsafe_allow_html=True
    )
if st.button("Ver ranking completo"):
    full_rank = db.get_full_ranking()
    st.markdown("### Ranking completo")
    for pos, r in enumerate(full_rank, 1):
        st.markdown(f"{pos}. {r['nickname']} - ${r['total_ganado'] or 0} MXN - Puntos: {r['points']} - Badges: {r['badges']}")

# ------------------ FAQ y CONTACTO ------------------
st.markdown('<div class="section-title">¿Cómo funciona?</div>', unsafe_allow_html=True)
st.markdown(
    """
    <ul>
    <li><b>1.</b> Elige tu juego y torneo.</li>
    <li><b>2.</b> Inscríbete y paga la inscripción.</li>
    <li><b>3.</b> Juega y gana.</li>
    <li><b>4.</b> Cobra tu premio si quedas en top.</li>
    </ul>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="section-title">Preguntas Frecuentes / Reglas</div>', unsafe_allow_html=True)
with st.expander("¿Cómo cobro mi premio?"):
    st.write("Si quedas en los primeros lugares, recibirás instrucciones para cobrar por transferencia bancaria, MercadoPago o PayPal.")
with st.expander("¿Qué pasa si hago trampa?"):
    st.write("Cuentas fraudulentas, trampas o cualquier comportamiento sospechoso resultarán en descalificación y baneo.")
with st.expander("¿Hay límite de torneos por persona?"):
    st.write("No, puedes participar en todos los torneos que quieras, siempre y cuando pagues la inscripción.")
with st.expander("¿Cómo se verifican los ganadores?"):
    st.write("El staff revisa los resultados y partidas grabadas. Si hay reclamos, se revisan pruebas antes de premiar.")

# ------------------ CONTACTO ------------------
st.markdown('<div class="section-title">¿Dudas o preguntas?</div>', unsafe_allow_html=True)
with st.form("contact_form"):
    nombre = st.text_input("Tu nombre")
    email = st.text_input("Correo electrónico", key="contact_email")
    mensaje = st.text_area("¿En qué te ayudamos?")
    if st.form_submit_button("Enviar"):
        st.success("¡Gracias! Pronto nos pondremos en contacto contigo.")

st.write("---")
st.caption("© 2025 Play & Win Gaming. Todos los derechos reservados.")