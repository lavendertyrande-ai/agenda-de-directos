from flask import Flask, render_template, request, redirect, flash, url_for
from db import db
from models import Reserva, TwitchUser
import pkgutil

if not hasattr(pkgutil, "get_loader"):
    import importlib.util
    def get_loader(name):
        spec = importlib.util.find_spec(name)
        return spec.loader if spec else None
    pkgutil.get_loader = get_loader


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SECRET_KEY'] = 'clave-secreta'
db.init_app(app)

with app.app_context():
    db.create_all()


# Función para verificar disponibilidad
def hora_disponible(hora):
    return not Reserva.query.filter(
        (Reserva.hora1 == hora) | (Reserva.hora2 == hora) | (Reserva.hora3 == hora)
    ).first()


@app.route("/", methods=["GET", "POST"])
def index():
    horas = [f"{dia} {h}:00" for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"] for h in range(16, 25)]
    ids = TwitchUser.query.all()  # 🔴 cargar IDs de Twitch

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


# Ruta para añadir nuevas IDs de Twitch
@app.route("/add_twitch", methods=["POST"])
def add_twitch():
    twitch_id = request.form.get("twitch_id")
    if twitch_id:
        nuevo = TwitchUser(twitch_id=twitch_id)
        db.session.add(nuevo)
        db.session.commit()
        flash("ID de Twitch añadido correctamente ✅")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

