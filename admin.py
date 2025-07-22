import streamlit as st
import db

st.set_page_config(page_title="Panel Admin | Play & Win", page_icon="🔑", layout="wide")

if 'user' not in st.session_state or not st.session_state.user.get("admin"):
    st.warning("Acceso restringido. Solo administradores.")
    st.stop()

st.header("Panel de Administración")

st.subheader("Gestión de Torneos")
torneos = db.get_torneos(activos_only=False)
for t in torneos:
    c = st.container()
    with c:
        st.write(f"ID: {t['id']} | {t['juego']} - {t['nombre']} | Premio: ${t['premio']} | Fecha: {t['fecha']} | Activo: {bool(t['activo'])}")
        if st.button("Editar", key=f"edit_{t['id']}"):
            with st.form(f"form_edit_{t['id']}"):
                juego = st.text_input("Juego", value=t['juego'])
                nombre = st.text_input("Nombre", value=t['nombre'])
                fecha = st.text_input("Fecha", value=t['fecha'])
                premio = st.number_input("Premio", value=t['premio'])
                descripcion = st.text_area("Descripción", value=t['descripcion'])
                activo = st.checkbox("Activo", value=bool(t["activo"]))
                if st.form_submit_button("Guardar cambios"):
                    db.edit_torneo(t["id"], juego, nombre, fecha, premio, descripcion, int(activo))
                    st.success("Torneo actualizado.")
                    st.rerun()
        if st.button("Eliminar", key=f"del_{t['id']}"):
            db.delete_torneo(t["id"])
            st.warning("Torneo eliminado.")
            st.rerun()

st.subheader("Agregar nuevo torneo")
with st.form("nuevo_torneo"):
    juego = st.text_input("Juego")
    nombre = st.text_input("Nombre del torneo")
    fecha = st.text_input("Fecha (YYYY-MM-DD)")
    premio = st.number_input("Premio MXN", min_value=0)
    descripcion = st.text_area("Descripción")
    if st.form_submit_button("Agregar"):
        db.add_torneo(juego, nombre, fecha, premio, descripcion)
        st.success("Torneo agregado.")
        st.rerun()

st.subheader("Inscripciones por torneo")
for t in torneos:
    st.markdown(f"**Torneo:** {t['nombre']} ({t['juego']}) - {t['fecha']}")
    insc = db.get_inscripciones_torneo(t["id"])
    if insc:
        for i in insc:
            st.write(f" - {i['nickname']} ({i['email']}) | Fecha: {i['fecha_insc']} | Status: {i['status']}")
    else:
        st.write("Sin inscripciones aún.")