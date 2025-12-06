from flask import Flask, render_template, request, redirect, flash, url_for, session
from db import db
from models import Reserva, TwitchUser
import pkgutil

# Parche para compatibilidad con Python 3.14
if not hasattr(pkgutil, "get_loader"):
    import importlib.util
    def get_loader(name):
        spec = importlib.util.find_spec(name)
        return spec.loader if spec else None
    pkgutil.get_loader = get_loader

# Crear aplicación Flask
app = Flask(__name__)

# Configuración
app.config['ADMIN_SECRET'] = "Canelito-Exiliado0909"   # 🔑 Tu clave secreta personal
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SECRET_KEY'] = 'clave-secreta'             # Para sesiones y mensajes flash
db.init_app(app)

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# Función para verificar disponibilidad
def hora_disponible(hora):
    return not Reserva.query.filter(
        (Reserva.hora1 == hora) | (Reserva.hora2 == hora) | (Reserva.hora3 == hora)
    ).first()

# Página principal con formulario de reservas
@app.route("/", methods=["GET", "POST"])
def index():
    horas = [f"{dia} {h}:00" for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"] for h in range(16, 25)]
    ids = TwitchUser.query.all()

    if request.method == "POST":
        twitch_id = request.form.get("twitch_id")
        hora1 = request.form.get("hora1")
        hora2 = request.form.get("hora2")
        hora3 = request.form.get("hora3")

        # Validar disponibilidad
        for h in [hora1, hora2, hora3]:
            if h and not hora_disponible(h):
                flash(f"Hora no disponible, elige otra: {h}")
                return redirect(url_for("index"))

        reserva = Reserva(twitch_id=twitch_id, hora1=hora1, hora2=hora2, hora3=hora3)
        db.session.add(reserva)
        db.session.commit()
        flash("Reserva realizada con éxito ✅")
        return redirect(url_for("index"))

    return render_template("index.html", horas=horas, ids=ids)

# ---------------------------
# LOGIN / LOGOUT / ADMIN
# ---------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        secret = request.form.get("secret")
        if secret == app.config['ADMIN_SECRET']:
            session["is_admin"] = True
            flash("Acceso concedido ✅")
            return redirect(url_for("admin_panel"))
        else:
            flash("Clave incorrecta ❌")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("is_admin", None)
    flash("Sesión cerrada ✅")
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET"])
def admin_panel():
    if not session.get("is_admin"):
        flash("Acceso restringido. Por favor, inicia sesión.")
        return redirect(url_for("login"))
    ids = TwitchUser.query.all()
    reservas = Reserva.query.all()
    return render_template("admin.html", ids=ids, reservas=reservas)

@app.route("/admin/add_twitch", methods=["POST"])
def admin_add_twitch():
    if not session.get("is_admin"):
        flash("Acceso restringido ❌")
        return redirect(url_for("login"))

    twitch_id = request.form.get("twitch_id")
    if twitch_id:
        nuevo = TwitchUser(twitch_id=twitch_id)
        db.session.add(nuevo)
        db.session.commit()
        flash("ID de Twitch añadido correctamente ✅")
    return redirect(url_for("admin_panel"))

# ---------------------------

# Ejecutar servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
