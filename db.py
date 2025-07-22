import sqlite3
from contextlib import contextmanager
import hashlib

DATABASE = "playwin.db"

@contextmanager
def get_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def setup_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT,
            admin INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            badges TEXT DEFAULT ''
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS torneos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            juego TEXT NOT NULL,
            nombre TEXT NOT NULL,
            fecha TEXT NOT NULL,
            premio INTEGER NOT NULL,
            descripcion TEXT,
            activo INTEGER DEFAULT 1
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            torneo_id INTEGER NOT NULL,
            fecha_insc TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(torneo_id) REFERENCES torneos(id)
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS premios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            torneo_id INTEGER NOT NULL,
            posicion INTEGER NOT NULL,
            monto INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(torneo_id) REFERENCES torneos(id)
        )
        """)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(nickname, email, password="", admin=0):
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (nickname, email, password, admin) VALUES (?, ?, ?, ?)",
                (nickname, email, hash_password(password) if password else "", admin)
            )
        return True, "Registro exitoso."
    except sqlite3.IntegrityError as e:
        return False, "Email o nickname ya registrados."

def authenticate_user(nickname, email):
    with get_conn() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE nickname=? AND email=?", (nickname, email)
        ).fetchone()
        return user

def get_user_by_id(user_id):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE id=?", (user_id,)
        ).fetchone()

def get_user_by_nickname(nickname):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE nickname=?", (nickname,)
        ).fetchone()

def get_user_by_email(email):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email=?", (email,)
        ).fetchone()

def get_torneos(activos_only=True):
    with get_conn() as conn:
        if activos_only:
            return conn.execute("SELECT * FROM torneos WHERE activo=1").fetchall()
        return conn.execute("SELECT * FROM torneos").fetchall()

def add_torneo(juego, nombre, fecha, premio, descripcion):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO torneos (juego, nombre, fecha, premio, descripcion) VALUES (?, ?, ?, ?, ?)",
            (juego, nombre, fecha, premio, descripcion)
        )

def edit_torneo(torneo_id, juego, nombre, fecha, premio, descripcion, activo):
    with get_conn() as conn:
        conn.execute(
            "UPDATE torneos SET juego=?, nombre=?, fecha=?, premio=?, descripcion=?, activo=? WHERE id=?",
            (juego, nombre, fecha, premio, descripcion, activo, torneo_id)
        )

def delete_torneo(torneo_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM torneos WHERE id=?", (torneo_id,))

def inscribir_usuario(user_id, torneo_id, fecha, status="Preinscrito"):
    with get_conn() as conn:
        # Evita inscripcion doble
        existe = conn.execute(
            "SELECT * FROM inscripciones WHERE user_id=? AND torneo_id=?", (user_id, torneo_id)
        ).fetchone()
        if existe:
            return False, "Ya estás inscrito a este torneo."
        conn.execute(
            "INSERT INTO inscripciones (user_id, torneo_id, fecha_insc, status) VALUES (?, ?, ?, ?)",
            (user_id, torneo_id, fecha, status)
        )
        return True, "Inscripción exitosa."

def get_inscripciones_usuario(user_id):
    with get_conn() as conn:
        return conn.execute("""
            SELECT i.*, t.nombre as torneo_nombre, t.juego, t.fecha as torneo_fecha, t.premio
            FROM inscripciones i
            JOIN torneos t ON t.id = i.torneo_id
            WHERE i.user_id=?
            ORDER BY i.fecha_insc DESC
        """, (user_id,)).fetchall()

def get_inscripciones_torneo(torneo_id):
    with get_conn() as conn:
        return conn.execute("""
            SELECT i.*, u.nickname, u.email
            FROM inscripciones i
            JOIN users u ON u.id = i.user_id
            WHERE i.torneo_id=?
        """, (torneo_id,)).fetchall()

def add_premio(user_id, torneo_id, posicion, monto, fecha):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO premios (user_id, torneo_id, posicion, monto, fecha) VALUES (?, ?, ?, ?, ?)",
            (user_id, torneo_id, posicion, monto, fecha)
        )
        # Suma puntos y badges al usuario
        points = {1: 100, 2: 60, 3: 30}.get(posicion, 10)
        conn.execute(
            "UPDATE users SET points = points + ? WHERE id = ?",
            (points, user_id)
        )

def get_ranking(top=10):
    with get_conn() as conn:
        return conn.execute("""
            SELECT u.nickname, SUM(p.monto) as total_ganado, u.points, u.badges
            FROM premios p
            JOIN users u ON u.id = p.user_id
            GROUP BY p.user_id
            ORDER BY total_ganado DESC, u.points DESC
            LIMIT ?
        """, (top,)).fetchall()

def get_full_ranking():
    with get_conn() as conn:
        return conn.execute("""
            SELECT u.nickname, SUM(p.monto) as total_ganado, u.points, u.badges
            FROM premios p
            JOIN users u ON u.id = p.user_id
            GROUP BY p.user_id
            ORDER BY total_ganado DESC, u.points DESC
        """).fetchall()