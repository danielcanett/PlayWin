# -*- coding: utf-8 -*-
import streamlit as st

# --------- CONFIGURACIÓN DE LA PÁGINA ---------
st.set_page_config(page_title="Play & Win | Torneos Gaming", page_icon="🎮", layout="wide")

# --------- SESIÓN DE USUARIO (LOGIN SIMPLE) ---------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'nickname' not in st.session_state:
    st.session_state.nickname = ""
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'inscripciones' not in st.session_state:
    st.session_state.inscripciones = []

def login_widget():
    st.markdown("### Inicia sesión o regístrate para participar")
    nickname = st.text_input("Nickname (visible en rankings)", key="nickname_input")
    email = st.text_input("Correo electrónico", key="email_input")
    if st.button("Entrar"):
        if nickname and email:
            st.session_state.logged_in = True
            st.session_state.nickname = nickname
            st.session_state.email = email
            st.success(f"Bienvenido, {nickname}!")
        else:
            st.error("Debes ingresar nickname y correo.")

if not st.session_state.logged_in:
    login_widget()
    st.stop()

# --------- BOTÓN CERRAR SESIÓN ---------
st.sidebar.markdown(f"**Usuario:** {st.session_state.nickname}")
if st.sidebar.button("Cerrar sesión"):
    st.session_state.logged_in = False
    st.session_state.nickname = ""
    st.session_state.email = ""
    st.session_state.inscripciones = []
    st.rerun()

# --------- ESTILOS PERSONALIZADOS ---------
st.markdown("""
<style>
body { background: #10131a; }
.main { background-color: #1a1d25; }
.hero-title { font-size: 3.5rem; font-weight: 900; color: #00ffe7;}
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
</style>
""", unsafe_allow_html=True)

# --------- HERO SECTION ---------
st.markdown('<div class="hero-title">Compite, Gana y Cobra!</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Participa en torneos de tus juegos favoritos, gana dinero real y sube en el ranking. <br> ¡Demuestra tu habilidad y conviértete en leyenda!</div>', unsafe_allow_html=True)
st.markdown('<button class="custom-btn">Únete ahora</button>', unsafe_allow_html=True)

st.write("")
st.write("---")

# --------- SECCIÓN PARTIDAS DESTACADAS ---------
st.markdown('<div class="section-title">Partidas Destacadas</div>', unsafe_allow_html=True)
game_col1, game_col2, game_col3 = st.columns(3)

with game_col1:
    st.markdown(
        """
        <div class="game-card">
            <img class="game-img" src="https://cdn.cloudflare.steamstatic.com/steam/apps/578080/header.jpg" />
            <h3>PUBG</h3>
            <div class="prize">Premio: $1,000 MXN</div>
            <p>Solo / Dúo.<br>Próximo torneo: 20 de julio, 18:00 hrs.<br>¡Inscríbete y demuestra tu puntería!</p>
            <button class="custom-btn">Inscribirse</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

with game_col2:
    st.markdown(
        """
        <div class="game-card">
            <img class="game-img" src="fortnite.jpg" />
            <h3>Fortnite</h3>
            <div class="prize">Premio: $1,500 MXN</div>
            <p>Solo / Dúo.<br>Próximo torneo: 20 de julio, 18:00 hrs.<br>Construye, dispara, ¡y gana!</p>
            <button class="custom-btn">Inscribirse</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

with game_col3:
    st.markdown(
        """
        <div class="game-card">
            <img class="game-img" src="https://cdn.cloudflare.steamstatic.com/steam/apps/1506830/header.jpg" />
            <h3>FIFA</h3>
            <div class="prize">Premio: $2,000 MXN</div>
            <p>1v1 online.<br>Próximo torneo: 25 de julio, 21:00 hrs.<br>¡Golea y gana efectivo!</p>
            <button class="custom-btn">Inscribirse</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------- SECCIÓN DE INSCRIPCIÓN Y PAGO (PLACEHOLDER) ---------
st.markdown('<div class="section-title">Inscripción a Torneos</div>', unsafe_allow_html=True)
with st.form("inscripcion_form"):
    torneo = st.selectbox(
        "¿A qué torneo te quieres inscribir?",
        ["PUBG - 20 de julio", "Fortnite - 20 de julio", "FIFA - 25 de julio"],
    )
    st.info("El pago será procesado por MercadoPago. Prototipo MVP: recibirás instrucciones por email.")
    submit_inscripcion = st.form_submit_button("Inscribirse y pagar")
    if submit_inscripcion:
        st.session_state.inscripciones.append({
            "torneo": torneo,
            "fecha": "2025-01-21",
            "status": "Preinscrito",
        })
        st.success(f"¡Te has preinscrito al torneo de {torneo}! Recibirás instrucciones en tu correo {st.session_state.email}.")

# --------- HISTORIAL DE INSCRIPCIONES REAL ---------
st.markdown('<div class="section-title">Mi Historial de Torneos</div>', unsafe_allow_html=True)
if st.session_state.inscripciones:
    for i, ins in enumerate(st.session_state.inscripciones, 1):
        st.markdown(
            f"""
            <div class="user-history-card">
                <b>{i}. Torneo:</b> {ins['torneo']}<br>
                <b>Fecha inscripción:</b> {ins['fecha']}<br>
                <b>Estatus:</b> {ins['status']}
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("Aún no te has inscrito a ningún torneo. ¡Participa en uno arriba!")

# --------- SECCIÓN DE PREMIOS Y RANKING ---------
st.markdown('<div class="section-title">Ranking General/Div>', unsafe_allow_html=True)
rank_col1, rank_col2 = st.columns((2, 1))
with rank_col1:
    st.markdown(
        """
        <div class="ranking-card">
            <span class="ranking-pos">🥇 1</span> <b>PlayerPro</b> – $5,200 MXN ganados
        </div>
        <div class="ranking-card">
            <span class="ranking-pos">🥈 2</span> <b>FortniteKing</b> – $3,800 MXN ganados
        </div>
        <div class="ranking-card">
            <span class="ranking-pos">🥉 3</span> <b>FIFAMaster</b> – $2,950 MXN ganados
        </div>
        """,
        unsafe_allow_html=True,
    )
with rank_col2:
    st.markdown(
        """
        <div class="ranking-card">
            <b>¿Quieres estar aquí?</b><br>
            Juega, gana partidas y suma puntos.<br>
            <button class="custom-btn">Ver ranking completo</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------- SECCIÓN DE TESTIMONIOS / FAQ Y REGLAS ---------
st.markdown('<div class="section-title">¿Cómo funciona?</div>', unsafe_allow_html=True)
st.markdown(
    """
    <ul>
    <li><b>1.</b> Elige tu juego: PUBG, Fortnite, FIFA y más.</li>
    <li><b>2.</b> Inscríbete a un torneo: Selecciona el torneo que más te guste y regístrate.</li>
    <li><b>3.</b> Juega y gana: Compite en las partidas programadas.</li>
    <li><b>4.</b> Cobra tu premio: Si quedas en el top, ¡el dinero es tuyo!</li>
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

# --------- SECCIÓN DE CONTACTO ---------
st.markdown('<div class="section-title">¿Dudas o preguntas?</div>', unsafe_allow_html=True)
with st.form("contact_form"):
    name = st.text_input("Tu nombre")
    email = st.text_input("Correo electrónico")
    message = st.text_area("¿En qué te ayudamos?")
    submitted = st.form_submit_button("Enviar")
    if submitted:
        st.success("¡Gracias! Pronto nos pondremos en contacto contigo.")

# --------- FOOTER MEJORADO ---------
st.write("---")
cols_footer = st.columns(3)
with cols_footer[0]:
    st.caption("© 2025 Play & Win Gaming. Todos los derechos reservados.")
with cols_footer[1]:
    st.markdown(
        """
        <a href="https://instagram.com" target="_blank">Instagram</a> | 
        <a href="https://discord.com" target="_blank">Discord</a> | 
        <a href="mailto:contacto@playandwin.mx">Email</a>
        """,
        unsafe_allow_html=True,
    )
with cols_footer[2]:
    st.markdown(
        """
        <a href="#">Términos y condiciones</a> | 
        <a href="#">Aviso de privacidad</a>
        """,
        unsafe_allow_html=True,
    )